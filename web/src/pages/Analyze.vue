<script setup lang="ts">
import { useDataStore } from '../stores/DataStore';
import LeftSidebar from '../components/LeftSidebar.vue';
import { MessageType } from '../models/ClinicalCase';
import type { Message } from '../models/ClinicalCase';
const data_store = useDataStore();


</script>

<template>
<LeftSidebar />
<div class="main-container">
<TopMenu />
<div class="main-content flex flex-row items-center justify-center">
    <div class="w-1/2">
        <div class="flex flex-col items-center justify-center">
            
        </div>
    </div>
    <div class="w-1/2">
        <div class="flex flex-col items-center justify-center">
            <h1>Analyze</h1>
        </div>
    </div>
</div>
</div>
</template>

<style scoped>
</style>