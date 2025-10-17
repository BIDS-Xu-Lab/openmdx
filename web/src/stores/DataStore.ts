import { defineStore } from 'pinia';

export const useDataStore = defineStore('data', {
    state: () => ({
        current_page: ''
    }),
    actions: {
        setCurrentPage(page: string) {
            this.current_page = page;
        }
    }
})