<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue';
import { useCaseStore } from '../stores/CaseStore';
import type { EvidenceSnippet } from '../models/ClinicalCase';

const case_store = useCaseStore();
const evidence_snippet = ref<EvidenceSnippet | null>(null);

const props = defineProps<{
    snippet_id: string;
}>();

const emit = defineEmits<{
    (e: 'click', snippet_id: string): void;
}>();

// Reactive refs
const cite_popup_ref = ref();

const handleMouseEnter = (event: MouseEvent) => {
    cite_popup_ref.value.show(event);

    // get the evidence snippet from the case store
    const ev = case_store.evidence_dict[props.snippet_id];
    evidence_snippet.value = ev;
};

let hide_overlay_panel_timeout:number | undefined;
const handleMouseLeave = () => {
    if (hide_overlay_panel_timeout) {
        clearTimeout(hide_overlay_panel_timeout);
    }
    hide_overlay_panel_timeout = setTimeout(() => {
        cite_popup_ref.value.hide();
    }, 500);
};

const handleMouseEnterOverlayPanel = (event: MouseEvent) => {
    clearTimeout(hide_overlay_panel_timeout);
    cite_popup_ref.value.show(event);
};

const handleMouseLeaveOverlayPanel = () => {
    if (hide_overlay_panel_timeout) {
        clearTimeout(hide_overlay_panel_timeout);
    }
    cite_popup_ref.value.hide();
};

const shortenText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) {
        return text;
    }
    return text.slice(0, maxLength) + '...';
};
</script>

<template>
<span class="cite-tag cursor-pointer text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-600" 
    @click="emit('click', snippet_id)"
    @mouseenter="handleMouseEnter($event)"
    @mouseleave="handleMouseLeave">
    <font-awesome-icon icon="fa-solid fa-link" />
    {{ case_store.evidence_dict[props.snippet_id].index + 1 }}
</span>


<!-- Cite Popup -->
<Popover ref="cite_popup_ref" 
    @mouseenter="handleMouseEnterOverlayPanel($event)"
    @mouseleave="handleMouseLeaveOverlayPanel"
    class="cite-popup">
<div class="p-3 max-w-sm flex flex-col gap-2">
    <div class="font-medium">
        <font-awesome-icon icon="fa-solid fa-link" />
        {{ evidence_snippet?.source_type }}
        {{ evidence_snippet?.source_id }}
    </div>
    <div class="text-sm">
        {{ shortenText(evidence_snippet?.text || '', 100) }}
    </div>

    <div class="text-sm">
        <font-awesome-icon icon="fa-regular fa-clock" />
        {{ evidence_snippet?.created_at }}
    </div>
</div>
</Popover>
</template>


<style scoped>
.cite-tag {
    transition: color 0.2s ease;
    background-color: var(--highlight-background-color);
    cursor: pointer;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    margin-right: 0.25rem;
    padding: 0 0.25rem;
}
</style>
