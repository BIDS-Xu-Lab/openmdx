// ClinicalCase.ts (simple version, no "extends")

// ---------- Core primitives ----------

export type ID = string;
export type ISODateTime = string;

export type ClinicalCaseStatus = "draft" | "active" | "completed" | "archived";

// ---------- Case metadata & patient ----------

export interface ClinicalCaseMeta {
  case_id: ID;
  title?: string;
  source?: "manual" | "upload" | "api";
  schema_version: "1.0.0";
  created_at: ISODateTime;
  updated_at: ISODateTime;
}

export interface PatientCore {
  age?: number;
  sex?: "M" | "F" | "O";
  mrn_masked?: string;
}

// ---------- Notes ----------

export type NoteType = "HPI" | "ROS" | "PE" | "Labs" | "Imaging" | "AP" | "Other";

export interface ClinicalNote {
  note_id: ID;
  type: NoteType;
  content_markdown: string;
  created_at: ISODateTime;
  updated_at: ISODateTime;
}

// ---------- Simple output ----------

export interface EvidenceSnippet {
  text: string;
  source_ref?: string;
}

export interface DifferentialItem {
  dx_id: ID;
  label: string;
  prob?: number;
  evidence: EvidenceSnippet[];
  guideline_badge?: boolean;
  red_flag?: boolean;
}

export interface NextStepItem {
  step_id: ID;
  label: string;
  reason: string;
  eta?: string;
  risk?: "low" | "mid" | "high";
}

export interface SimpleUncertainty {
  missing_top2?: string[];
  red_flags?: string[];
}

export interface SimpleView {
  summary_line?: string;
  differential_top3: DifferentialItem[];
  next_steps_top3: NextStepItem[];
  uncertainty?: SimpleUncertainty;
}

// ---------- Agents ----------

export interface AgentInfo {
  agent_id: ID;
  name: string;
  model?: string;
  enabled?: boolean;
}

// ---------- Conversation ----------

export type ParticipantKind = "user" | "agent" | "tool" | "system";

export interface Participant {
  participant_id: ID;
  kind: ParticipantKind;
  display_name?: string;
}

export type MessageKind = "text" | "tool_call" | "tool_result";

export interface Message {
  message_id: ID;
  ts: ISODateTime;
  from_id: ID;
  to_id?: ID;
  kind: MessageKind;
  text?: string;
  payload_json?: unknown;
}

export interface Conversation {
  participants: Participant[];
  timeline: Message[];
}

// ---------- User questions ----------

export type QuestionStatus = "pending" | "answered" | "dismissed";

export interface UserQuestion {
  question_id: ID;
  text: string;
  asked_by: ID;
  status: QuestionStatus;
  answer_message_id?: ID;
  created_at: ISODateTime;
  updated_at: ISODateTime;
}

// ---------- Aggregate root ----------

export interface ClinicalCase {
  meta: ClinicalCaseMeta;
  status: ClinicalCaseStatus;

  patient: PatientCore;
  notes: ClinicalNote[];

  simple: SimpleView;

  agents: AgentInfo[];
  conversation: Conversation;
  questions: UserQuestion[];

  created_at: ISODateTime;
  updated_at: ISODateTime;
}

// ---------- Helpers ----------

export function createEmptyClinicalCase(partial?: Partial<ClinicalCase>): ClinicalCase {
  const now = new Date().toISOString();
  return {
    meta: {
      case_id: generateId(),
      title: partial?.meta?.title,
      source: partial?.meta?.source ?? "manual",
      schema_version: "1.0.0",
      created_at: now,
      updated_at: now,
    },
    status: partial?.status ?? "draft",
    created_at: now,
    updated_at: now,

    patient: partial?.patient ?? {},
    notes: partial?.notes ?? [],

    simple: partial?.simple ?? {
      summary_line: "",
      differential_top3: [],
      next_steps_top3: [],
      uncertainty: {},
    },

    agents: partial?.agents ?? [],
    conversation: partial?.conversation ?? { participants: [], timeline: [] },
    questions: partial?.questions ?? [],
  };
}

export function addMessage(clinical_case: ClinicalCase, msg: Message): ClinicalCase {
  const updated: ClinicalCase = { ...clinical_case };
  updated.conversation = {
    ...updated.conversation,
    timeline: [...updated.conversation.timeline, msg],
  };
  updated.updated_at = new Date().toISOString();
  return updated;
}

export function addUserQuestion(
  clinical_case: ClinicalCase,
  q: Omit<UserQuestion, "created_at" | "updated_at">
): ClinicalCase {
  const now = new Date().toISOString();
  const new_q: UserQuestion = { ...q, created_at: now, updated_at: now };
  const updated: ClinicalCase = { ...clinical_case, questions: [...clinical_case.questions, new_q] };
  updated.updated_at = now;
  return updated;
}

export function upsertAgent(clinical_case: ClinicalCase, agent: AgentInfo): ClinicalCase {
  const idx = clinical_case.agents.findIndex(a => a.agent_id === agent.agent_id);
  const agents =
    idx >= 0
      ? clinical_case.agents.map(a => (a.agent_id === agent.agent_id ? agent : a))
      : [...clinical_case.agents, agent];
  return { ...clinical_case, agents, updated_at: new Date().toISOString() };
}

// ---------- ID generator ----------

export function generateId(): ID {
  const g: unknown = (globalThis as any)?.crypto?.randomUUID?.();
  return typeof g === "string" && g.length > 0
    ? (g as ID)
    : (`id_${Math.random().toString(36).slice(2)}` as ID);
}