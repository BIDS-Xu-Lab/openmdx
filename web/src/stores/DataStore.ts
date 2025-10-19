import { defineStore } from 'pinia';
import type { ClinicalCase } from '../models/ClinicalCase';
export const useDataStore = defineStore('data', {
    state: () => ({
        current_page: '',
        color_scheme: 'light',

        flag_sidebar_open: false,

        current_clinical_case: null as ClinicalCase | null,
    }),
    actions: {
        setCurrentPage(page: string) {
            this.current_page = page;
        },

        isDarkMode() {
            return this.color_scheme === 'dark';
        }
    }
})