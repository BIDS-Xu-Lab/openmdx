import { defineStore } from 'pinia';

export const useDataStore = defineStore('data', {
    state: () => ({
        current_page: '',
        color_scheme: 'light',
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