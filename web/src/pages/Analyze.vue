<script setup lang="ts">
import { useDataStore } from '../stores/DataStore';
import LeftSidebar from '../components/LeftSidebar.vue';
const data_store = useDataStore();

</script>

<template>
<LeftSidebar />
<div class="main-container">
    

    <TopMenu />
    <div class="main-content flex flex-col items-center justify-center">
        <h1>Analyze</h1>
    </div>
</div>
</template>

<style scoped>
</style>