<script setup lang="ts">
import { ref } from "vue";
import Aurora from '../components/backgrounds/Aurora.vue';
import { useRouter } from 'vue-router';
import { useDataStore } from '../stores/DataStore';
import CaseInputArea from '../components/CaseInputArea.vue';

const router = useRouter();
const data_store = useDataStore();

const items = ref([
{
    label: 'Company',
    root: true,
    items: [
        [
            {
                items: [
                    { label: 'Features', icon: 'pi pi-list', subtext: 'Subtext of item' },
                    { label: 'Customers', icon: 'pi pi-users', subtext: 'Subtext of item' },
                    { label: 'Case Studies', icon: 'pi pi-file', subtext: 'Subtext of item' }
                ]
            }
        ],
        [
            {
                items: [
                    { label: 'Solutions', icon: 'pi pi-shield', subtext: 'Subtext of item' },
                    { label: 'Faq', icon: 'pi pi-question', subtext: 'Subtext of item' },
                    { label: 'Library', icon: 'pi pi-search', subtext: 'Subtext of item' }
                ]
            }
        ],
        [
            {
                items: [
                    { label: 'Community', icon: 'pi pi-comments', subtext: 'Subtext of item' },
                    { label: 'Rewards', icon: 'pi pi-star', subtext: 'Subtext of item' },
                    { label: 'Investors', icon: 'pi pi-globe', subtext: 'Subtext of item' }
                ]
            }
        ],
        [
            {
                items: [{ image: 'https://primefaces.org/cdn/primevue/images/uikit/uikit-system.png', label: 'GET STARTED', subtext: 'Build spectacular apps in no time.' }]
            }
        ]
    ]
},
{
    label: 'Resources',
    root: true
},
{
    label: 'Contact',
    root: true
}
]);

const onClickSignIn = () => {
    router.push('/login');
}

</script>

<template>
<div class="main-container">
    <div class="bg-container">
        <Aurora 
            :color-stops="data_store.isDarkMode() ? 
                ['#172d40', '#0f210d', '#2d1b0b'] : 
                ['#bcdefb', '#ffe666', '#e0b3ff']"
            :amplitude="1.0"
            :blend="0.5"
            :speed="1.0"
            :intensity="1.0"
            class="w-full h-full"
        />
    </div>

    <div class="main-menu">
        <MegaMenu :model="items" style="border-radius: 0; border: none; background: transparent;">
            <template #start>
            </template>
            <template #item="{ item }">
                <!-- <a v-if="item.root" class="flex items-center cursor-pointer px-4 py-2 overflow-hidden relative font-semibold text-lg uppercase" style="border-radius: 2rem">
                    <span>{{ item.label }}</span>
                </a>
                <a v-else-if="!item.image" class="flex items-center p-4 cursor-pointer mb-2 gap-3">
                    <span class="inline-flex items-center justify-center rounded-full bg-primary text-primary-contrast w-12 h-12">
                        <i :class="[item.icon, 'text-lg']"></i>
                    </span>
                    <span class="inline-flex flex-col gap-1">
                        <span class="font-bold text-lg">{{ item.label }}</span>
                        <span class="whitespace-nowrap">{{ item.subtext }}</span>
                    </span>
                </a>
                <div v-else class="flex flex-col items-start gap-4 p-2">
                    <img alt="megamenu-demo" :src="item.image" class="w-full" />
                    <span>{{ item.subtext }}</span>
                    <Button :label="item.label" variant="outlined" />
                </div> -->
            </template>
            <template #end>
                <Button size="small" 
                    @click="onClickSignIn"
                    label="Sign In" icon="pi pi-user" />
            </template>
        </MegaMenu>
    </div>


    <div class="main-content flex flex-col items-center justify-center">
        <div class="mt-16 items-center justify-center flex flex-col gap-4">
            <div class="font-bold text-6xl">
                OpenMDX
            </div>
            <div class="text-xl">
                Transforming Clinical Questions into Diagnostic Insights
            </div>
        </div>

        <CaseInputArea />





        <div class="flex flex-col items-center gap-4 mb-4 w-1/2 justify-center mt-4">
            <p class="text-2xl font-bold text-on-line">
                <i />
                <span>
                    Key Features
                </span>
                <i />
            </p>

            <div class="grid grid-cols-1 grid-cols-2 gap-4 text-center">
                <div class="w-full rounded-md p-4">
                    <span class="mb-4 flex h-16 w-16 items-center justify-center rounded-lg shadow mx-auto text-4xl">
                        <font-awesome-icon icon="fa-solid fa-hexagon-nodes" />
                    </span>
                    <div class="flex flex-col gap-1">
                        <div class="text-surface-900 dark:text-surface-0 text-xl font-medium leading-tight">
                            Multi-agent Collaboration
                        </div>
                        <p class="text-surface-500 dark:text-surface-400 leading-normal">
                            Our system is powered by multiple agents that can collaborate to answer your questions.
                        </p>
                    </div>
                </div>
                <div class="w-full rounded-md p-4">
                    <span class="mb-4 flex h-16 w-16 items-center justify-center rounded-lg shadow mx-auto text-4xl">
                        <font-awesome-icon icon="fa-solid fa-book" />
                    </span>
                    <div class="flex flex-col gap-1">
                        <div class="text-surface-900 dark:text-surface-0 text-xl font-medium leading-tight">
                            Clinical Knowledge Base
                        </div>
                        <p class="text-surface-500 dark:text-surface-400 leading-normal">
                            The answer is based on the latest clinical guidelines and biomedical literature.
                        </p>
                    </div>
                </div>
            </div>
        </div>


        <div class="flex flex-col items-center gap-4 mb-4 w-1/2 justify-center mt-4">
            <p class="text-2xl font-bold text-on-line">
                <i />
                <span>
                    Data Platform
                </span>
                <i />
            </p>

            <p class="text-sm text-gray-500">
                Our system is powered by PubMed, PubMed Central, and other public databases.
            </p>
        </div>

    </div>

    <Footer />
</div>
</template>

<style scoped>
.main-container {
    top: 0;
    left: 0;
    z-index: 10;
    width: 100%;
    height: 100vh;
    overflow-y: auto;
    background: transparent;
}
.bg-container {
    position: absolute;
    z-index: 0;
    top: 0;
    left: 0;
    width: 100%;
    height: 400px;
}
.main-menu {
    position: absolute;
    z-index: 20;
    top: 0;
    right: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-end;
}
.main-content {
    position: relative;
    z-index: 10;
    width: 100%;
}
.text-on-line {
    position: relative;
    display: flex;
    grid-row: 1;
    align-items: center;
    justify-content: stretch;
    padding: 0.5rem 2rem;
    width: 100%;
}

.text-on-line > i {
    flex: 1 1;
    border-bottom: 1px solid var(--border-color);
}
.text-on-line > span {
    padding: 0 1rem;
}

.text-on-line::before {
    margin-right: 1.5rem;
}

.text-on-line::after {
    margin-left: 1.5rem;
}
.bg-line {
    width: 100%;
    height: 1px;
    background-color: var(--border-color);
    margin-bottom: 2rem;
    z-index: -1;
}
</style>
