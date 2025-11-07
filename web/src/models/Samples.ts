import {
    ClinicalCaseStatus,
    createEmptyMessage,
    MessageType,
} from "./ClinicalCase";
import type { ClinicalCase, EvidenceSnippet, Message } from "./ClinicalCase";

export const questions = [
    {
        section: "Ask for a Quick Fact",
        text: "What is the intravenous half-life of atropine?",
    },
    {
        section: "Ask for a Quick Fact",
        text: "When is high-dose atorvastatin indicated?",
    },
    {
        section: "Ask for a Quick Fact",
        text:
            "Can you explain the concept of the net state of immunosuppression?",
    },

    {
        section: "Write Home Care Instructions",
        text:
            "Provide discharge guidance for someone recovering from a mild ankle sprain, emphasizing RICE therapy, limits on activity, and follow-up needs.",
    },
    {
        section: "Write Home Care Instructions",
        text:
            "Prepare instructions for post-minor skin procedure care—cover cleaning, infection signs, showering, and timing of suture removal.",
    },
    {
        section: "Write Home Care Instructions",
        text:
            "Outline home management for a patient after a mild asthma flare, including inhaler technique, medication duration, and warning signs for emergency evaluation.",
    },

    {
        section: "Prepare For MOC Exams",
        text:
            "How should a 7-year-old with diarrhea and a stool test positive for Giardia be managed?",
    },
    {
        section: "Prepare For MOC Exams",
        text:
            "What is the best next step for a 60-year-old man presenting with chest pain, hypertension, and lateral ST-segment depression?",
    },
    {
        section: "Prepare For MOC Exams",
        text:
            "Identify the most likely organism causing meningitis in a 32-year-old woman with fever, headache, and neutrophilic CSF findings.",
    },

    {
        section: "Ask in a Language Other Than English",
        text:
            "¿De qué manera el PCP produce daño pulmonar en pacientes que no tienen VIH?",
    },
    {
        section: "Ask in a Language Other Than English",
        text:
            "Quelles sont les recommandations actuelles de l'ATS et de l'IDSA pour traiter l'histoplasmose ?",
    },

    {
        section: "Compute Common Formulas",
        text:
            "Given a serum calcium of 7.8 mg/dL and albumin of 2.5 g/dL, compute the corrected calcium and determine if hypocalcemia is present.",
    },
    {
        section: "Compute Common Formulas",
        text:
            "Determine the dexamethasone equivalent for a patient switching from 40 mg of prednisone daily.",
    },
    {
        section: "Compute Common Formulas",
        text:
            "With sodium 140 mEq/L, creatinine 2.0 mg/dL, urine sodium 50 mEq/L, and urine creatinine 100 mg/dL, calculate FENa and decide whether the AKI is prerenal or intrinsic.",
    },

    {
        section: "Double Check with a Quick Curbside Consult",
        text:
            "For a suspected meniscal tear, should knee MRI be ordered with or without contrast?",
    },
    {
        section: "Double Check with a Quick Curbside Consult",
        text:
            "After MRI and CT findings in a stroke patient, is CTA still indicated?",
    },
    {
        section: "Double Check with a Quick Curbside Consult",
        text:
            "In patients with atrial fibrillation and rapid ventricular response where EF is unknown, under what circumstances should diltiazem be avoided?",
    },

    {
        section: "Ask a Pop-Science Question",
        text:
            "Do artificial sweeteners taken long term raise the likelihood of metabolic diseases such as diabetes?",
    },
    {
        section: "Ask a Pop-Science Question",
        text:
            "Are GLP-1 receptor agonists associated with kidney protection in people with diabetes?",
    },
    {
        section: "Ask a Pop-Science Question",
        text:
            "Can adopting a ketogenic diet genuinely improve clinical outcomes?",
    },

    {
        section: "Ask about Treatment Options",
        text:
            "How is chronic heart failure with reduced ejection fraction typically managed?",
    },
    {
        section: "Ask about Treatment Options",
        text:
            "List current therapy options for stage IV non-small-cell lung carcinoma.",
    },
    {
        section: "Ask about Treatment Options",
        text:
            "How should recurrent *C. difficile* infection be managed after several antibiotic courses have failed?",
    },

    {
        section: "Write an Exam Question",
        text:
            "Design an MCQ testing understanding of beta-blockers' mechanisms of action.",
    },
    {
        section: "Write an Exam Question",
        text:
            "Formulate an exam item assessing antibiotic selection for pediatric otitis media.",
    },

    {
        section: "Ask about Treatment Alternatives",
        text:
            "Which antibiotics are suitable for cellulitis in a patient allergic to penicillin, cephalosporins, and Bactrim?",
    },
    {
        section: "Ask about Treatment Alternatives",
        text:
            "What are suitable replacements if metformin causes gastrointestinal intolerance?",
    },
    {
        section: "Ask about Treatment Alternatives",
        text:
            "Should ceftriaxone be avoided in someone with a known penicillin allergy?",
    },

    {
        section: "Ask about Drug Side Effects",
        text: "List the most frequent adverse effects of metformin.",
    },
    {
        section: "Ask about Drug Side Effects",
        text:
            "Are there severe or potentially fatal adverse effects linked to prolonged lisinopril use?",
    },
    {
        section: "Ask about Drug Side Effects",
        text:
            "Summarize common side effects of apixaban, especially in older adults or those with renal impairment.",
    },

    {
        section: "Calculate a Risk Score",
        text: "Compute the anion gap for a patient sample.",
    },
    {
        section: "Calculate a Risk Score",
        text:
            "Estimate the CHA₂DS₂-VASc score for a 72-year-old woman with hypertension, diabetes, and prior stroke.",
    },
    {
        section: "Calculate a Risk Score",
        text: "Determine the BMI of a person who is 6′2″ and weighs 190 lb.",
    },

    {
        section: "Ask for a Table",
        text:
            "Create a table showing how various risk factors contribute to ASCVD risk.",
    },

    {
        section: "Research a Topic",
        text:
            "Summarize recent progress in gene therapy for Duchenne muscular dystrophy.",
    },
    {
        section: "Research a Topic",
        text:
            "Describe Kawasaki disease, including its manifestations and standard treatments.",
    },
    {
        section: "Research a Topic",
        text:
            "Discuss current findings about gut microbiota involvement in autoimmune disorders.",
    },

    {
        section: "Ask about Drug Dosing",
        text:
            "What is the dosing regimen of methotrexate for adults with severe psoriasis?",
    },
    {
        section: "Ask about Drug Dosing",
        text:
            "How should ceftriaxone doses be modified in patients with significant renal dysfunction?",
    },

    {
        section: "Write a Prior Auth Letter",
        text:
            "Draft a prior-authorization request to Cigna for denosumab coverage for osteoporosis.",
    },
    {
        section: "Write a Prior Auth Letter",
        text:
            "Compose a prior-authorization letter to Kaiser requesting physical therapy approval after rotator cuff surgery.",
    },

    {
        section: "Ask for Evidence",
        text:
            "What clinical studies support choline supplementation during pregnancy?",
    },
    {
        section: "Ask for Evidence",
        text:
            "Summarize published data on bleeding risks associated with acalabrutinib.",
    },

    {
        section: "Ask about Guidelines",
        text:
            "Outline current IDSA guidance for treating multidrug-resistant *Pseudomonas* infections.",
    },
    {
        section: "Ask about Guidelines",
        text:
            "Provide a summary of AHA/ACC hypertension guidelines for patients with chronic kidney disease.",
    },
    {
        section: "Ask about Guidelines",
        text:
            "Highlight major updates in the 2024 ADA diabetes management guidelines.",
    },
    {
        section: "Ask about Guidelines",
        text:
            "According to ASCO, what are the current recommendations for immunotherapy use in triple-negative breast cancer?",
    },

    {
        section: "Ask about Primary Evidence",
        text:
            "What major trials underpin metformin's role as first-line therapy for type 2 diabetes?",
    },
    {
        section: "Ask about Primary Evidence",
        text:
            "Which randomized studies support using low-dose aspirin to prevent initial cardiovascular events?",
    },

    {
        section: "Construct a Workup",
        text:
            "Outline the appropriate evaluation for a patient with normal Pap but positive HPV-18.",
    },
    {
        section: "Construct a Workup",
        text: "Describe the diagnostic workup for hypercalciuria.",
    },
    {
        section: "Construct a Workup",
        text:
            "List the laboratory investigations recommended for stage 3b chronic kidney disease.",
    },

    {
        section: "Ask about Drug Interactions",
        text:
            "Identify potential interactions between grapefruit juice and atorvastatin.",
    },
    {
        section: "Ask about Drug Interactions",
        text:
            "Assess possible interactions among ritonavir, rosuvastatin, and apixaban given CYP3A4 inhibition.",
    },

    {
        section: "Ask About Labs to Consider",
        text:
            "Which lab tests are essential in assessing an acute heart-failure exacerbation?",
    },
    {
        section: "Ask About Labs to Consider",
        text:
            "What laboratory workup is indicated for a patient presenting with generalized weakness?",
    },
    {
        section: "Ask About Labs to Consider",
        text:
            "Which labs should be monitored in patients on amlodipine therapy?",
    },

    {
        section: "Write a Patient Handout",
        text:
            "Prepare a patient handout explaining how to control type 2 diabetes through lifestyle modification and medication adherence.",
    },
    {
        section: "Write a Patient Handout",
        text:
            "Write educational material for patients on the purpose and potential side effects of anticoagulants like warfarin.",
    },
    {
        section: "Write a Patient Handout",
        text:
            "Create a patient information sheet on recovery after knee replacement, covering exercises and precautions.",
    },

    {
        section: "Ask a Tough Question",
        text:
            "What factors influence the decision between immunotherapy and targeted therapy for metastatic melanoma with a BRAF mutation?",
    },
    {
        section: "Ask a Tough Question",
        text:
            "How would you optimize heart-failure therapy in a patient with reduced EF, CKD, and recurrent hyperkalemia?",
    },
    {
        section: "Ask a Tough Question",
        text:
            "How should clinicians weigh anticoagulation risks and benefits in an elderly patient with AF, frequent falls, and a recent GI bleed?",
    },
];

