import { defineStore } from 'pinia';
import type { ClinicalCase, EvidenceSnippet, Message } from '../models/ClinicalCase';

export const useCaseStore = defineStore('case', {
    state: () => ({
        clinical_case: null as ClinicalCase | null,
        current_evidence_tab: 0,
        show_thinking: false,
        chat_rating: 0,
        input_text: '',
        is_recording: false,
    }),

    getters: {
        evidence_dict: (state) => {
            const dict: { [key: string]: any } = {};
            const snippets = state.clinical_case?.evidence_snippets || [];
            snippets.forEach((snippet: EvidenceSnippet) => {
                dict[snippet.snippet_id] = snippet;
            });
            return dict;
        },
        messages: (state) => state.clinical_case?.messages || [],
        evidence_snippets: (state) => state.clinical_case?.evidence_snippets || [],
        current_evidence: (state) => {
            const snippets = state.clinical_case?.evidence_snippets || [];
            return snippets[state.current_evidence_tab] || null;
        },
        evidence_count: (state) => state.clinical_case?.evidence_snippets?.length || 0,
    },

    actions: {
        setClinicalCase(case_data: ClinicalCase | null) {
            this.clinical_case = case_data;
        },

        setCurrentEvidenceTab(index: number) {
            this.current_evidence_tab = index;
        },

        toggleThinking() {
            this.show_thinking = !this.show_thinking;
        },

        setChatRating(rating: number) {
            this.chat_rating = rating;
        },

        setInputText(text: string) {
            this.input_text = text;
        },

        toggleRecording() {
            this.is_recording = !this.is_recording;
        },

        addMessage(message: Message) {
            if (this.clinical_case) {
                this.clinical_case.messages.push(message);
                this.clinical_case.updated_at = new Date().toISOString();
            }
        },

        copyChatHistory() {
            const messages = this.messages;
            const chatText = messages.map(msg => {
                const sender = msg.message_type === 'USER' ? 'User' : 
                             msg.message_type === 'AGENT' ? 'Agent' : 
                             msg.message_type === 'TOOL' ? 'Tool' : 'System';
                return `${sender}: ${msg.text || ''}`;
            }).join('\n\n');
            
            navigator.clipboard.writeText(chatText);
        },

        exportChatHistory() {
            const messages = this.messages;
            const chatData = {
                case_id: this.clinical_case?.case_id,
                title: this.clinical_case?.title,
                export_date: new Date().toISOString(),
                messages: messages.map(msg => ({
                    id: msg.message_id,
                    type: msg.message_type,
                    text: msg.text,
                    timestamp: msg.created_at,
                    payload: msg.payload_json
                }))
            };
            
            const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `chat_history_${this.clinical_case?.case_id || 'unknown'}.json`;
            a.click();
            URL.revokeObjectURL(url);
        },

        exportEvidence() {
            const evidence = this.evidence_snippets;
            const evidenceData = {
                case_id: this.clinical_case?.case_id,
                title: this.clinical_case?.title,
                export_date: new Date().toISOString(),
                evidence_snippets: evidence.map(snippet => ({
                    id: snippet.snippet_id,
                    text: snippet.text,
                    source_id: snippet.source_id,
                    source_type: snippet.source_type,
                    source_url: snippet.source_url,
                    source_citation: snippet.source_citation,
                    created_at: snippet.created_at
                }))
            };
            
            const blob = new Blob([JSON.stringify(evidenceData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `evidence_${this.clinical_case?.case_id || 'unknown'}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }
    }
});
