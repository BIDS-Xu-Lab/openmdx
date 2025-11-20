<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useDataStore } from '../stores/DataStore';
import { useCaseStore } from '../stores/CaseStore';
import LeftSidebar from '../components/LeftSidebar.vue';
import { MessageType } from '../models/ClinicalCase';
import type { Message } from '../models/ClinicalCase';
import { marked } from 'marked';
import { useToast } from 'primevue/usetoast';
import { clinical_cases as sample_clinical_cases } from '../models/Samples';

const toast = useToast();

// PrimeVue components
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';

const data_store = useDataStore();
const case_store = useCaseStore();

// Computed properties
const evidence_snippets = computed(() => case_store.evidence_snippets);
const current_evidence = computed(() => case_store.current_evidence);
const evidence_count = computed(() => case_store.evidence_count);

// Chat toolbar items
const chat_toolbar_items = [
    {
        icon: 'pi pi-download',
        label: 'Export as JSON',
        command: () => case_store.exportChatHistory()
    },
    {
        label: 'More',
        items: [
            { label: 'View All', icon: 'pi pi-list' },
            { label: 'Search', icon: 'pi pi-search' },
            { label: 'Filter', icon: 'pi pi-filter' }
        ]
    }
];

const chat_toolbar_menu_ref = ref();
const toggleChatToolbarMenu = (event: Event) => {
    chat_toolbar_menu_ref.value.toggle(event);
};

// Evidence toolbar items
const evidence_toolbar_menu_ref = ref();
const evidence_toolbar_items = [
    {
        label: 'Download All Evidence',
        items: [
            { label: 'As a JSON file', icon: 'pi pi-list', command: () => case_store.exportEvidence() },
        ]
    }
];

const toggleEvidenceToolbarMenu = (event: Event) => {
    evidence_toolbar_menu_ref.value.toggle(event);
};

// Methods
const handleSubmitMessage = () => {
    if (case_store.input_text.trim()) {
        const new_message: Message = {
            message_id: `msg_${Date.now()}`,
            from_id: 'user_001',
            message_type: MessageType.USER,
            text: case_store.input_text,
            created_at: new Date().toISOString(),
            stage: 'input'
        };
        case_store.addMessage(new_message);
        case_store.setInputText('');
    }
};

const handleEvidenceTabChange = (snippet_id: string) => {
    case_store.setCurrentEvidenceTab(snippet_id);
};

const renderMessageText = (text: string) => {
    let html = marked.parse(text);

    // second, highlight the keywords in the text
    const keywords = case_store.filter_keywords;
    if (keywords.length > 0) {
        for (const keyword of keywords) {
            html = (html as string).replace(new RegExp(`(${keyword})`, 'gi'), '<span class="highlight-keyword">$1</span>');
        }
    }

    return html;
};


const cite_popup_ref = ref();
const handleMouseEnterOverlayPanel = () => {
    console.log('handleMouseEnterOverlayPanel');
    case_store.clearHideHoveredSnippetTimeout();
};

const handleMouseLeaveOverlayPanel = () => {
    console.log('handleMouseLeaveOverlayPanel');
    case_store.hideHoveredSnippet(true);
};


const shortenText = (text: string, maxLength: number) => {
    if (text.length <= maxLength) {
        return text;
    }
    return text.slice(0, maxLength) + '...';
};

const copyMessageToClipboard = (message: Message) => {
    navigator.clipboard.writeText(message.text || '');

    toast.add({
        severity: 'info',
        summary: 'Copied to clipboard',
        detail: 'The answer has been copied to your clipboard',
        life: 3000
    });
};

const togglePlaceholderDetails = () => {
    console.log('togglePlaceholderDetails');
    case_store.show_thinking = !case_store.show_thinking;
};

// Initialize case data
onMounted(() => {
    if (case_store.clinical_case == null) {
        case_store.setClinicalCase(sample_clinical_cases[0]!);
    }

    case_store.cite_popup_ref = cite_popup_ref.value;
});
</script>

<template>
<LeftSidebar />
<div class="main-container flex flex-col h-screen">


<TopMenu />

