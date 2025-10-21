<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useDataStore } from '../stores/DataStore';
import { useCaseStore } from '../stores/CaseStore';
import LeftSidebar from '../components/LeftSidebar.vue';
import TopMenu from '../components/TopMenu.vue';
import { MessageType } from '../models/ClinicalCase';
import type { Message } from '../models/ClinicalCase';

// PrimeVue components
import Menubar from 'primevue/menubar';
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';
import ToggleButton from 'primevue/togglebutton';
import Rating from 'primevue/rating';
import OverlayPanel from 'primevue/overlaypanel';

const data_store = useDataStore();
const case_store = useCaseStore();

// Reactive refs
const cite_popup_ref = ref();
const cite_content = ref('');

// Computed properties
const clinical_case = computed(() => data_store.c3);
const messages = computed(() => case_store.messages);
const evidence_snippets = computed(() => case_store.evidence_snippets);
const current_evidence = computed(() => case_store.current_evidence);
const evidence_count = computed(() => case_store.evidence_count);

// Chat toolbar items
const chat_toolbar_items = computed(() => [
    // {
    //     label: 'Copy',
    //     icon: 'pi pi-copy',
    //     command: () => case_store.copyChatHistory()
    // },
    {
        label: 'Export',
        icon: 'pi pi-download',
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
]);

// Evidence toolbar items
const evidence_toolbar_items = computed(() => [
    {
        label: 'Export',
        icon: 'pi pi-download',
        command: () => case_store.exportEvidence()
    },
    {
        label: 'More',
        items: [
            { label: 'View All', icon: 'pi pi-list' },
            { label: 'Search', icon: 'pi pi-search' },
            { label: 'Filter', icon: 'pi pi-filter' }
        ]
    }
]);

// Methods
const handleSubmitMessage = () => {
    if (case_store.input_text.trim()) {
        const new_message: Message = {
            message_id: `msg_${Date.now()}`,
            from_id: 'user_001',
            message_type: MessageType.USER,
            text: case_store.input_text,
            created_at: new Date().toISOString()
        };
        case_store.addMessage(new_message);
        case_store.setInputText('');
    }
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const handleCiteHover = (event: Event, content: string) => {
    cite_content.value = content;
    cite_popup_ref.value.show(event);
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const handleCiteLeave = () => {
    cite_popup_ref.value.hide();
};

const handleEvidenceTabChange = (index: number) => {
    case_store.setCurrentEvidenceTab(index);
};

const formatMessageText = (text: string) => {
    // Parse cite tags and create interactive elements
    return text.replace(/<cite>(.*?)<\/cite>/g, (_, content) => {
        return `<span class="cite-tag" @mouseenter="handleCiteHover($event, '${content}')" @mouseleave="handleCiteLeave">${content}</span>`;
    });
};

const keyword = ref('');

// Initialize case data
onMounted(() => {
    if (clinical_case.value) {
        case_store.setClinicalCase(clinical_case.value);
    }
});
</script>

<template>
<LeftSidebar />
<div class="main-container">
    <div class="main-content flex flex-row h-screen">

        <Splitter style="height: 100svh; border: 0;">
            
        <!-- Chat Panel -->
        <SplitterPanel class="flex flex-col" :size="45" :minSize="30">
            <!-- Chat Header -->
            <div class="chat-header h-12 flex items-center justify-between pl-4 border-b">
                <div class="flex items-center gap-2">
                    <span class="font-semibold">
                        Analyzer
                    </span>

                    <input type="text" 
                        v-model="keyword" 
                        placeholder="Filter messages by keyword" 
                        style="padding-right: 2rem;"
                        class="p-1 border-1" />

                    <Button icon="pi pi-times" size="small" class="p-button-text" text
                        style="margin-left: -2.5rem" />
                </div>
                <div class="flex items-center gap-2">

                    <ToggleSwitch 
                        id="show_thinking"
                        v-model="case_store.show_thinking" 
                        onLabel="Thinking" 
                        offLabel="Thinking"
                        class="text-xs" />

                    <label for="show_thinking">
                        Thinking
                    </label>
                    
                    <Menubar :model="chat_toolbar_items" 
                        style="border: none; background: transparent;"
                        class="p-0" />

                    <Button type="button" icon="pi pi-ellipsis-v" @click="toggle" aria-haspopup="true" aria-controls="overlay_menu" />
                    <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
                    <!-- <ToggleButton 
                        v-model="case_store.show_thinking" 
                        onLabel="Thinking" 
                        offLabel="Thinking"
                        class="text-xs"
                        @change="case_store.toggleThinking"
                    /> -->
                    <!-- <Rating v-model="case_store.chat_rating" :stars="5" class="text-sm" /> -->
                </div>
            </div>

            <!-- Chat Body -->
            <div class="chat-body flex-1 overflow-y-auto p-4 space-y-4">
                <template v-for="message in messages" :key="message.message_id">
                    <div v-if="['USER', 'AGENT', 'TOOL'].includes(message.message_type)"
                        class="message-item hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md p-2" 
                        :class="{ 'user-message': message.message_type === 'USER', 
                        'system-message': message.message_type !== 'USER' }">
                    
                        <div class="message-header flex justify-between items-center gap-2">
                            <div class="flex items-center gap-2">
                                <span class="font-medium text-sm">
                                    {{ message.message_type === 'USER' ? 'User' : 
                                    message.message_type === 'AGENT' ? 'Agent' : 
                                    message.message_type === 'TOOL' ? 'Tool' : 'System' }}
                                </span>
                                <span class="text-xs text-gray-500">{{ new Date(message.created_at).toLocaleTimeString() }}</span>
                            </div>
                            
                            <!-- System message toolbar -->
                            <div v-if="message.message_type !== 'USER'" class="message-toolbar mt-2 flex gap-2">
                                <Button size="small" icon="pi pi-thumbs-up" class="p-button-text p-button-sm" />
                                <Button size="small" icon="pi pi-thumbs-down" class="p-button-text p-button-sm" />
                                <Button size="small" icon="pi pi-copy" class="p-button-text p-button-sm" />
                            </div>
                        </div>
                        
                        <div class="message-content" v-html="formatMessageText(message.text || '')"></div>
                    </div>
                </template>
            </div>

            <!-- Chat Footer -->
            <div class="chat-footer border-t pl-4 pr-2 py-2">
                <div class="flex flex-col gap-2">
                    <!-- Input area -->
                    <Textarea 
                        v-model="case_store.input_text"
                        placeholder="Type your follow-up question here..."
                        :auto-resize="true"
                        rows="1"
                        style="max-height: 10rem;"
                        class="w-full"
                        @keydown.enter.prevent="handleSubmitMessage"
                    />
                    
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
                                @click="case_store.toggleRecording"
                            />
                            <Button 
                                icon="pi pi-send" 
                                size="small" 
                                @click="handleSubmitMessage"
                            />
                        </div>
                    </div>
                </div>
            </div>
        
        </SplitterPanel>


        <!-- Evidence Panel -->
        <SplitterPanel class="flex flex-col" :size="55" :minSize="30">
            <!-- Evidence Header -->
            <div class="evidence-header h-12 flex items-center justify-between pl-4 border-b"
                style="border-color: var(--border-color);">
                <div class="flex items-center gap-2">
                    <i class="pi pi-book"></i>
                    <span class="font-semibold">
                        Evidence
                    </span>
                    <span class="text-sm text-gray-500">({{ evidence_count }} pieces)</span>
                </div>
                <div class="flex items-center gap-2">
                    <Menubar :model="evidence_toolbar_items" 
                        style="border: none; background: transparent;"
                        class="p-0" />
                </div>
            </div>

            <!-- Evidence Body -->
            <div class="evidence-body flex-1 flex">
                <!-- Evidence Tabs (Left 1/4) -->
                <div class="w-1/4 border-r overflow-x-hidden bg-gray-50 pl-2"
                    style="overflow-y: auto; height: calc(100svh - 3rem);">
                    <div v-for="(snippet, index) in evidence_snippets" :key="snippet.snippet_id"
                        class="evidence-tab p-2 rounded hover:bg-white dark:hover:bg-gray-700 border-btransition-colors"
                        :class="{ 'bg-white dark:bg-gray-800 shadow-sm': index === case_store.current_evidence_tab }"
                        @click="handleEvidenceTabChange(index)">
                        <div class="flex items-center gap-2">
                            <template v-if="['pubmed', 'pmc', 'doi', 'webpage'].includes(snippet.source_type)">
                                <font-awesome-icon icon="fa-solid fa-globe" />
                                <span class="text-sm font-medium truncate">
                                    {{ snippet.source_type }}
                                </span>

                                <span class="text-sm font-medium truncate">
                                    {{ snippet.source_id }}
                                </span>

                            </template>

                            <template v-else>
                                <font-awesome-icon icon="fa-solid fa-file-lines" />

                                <span class="text-sm font-medium truncate">
                                    {{ snippet.source_type.replace('_', ' ').toUpperCase() }}
                                </span>
                            </template>
                        </div>


                        <div class="text-xs text-gray-500 mt-1 truncate">
                            {{ snippet.text.substring(0, 50) }}...
                        </div>
                    </div>
                </div>

                <!-- Evidence Detail (Right 3/4) -->
                <div class="w-3/4 p-4 overflow-y-auto">
                    <div v-if="current_evidence" class="evidence-detail">
                        <div class="evidence-header mb-4">
                            <h3 class="text-lg font-semibold mb-2">{{ current_evidence.source_type.replace('_', ' ').toUpperCase() }}</h3>
                            <div class="text-sm text-gray-600 mb-2">
                                <span class="font-medium">Source:</span> {{ current_evidence.source_citation }}
                            </div>
                            <div v-if="current_evidence.source_url" class="text-sm text-blue-600 mb-2">
                                <a :href="current_evidence.source_url" target="_blank" class="hover:underline">
                                    {{ current_evidence.source_url }}
                                </a>
                            </div>
                        </div>
                        
                        <div class="evidence-content">
                            <div class="prose max-w-none">
                                <p class="whitespace-pre-wrap">{{ current_evidence.text }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <div v-else class="flex items-center justify-center h-full">
                        <div class="text-center">
                            <i class="pi pi-book text-4xl mb-4"></i>
                            <p>No evidence selected</p>
                        </div>
                    </div>
                </div>
            </div>
        </SplitterPanel>
        </Splitter>
    </div>
</div>

<!-- Cite Popup -->
<OverlayPanel ref="cite_popup_ref" class="cite-popup">
    <div class="p-3 max-w-sm">
        <div class="text-sm">{{ cite_content }}</div>
    </div>
</OverlayPanel>
</template>

<style scoped>
.main-container {
    height: 100vh;
    overflow: hidden;
}

.main-content {
    height: calc(100svh - 3rem); /* Adjust for TopMenu height */
}

.chat-body {
    scrollbar-width: thin;
}

.evidence-body {
    scrollbar-width: thin;
}

.message-item {
    padding: 0.5rem;
    margin-bottom: 0.5rem;
}
.message-header {
    height: 2rem;
}
.message-toolbar {
    display: none;
}
.message-item:hover .message-toolbar {
    display: inline-block;
}

.cite-tag {
    background-color: var(--highlight-background-color);
    color: #92400e;
    padding: 0.125rem 0.25rem;
    border-radius: 0.25rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.cite-tag:hover {
    background-color: #fde68a;
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