// Sample Clinical Case: Complex Heart Failure with Multiple Comorbidities (revised)
export const clinical_case = {
    case_id: "case_heart_failure_2024_001",
    status: ClinicalCaseStatus.COMPLETED,
    title: "Complex Heart Failure with Reduced Ejection Fraction in Elderly Patient with Multiple Comorbidities",

    evidence_snippets: [
        {
            snippet_id: "evid_001",
            text:
                "Create aftercare instructions for a patient discharged after a minor skin surgery. Explain how to care for the wound site, signs of infection to watch for, when they can shower, and when to come back for suture removal.",
            source_id: "clinical_note_001",
            source_type: "clinical_note",
            source_citation: "Emergency Department Clinical Note - Dr. X, MD",
            created_at: "2024-01-15T08:30:00Z",
        },
        {
            snippet_id: "evid_002",
            text:
                "Echocardiogram findings: Left ventricular ejection fraction 25%, severe global hypokinesis, moderate mitral regurgitation, moderate tricuspid regurgitation, estimated pulmonary artery systolic pressure 45 mmHg, left atrial enlargement (LA volume index 45 mL/m²). No pericardial effusion. Right ventricular function mildly reduced.",
            source_id: "echo_001",
            source_type: "diagnostic_test",
            source_citation: "Echocardiogram Report - Dr. X, MD",
            created_at: "2024-01-15T10:15:00Z",
        },
        {
            snippet_id: "evid_003",
            text:
                "Current medications: Metformin 1000mg BID, Lisinopril 10mg daily, Metoprolol succinate 50mg daily, Furosemide 40mg daily, Apixaban 5mg BID, Atorvastatin 40mg daily. Patient reports good adherence to medications. No known drug allergies.",
            source_id: "med_list_001",
            source_type: "medication_list",
            source_citation: "Pharmacy Records - CVS Pharmacy #1234",
            created_at: "2024-01-15T09:00:00Z",
        },
        {
            snippet_id: "evid_004",
            text:
                "2023 AHA/ACC/HFSA Heart Failure Guideline Update: For patients with HFrEF, quadruple therapy with ACE inhibitor/ARB, beta-blocker, MRA, and SGLT2 inhibitor is recommended. SGLT2 inhibitors (dapagliflozin, empagliflozin) are now recommended for all patients with HFrEF regardless of diabetes status. ARNI (sacubitril-valsartan) is preferred over ACE inhibitor for patients with HFrEF who are tolerating ACE inhibitor or ARB therapy.",
            source_id: "10.1161/CIR.0000000000001063",
            source_type: "clinical_guideline",
            source_url:
                "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063",
            source_citation:
                "Heidenreich PA, et al. 2022 AHA/ACC/HFSA Heart Failure Guideline. Circulation. 2022;145:e895-e1032.",
            created_at: "2024-01-15T11:00:00Z",
        },
        {
            snippet_id: "evid_005",
            text:
                "DAPA-HF Trial Results: Dapagliflozin reduced the risk of cardiovascular death or worsening heart failure by 26% (HR 0.74, 95% CI 0.65-0.85, p<0.001) in patients with HFrEF, regardless of diabetes status. The number needed to treat to prevent one primary outcome event was 21 patients over 2.3 years. Safety profile was favorable with no increase in adverse events.",
            source_id: "31535829",
            source_type: "pubmed",
            source_url: "https://pubmed.ncbi.nlm.nih.gov/31535829/",
            source_citation:
                "McMurray JJV, et al. Dapagliflozin in Patients with Heart Failure and Reduced Ejection Fraction. N Engl J Med. 2019;381:1995-2008.",
            created_at: "2024-01-15T11:30:00Z",
        },
        {
            snippet_id: "evid_006",
            text:
                "PARADIGM-HF Trial: Sacubitril-valsartan (ARNI) reduced cardiovascular death or heart failure hospitalization by 20% compared to enalapril (HR 0.80, 95% CI 0.73-0.87, p<0.001) in patients with HFrEF. The benefit was consistent across all subgroups including elderly patients and those with CKD. ARNI was associated with higher rates of hypotension but lower rates of hyperkalemia and renal dysfunction.",
            source_id: "25107801",
            source_type: "pubmed",
            source_url: "https://pubmed.ncbi.nlm.nih.gov/25107801/",
            source_citation:
                "McMurray JJV, et al. Angiotensin-Neprilysin Inhibition versus Enalapril in Heart Failure. N Engl J Med. 2014;371:993-1004.",
            created_at: "2024-01-15T12:00:00Z",
        },
        {
            snippet_id: "evid_007",
            text:
                "Laboratory results from admission: Hemoglobin 11.2 g/dL, hematocrit 33.5%, WBC 8.2 K/μL, platelets 245 K/μL. Comprehensive metabolic panel: glucose 145 mg/dL, BUN 28 mg/dL, creatinine 1.8 mg/dL, eGFR 35 mL/min/1.73m², sodium 138 mEq/L, potassium 4.2 mEq/L, chloride 102 mEq/L, CO2 24 mEq/L, calcium 9.1 mg/dL, phosphorus 3.8 mg/dL, magnesium 1.9 mg/dL. Liver function tests within normal limits.",
            source_id: "labs_001",
            source_type: "laboratory_results",
            source_citation: "Laboratory Results - Quest Diagnostics",
            created_at: "2024-01-15T09:30:00Z",
        },
        {
            snippet_id: "evid_008",
            text:
                "Chest X-ray findings: Cardiomegaly with cardiothoracic ratio of 0.65, bilateral pleural effusions (small to moderate), pulmonary vascular congestion, no acute pulmonary edema. No pneumothorax or pneumonia. Bony structures unremarkable.",
            source_id: "cxr_001",
            source_type: "diagnostic_test",
            source_citation: "Chest X-ray Report - Dr. X, MD",
            created_at: "2024-01-15T09:45:00Z",
        },
        {
            snippet_id: "evid_009",
            text:
                "2024 ADA Standards of Care: For patients with diabetes and heart failure, SGLT2 inhibitors are recommended as first-line therapy for cardiovascular protection. Metformin remains the preferred first-line agent for diabetes management but should be used cautiously in patients with eGFR <30 mL/min/1.73m². Consider dose reduction or discontinuation if eGFR <30.",
            source_id: "ada_2024_guidelines",
            source_type: "clinical_guideline",
            source_url:
                "https://diabetesjournals.org/care/issue/47/Supplement_1",
            source_citation:
                "American Diabetes Association. Standards of Care in Diabetes—2024. Diabetes Care. 2024;47(Suppl. 1):S1-S212.",
            created_at: "2024-01-15T13:00:00Z",
        },
        {
            snippet_id: "evid_010",
            text:
                "Patient's social history: Lives alone in single-story home, independent with ADLs, has home health aide 3x/week for assistance with medication management and transportation. Family history significant for father with MI at age 65, mother with diabetes. Social support from adult daughter who lives 30 minutes away. Patient is a retired engineer, former smoker (quit 15 years ago, 30 pack-year history).",
            source_id: "social_hx_001",
            source_type: "clinical_note",
            source_citation:
                "Social History Assessment - Nurse Practitioner Lisa Wang, NP",
            created_at: "2024-01-15T14:00:00Z",
        },
    ] as EvidenceSnippet[],

    messages: [
        // user
        createEmptyMessage(
            "user_001",
            MessageType.USER,
            "Create aftercare instructions for a patient discharged after a minor skin surgery. Explain how to care for the wound site, signs of infection to watch for, when they can shower, and when to come back for suture removal.",
        ),

        // system + tools (unchanged)
        createEmptyMessage(
            "system_001",
            MessageType.SYSTEM,
            "Analyzing the case...",
            {
                event_name: "agent_thinking",
                agent_id: "cardiology_agent",
                status: "analyzing_case",
            },
            "thinking",
        ),

        createEmptyMessage(
            "system_002",
            MessageType.SYSTEM,
            "Searching published medical literature, guidelines, and more",
            {
                event_name: "tool_calling",
                tool_name: "guideline_search",
                parameters: {
                    query: "heart failure reduced ejection fraction",
                    year: "2023",
                },
            },
            "tooling",
        ),

        // AGENT (add citations)
        createEmptyMessage(
            "system_003",
            MessageType.SYSTEM,
            "Synthesizing relevant information",
            {
                event_name: "agent_synthesizing",
                agent_id: "cardiology_agent",
                status: "synthesizing_case",
            },
            "planning",
        ),

        // createEmptyMessage(
        //     "system_002",
        //     MessageType.SYSTEM,
        //     "",
        //     {
        //         event_name: "tool_calling",
        //         tool_name: "guideline_search",
        //         parameters: {
        //             condition: "heart_failure_reduced_ef",
        //             year: "2023",
        //         },
        //     },
        //     "tooling",
        // ),

        // NEW: FINAL answer to the user's first question (explicit, stage: "final")
        createEmptyMessage(
            "msg_final_001",
            MessageType.AGENT,
            `### Minor Skin Surgery Aftercare

**Wound Site Care:**  
  
- Keep the wound clean and covered with a non-adherent, moist dressing for the first 24-48 hours to promote optimal healing and reduce infection risk. Application of a thin layer of petroleum jelly or a similar ointment is recommended to maintain a moist environment.[1][2][3][4]  
  
- Change the dressing daily or if it becomes wet or soiled. Cleanse the wound gently with tap water or saline; antiseptic solutions are not required for routine care.[5][1][2][4]  
  
- Avoid trauma or excessive movement at the wound site.  
  
**Signs of Infection to Monitor:**  
  
- Watch for increasing redness, swelling, warmth, pain, purulent discharge, or fever. The Infectious Diseases Society of America defines surgical site infection as the presence of purulent drainage, positive wound cultures, or local signs such as pain, swelling, and erythema.[6]  
  
- If any of these signs develop, seek prompt medical evaluation.  
  
**Showering Recommendations:**  
  
- Showering is permitted as early as 6-12 hours after surgery, as multiple randomized trials and meta-analyses show no increased risk of infection or complications with early water exposure.[7][8][9]  
  
- When showering, allow water to run gently over the wound. Avoid soaking (e.g., baths, swimming) until sutures are removed and the wound is fully healed.[5][10][8]  
  
- After showering, gently pat the area dry and reapply a clean dressing.  
  
**Suture Removal:**  
  
- Return for suture removal as advised, typically:  
  
- Face: **5-7 days**  
  
- Scalp: **7-10 days**  
  
- Trunk and upper extremities: **7-14 days**  
  
- Lower extremities: **10-14 days**  
  
These intervals are based on expert consensus and clinical experience.[4]  
  
- Adhere to the specific timeline provided at discharge, as wound location and patient factors may influence timing.  
  
**Additional Instructions:**  
  
- Minimize strenuous activity or stretching of the wound area until sutures are removed.  
  
- Protect the wound from sun exposure to optimize cosmetic outcomes.[11][3]  
  
- Ensure tetanus immunization is up to date if indicated.[1][4]  
  
### References

1. Current Management of Acute Cutaneous Wounds. Singer AJ, Dagum AB. The New England Journal of Medicine. 2008;359(10):1037-46. doi:10.1056/NEJMra0707253.
2. Management of Minor Acute Cutaneous Wounds: Importance of Wound Healing in a Moist Environment. Korting HC, Schöllmann C, White RJ. Journal of the European Academy of Dermatology and Venereology : JEADV. 2011;25(2):130-7. doi:10.1111/j.1468-3083.2010.03775.x.
3. Wound Care Practices Following in-Office Cutaneous Surgery Among Family Physicians in Canada. Sander M, Rebner B, Wiens R, et al. Journal of Wound Care. 2024;33(Sup5):S14-S21. doi:10.12968/jowc.2024.33.Sup5.S14.
4. Laceration Repair: A Practical Approach. Forsch RT, Little SH, Williams C. American Family Physician. 2017;95(10):628-636.
5. Common Questions About Wound Care. Worster B, Zawora MQ, Hsieh C. American Family Physician. 2015;91(2):86-92.
6. Practice Guidelines for the Diagnosis and Management of Skin and Soft Tissue Infections: 2014 Update by the Infectious Diseases Society of America. Stevens DL, Bisno AL, Chambers HF, et al. Clinical Infectious Diseases : An Official Publication of the Infectious Diseases Society of America. 2014;59(2):147-59. doi:10.1093/cid/ciu296.
7. Early Postoperative Water Exposure Does Not Increase Complications in Cutaneous Surgeries: A Randomized, Investigator-Blinded, Controlled Trial. Samaan C, Kim Y, Zhou S, Kirby JS, Cartee TV. Journal of the American Academy of Dermatology. 2024;91(5):896-903. doi:10.1016/j.jaad.2024.05.098.
8. Can Sutures Get Wet? Prospective Randomised Controlled Trial of Wound Management in General Practice. Heal C, Buettner P, Raasch B, et al. BMJ (Clinical Research Ed.). 2006;332(7549):1053-6. doi:10.1136/bmj.38800.628704.AE.
9. Does the Timing of Postoperative Showering Impact Infection Rates? A Systematic Review and Meta-Analysis. Copeland-Halperin LR, Reategui Via Y Rada ML, Levy J, et al. Journal of Plastic, Reconstructive & Aesthetic Surgery : JPRAS. 2020;73(7):1306-1311. doi:10.1016/j.bjps.2020.02.007.
10. Postoperative Showering for Clean and Clean-Contaminated Wounds: A Prospective, Randomized Controlled Trial. Hsieh PY, Chen KY, Chen HY, et al. Annals of Surgery. 2016;263(5):931-6. doi:10.1097/SLA.0000000000001359.
11. Dermatological Postoperative Patient Information Leaflets: Is It Time for More Uniformity?. Hunt WT, McGrath EJ. Clinical and Experimental Dermatology. 2015;40(7):747-52. doi:10.1111/ced.12701.`,
            { agent_name: "Review Agent" },
            "final"
        ),
    ] as Message[],

    created_at: "2024-01-15T08:00:00Z",
    updated_at: "2024-01-15T15:30:00Z",
} as ClinicalCase;