<div class="main-content">

    <!-- Chat Body -->
    <div class="chat-body flex-1 overflow-y-auto p-4 w-full">
        <template v-for="message in case_store.filterRenderedMessages()" :key="message.message_id">
            <div v-if="['USER'].includes(message.message_type)"
                class="message-item user-message ">
                <div class="message-header flex justify-between items-center gap-2">
                    <div class="flex items-center gap-2">
                        <span class="font-medium text-sm">
                            <font-awesome-icon icon="fa-solid fa-user" />
                        </span>
                        <span class="text-xs">
                            {{ new Date(message.created_at).toLocaleTimeString() }}
                        </span>
                    </div>
                </div>
                
                <div class="message-content prose max-w-none text-base/6"
                    v-html="renderMessageText(message.text || '')" 
                    v-cite>
                </div>
            </div>

            <div v-else-if="['AGENT'].includes(message.message_type) && (case_store.show_thinking && message.stage !== 'final')"
                class="message-item agent-message " >
                <div class="message-header message-header-on-timeline p-2 flex justify-between items-center gap-2">
                    <div class="flex items-center gap-2">
                        <span class="role-icon font-medium text-sm">
                            <font-awesome-icon icon="fa-solid fa-robot" />
                        </span>
                        <span>
                            {{ message.payload_json?.agent_name }}
                        </span>
                        <span class="text-xs">
                            {{ new Date(message.created_at).toLocaleTimeString() }}
                        </span>
                    </div>
                    
                    <!-- System message toolbar -->
                    <div class="message-toolbar mt-2 flex gap-2">
                        <Button size="small" icon="pi pi-thumbs-up" class="p-button-text p-button-sm" />
                        <Button size="small" icon="pi pi-thumbs-down" class="p-button-text p-button-sm" />
                        <Button size="small" icon="pi pi-copy"  
                            class="p-button-text p-button-sm"
                            @click="copyMessageToClipboard(message)" />
                    </div>
                </div>
                
                <div class="message-content p-2 prose max-w-none text-base/6 text-sm"
                    v-html="renderMessageText(message.text || '')" 
                    v-cite>
                </div>
            </div>

            <div v-else-if="['AGENT'].includes(message.message_type) && message.stage == 'final'"
                class="message-item border rounded-lg" >
                <div class="message-header rounded-t-lg flex justify-between items-center gap-2 px-4 py-2 !h-12 bg-gray-100 dark:bg-gray-900 border-b">
                    <div class="flex items-center gap-2">
                        <span class="font-medium text-sm">
                            <font-awesome-icon icon="fa-solid fa-check-circle" />
                        </span>
                        <span>
                            Results Summary
                        </span>
                    </div>
                    
                    <!-- System message toolbar -->
                    <div class="message-toolbar mt-2 flex gap-2">
                        <Button size="small" icon="pi pi-thumbs-up" class="p-button-text p-button-sm" />
                        <Button size="small" icon="pi pi-thumbs-down" class="p-button-text p-button-sm" />
                        <Button size="small" icon="pi pi-copy"      
                            @click="copyMessageToClipboard(message)"
                            class="p-button-text p-button-sm" />
                    </div>
                </div>
                
                <div class="message-content prose max-w-none text-base/6 p-4"
                    v-html="renderMessageText(message.text || '')" 
                    v-cite>
                </div>
            </div>
            

            <div v-else-if="['PLACEHOLDER'].includes(message.message_type)"
                class="message-item placeholder-message " >
                <div class="message-content italic text-center">
                    <font-awesome-icon icon="fa-regular fa-clock" />
                    {{ message.text }}

                    <span class="text-sm cursor-pointer" @click="togglePlaceholderDetails">
                        (view details)
                    </span>
                </div>
            </div>


            <div v-else-if="['SYSTEM'].includes(message.message_type) && (case_store.show_thinking)"
                class="message-item tool-message " >
                <div class="message-header message-header-on-timeline p-2 flex justify-between items-center gap-2">
                    <div class="flex items-center gap-2">
                        <span class="role-icon font-medium text-sm">
                            <font-awesome-icon icon="fa-solid fa-circle-nodes" />
                        </span>
                        <div class="flex flex-col">
                            <span class="text-xs">
                                {{ message.payload_json?.agent_name }}
                            </span>
                            <span class="italic">
                                {{ message.text }}
                            </span>
                        </div>
                    </div>
                    
                    <!-- System message toolbar -->
                    <div class="message-toolbar mt-2 flex gap-2">
                        
                    </div>
                </div>
            </div>


            <div v-else-if="['TOOL'].includes(message.message_type) && (message.stage == 'final' || case_store.show_thinking)"
                class="message-item tool-message " >
                <div class="message-header message-header-on-timeline p-2 flex justify-between items-center gap-2">
                    <div class="flex items-center gap-2">
                        <span class="role-icon font-medium text-sm">
                            <font-awesome-icon icon="fa-solid fa-screwdriver-wrench" />
                        </span>
                        <span class="italic">
                            {{ message.payload_json?.tool_name }}
                        </span>
                        <span class="text-xs">
                            {{ new Date(message.created_at).toLocaleTimeString() }}
                        </span>
                    </div>
                    
                    <!-- System message toolbar -->
                    <div class="message-toolbar mt-2 flex gap-2">
                        <Button size="small" icon="pi pi-thumbs-up" class="p-button-text p-button-sm" />
                        <Button size="small" icon="pi pi-thumbs-down" class="p-button-text p-button-sm" />
                        <Button size="small" icon="pi pi-copy" 
                            class="p-button-text p-button-sm"
                            @click="copyMessageToClipboard(message)" />
                    </div>
                </div>
                
                <div class="message-content text-sm p-2"
                    v-html="renderMessageText(message.text || '')" 
                    v-cite>
                </div>

                <div class="flex flex-row gap-2 pt-2 mt-2 p-2">
                    <div v-for="parameter_key in Object.keys(message.payload_json?.tool_parameters)" :key="parameter_key"
                        class="flex flex-col">
                        <span class="text-xs">
                            {{ parameter_key }}
                        </span>
                        <span class="text-sm">
                            {{ message.payload_json?.tool_parameters[parameter_key] }}
                        </span>
                    </div>
                </div>
            </div>
        </template>

        <div v-if="case_store.filterRenderedMessages().length === 0"
            class="message-item user-message ">                    
            <div class="message-content prose max-w-none text-base/6">
                <p>
                    No messages found for the given keywords in any of the processing steps. Please try other keywords or clear the filter.
                </p>
            </div>
        </div>
    </div>

    <!-- Chat Footer -->
    <div class="chat-footer w-full border-t pl-4 pr-2 py-4">
        <div class="flex flex-col gap-2">
            <!-- Input area -->
            <Textarea 
                v-model="case_store.input_text"
                placeholder="Type your follow-up question here..."
                :auto-resize="true"
                rows="1"
                style="max-height: 10rem;"
                class="w-full"
                @keydown.enter.prevent="handleSubmitMessage" />
            
            <!-- Action buttons -->
            <div class="flex justify-between items-center">
                <div class="flex gap-2">
                    <Button icon="pi pi-upload" size="small" class="p-button-text" />
                    <Button icon="pi pi-search" size="small" class="p-button-text" />
                </div>
                <div class="flex gap-2">
                    <Button 
                        icon="pi pi-microphone" 
                        size="small" 
                        :class="{ 'p-button-warning': case_store.is_recording }"
                        @click="case_store.toggleRecording" />
                    <Button 
                        icon="pi pi-send" 
                        size="small" 
                        @click="handleSubmitMessage" />
                </div>
            </div>
        </div>
    </div>

