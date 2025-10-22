import { defineStore } from 'pinia';
import type { ClinicalCase } from '../models/ClinicalCase';
import { clinical_case } from '../models/Samples';

export const useDataStore = defineStore('data', {
    state: () => ({
        current_page: '',
        color_scheme: 'light',

        flag_sidebar_open: false,

        current_clinical_case: clinical_case as ClinicalCase,
    }),

    getters: {
        c3: (state) => state.current_clinical_case,
    },
    
    actions: {
        init() {
            this.updateColorScheme();
        },

        updateColorScheme() {
            const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            if (darkModeMediaQuery.matches) {
                this.color_scheme = 'dark';
            } else {
                this.color_scheme = 'light';
            }
        },

        setCurrentPage(page: string) {
            this.current_page = page;
        },

        isDarkMode() {
            return this.color_scheme === 'dark';
        },

        setClinicalCase(case_data: ClinicalCase) {
            this.current_clinical_case = case_data;
        }
    }
})