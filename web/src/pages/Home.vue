<script setup lang="ts">
import { ref } from "vue";
import Aurora from '../components/backgrounds/Aurora.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

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
<div class="bg-container">
    <Aurora
        :color-stops="['#bcdefb', '#ffe666', '#e0b3ff']"
        :amplitude="1.0"
        :blend="0.5"
        :speed="1.0"
        :intensity="1.0"
        class="w-full h-full"
    />
</div>
<div class="main">

    <div class="absolute top-0 left-0 w-full h-16">
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


    <div class="bg-surface-0 dark:bg-surface-950 px-6 py-20 md:px-12 lg:px-20 flex items-center justify-center min-h-[500px]">
        <div class="text-surface-700 dark:text-surface-100 text-center flex flex-col items-center gap-4">
            <img src="/logo.svg" alt="OpenMDX" class="w-24 h-24" />
            <div class="text-surface-900 dark:text-surface-0 font-bold text-6xl leading-tight">
                OpenMDX
            </div>
            <div class="text-surface-700 dark:text-surface-100 text-xl leading-normal">
                Transforming Clinical Questions into Diagnostic Insights
            </div>
            
        </div>
    </div>
</div>
</template>

<style scoped>
.bg-container {
    position: absolute !important;
    z-index: 0;
    top: 0;
    left: 0;
    width: 100%;
    height: 500px;
    position: relative;
    overflow: hidden;
}
.main {
    position: relative;
    z-index: 10;
    background: transparent;
}
</style>