</div>

</div>





<!-- Cite Popup -->
<Popover ref="cite_popup_ref" 
    @mouseenter="handleMouseEnterOverlayPanel"
    @mouseleave="handleMouseLeaveOverlayPanel"
    class="cite-popup shadow-sm">
<div class="p-3 max-w-sm flex flex-col gap-2">
    <div class="font-medium">
        {{ case_store.current_hovered_evidence?.source_type }}
        {{ case_store.current_hovered_evidence?.source_id }}
    </div>
    <div class="text-sm">
        {{ shortenText(case_store.current_hovered_evidence?.text || '', 100) }}
    </div>

    <div class="text-sm">
        {{ case_store.current_hovered_evidence?.created_at }}
    </div>
</div>
</Popover>


</template>

<style scoped>
.main-container {
}

.main-content {
    min-width: 30rem;
    max-width: 60rem;
    width: auto;
    margin: 0 auto;
    height: calc(100svh - 3rem); /* Adjust for TopMenu height */
}

.chat-body {
    padding-bottom: 8rem;
}

.chat-footer {
    max-width: 60rem;
    position: fixed;
    bottom: 0;
    background-color: var(--background-color);
}

.evidence-body {
    scrollbar-width: thin;
}

.message-item {
    display: flex;
    flex-direction: column;
    padding-bottom: 1rem;
}
.message-header {
    height: 2rem;
}
.message-header-on-timeline {
    margin-left: -1.3rem;
}
.message-toolbar {
    display: none;
}
.message-item:hover .message-toolbar {
    display: inline-block;
}

.role-icon {
    background-color: var(--border-color);
    padding: 0.25rem;
    border-radius: 0.25rem;
}
.user-message {
    margin-bottom: 2rem;
    border-bottom: 2px solid var(--border-color);
}
.tool-message {
    margin-left: 1rem;
    border-left: 2px solid var(--border-color);
}

.agent-message {
    margin-left: 1rem;
    border-left: 2px solid var(--border-color);
}

.evidence-tab {
    transition: all 0.2s;
    cursor: pointer;
}

.evidence-tab:hover {
    transform: translateX(0.25rem);
}

.cite-popup {
    border: 1px solid var(--border-color);
}

/* Custom scrollbar */
.chat-body::-webkit-scrollbar,
.evidence-body::-webkit-scrollbar {
    width: 6px;
}

.chat-body::-webkit-scrollbar-track,
.evidence-body::-webkit-scrollbar-track {
    background-color: var(--background-color);
}

.chat-body::-webkit-scrollbar-thumb,
.evidence-body::-webkit-scrollbar-thumb {
    background-color: var(--border-color);
    border-radius: 9999px;
}

.chat-body::-webkit-scrollbar-thumb:hover,
.evidence-body::-webkit-scrollbar-thumb:hover {
    background-color: #9ca3af;
}
</style>