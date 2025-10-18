import { defineStore } from 'pinia';

export const useDataStore = defineStore('data', {
    state: () => ({
        current_page: '',
        color_scheme: 'light',

        flag_sidebar_open: false,
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