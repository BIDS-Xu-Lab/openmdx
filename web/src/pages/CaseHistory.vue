<script setup lang="ts">
import { useDataStore } from '../stores/DataStore';
import { clinical_case } from '../models/Samples';

const data_store = useDataStore();

const cases = [
    clinical_case,
    clinical_case,
    clinical_case,
]

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

const deleteCase = (case_id: string) => {
    console.log('* deleting case', case_id);
}

const exportCase = (case_id: string) => {
    console.log('* exporting case', case_id);
}
</script>

<template>
<LeftSidebar />
<div class="main-container">

    <div class="w-3/4 mx-auto mt-12">
        <h1 class="text-2xl font-bold">Case History</h1>
        <table class="w-full">
            <thead>
            <tr class="h-12 border-b text-left">
                <th class="col-date">
                    Date
                </th>
                <th class="col-title">
                    Title
                </th>
                <th class="col-actions">
                    &nbsp;
                </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="cc in cases" :key="cc.case_id"
                class="h-12 border-b">
                <td class="">
                    {{ formatDate(cc.created_at) }}
                </td>
                <td class="">
                    {{ cc.title }}
                </td>
                <td class="">
                    <Button icon="pi pi-trash" text
                        @click="deleteCase(cc.case_id)"
                        size="small" />
                    <Button icon="pi pi-download" text
                        @click="exportCase(cc.case_id)"
                        size="small" />
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<style scoped>
</style>