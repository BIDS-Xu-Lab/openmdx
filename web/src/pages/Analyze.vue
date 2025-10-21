<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useDataStore } from '../stores/DataStore';
import { useCaseStore } from '../stores/CaseStore';
import LeftSidebar from '../components/LeftSidebar.vue';
import CiteTag from '../components/CiteTag.vue';
import { MessageType } from '../models/ClinicalCase';
import type { Message } from '../models/ClinicalCase';
import { marked } from 'marked';

// PrimeVue components
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';
import OverlayPanel from 'primevue/overlaypanel';

const data_store = useDataStore();
const case_store = useCaseStore();

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

const chat_toolbar_menu_ref = ref();
const toggleChatToolbarMenu = (event: Event) => {
    chat_toolbar_menu_ref.value.toggle(event);
};

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
            created_at: new Date().toISOString(),
            stage: 'input'
        };
        case_store.addMessage(new_message);
        case_store.setInputText('');
    }
};

const handleCiteClick = (snippet_id: string) => {
    case_store.setCurrentEvidenceTab(snippet_id);
};

const handleEvidenceTabChange = (snippet_id: string) => {
    case_store.setCurrentEvidenceTab(snippet_id);
};

const parseMessageText = (text: string) => {
    // Parse cite tags and return structured data for rendering
    const parts: Array<{ type: 'text' | 'cite', content: string }> = [];
    let lastIndex = 0;
    
    const citeRegex = /<cite>(.*?)<\/cite>/g;
    let match;
    
    while ((match = citeRegex.exec(text)) !== null) {
        // Add text before the cite tag
        if (match.index > lastIndex) {
            parts.push({
                type: 'text',
                content: text.slice(lastIndex, match.index)
            });
        }
        
        // Add the cite tag
        parts.push({
            type: 'cite',
            content: match[1] || ''
        });
        
        lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text after the last cite tag
    if (lastIndex < text.length) {
        parts.push({
            type: 'text',
            content: text.slice(lastIndex)
        });
    }
    
    return parts;
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
                        class="text-xs" />

                    <label for="show_thinking">
                        Thinking
                    </label>

                    <Button type="button" 
                        text
                        size="small"
                        class="mr-2"
                        icon="pi pi-ellipsis-v" 
                        @click="toggleChatToolbarMenu" 
                        aria-haspopup="true" 
                        aria-controls="chat_toolbar_menu" />
                    <Menu ref="chat_toolbar_menu_ref"
                        id="chat_toolbar_menu" 
                        :model="chat_toolbar_items" 
                        :popup="true" />
                        
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
                        
                        <div class="message-content">
                            <template v-for="(part, index) in parseMessageText(message.text || '')" :key="index">
                                <span v-if="part.type === 'text'">
                                    <span v-html="marked(part.content)"></span>
                                </span>
                                <CiteTag v-else-if="part.type === 'cite'"
                                    :snippet_id="part.content"
                                    @click="handleCiteClick" />
                            </template>
                        </div>
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
                    <span class="text-sm text-gray-500">({{ evidence_count }})</span>
                </div>
                <div class="flex items-center gap-2">

                    <Button type="button" 
                        text
                        size="small"
                        class="mr-2"
                        icon="pi pi-ellipsis-v" 
                        @click="toggleChatToolbarMenu" 
                        aria-haspopup="true" 
                        aria-controls="chat_toolbar_menu" />
                    <Menu ref="chat_toolbar_menu_ref"
                        id="chat_toolbar_menu" 
                        :model="evidence_toolbar_items" 
                        :popup="true" />
                </div>
            </div>

            <!-- Evidence Body -->
            <div class="evidence-body flex-1 flex">
                <!-- Evidence Tabs (Left 1/4) -->
                <div class="w-1/4 border-r overflow-x-hidden bg-gray-50 pl-2"
                    style="overflow-y: auto; height: calc(100svh - 3rem);">
                    <div v-for="(snippet, index) in evidence_snippets" :key="snippet.snippet_id"
                        class="evidence-tab p-2 rounded hover:bg-white dark:hover:bg-gray-700 border-btransition-colors"
                        :class="{ 'bg-white dark:bg-gray-800 shadow-sm': snippet.snippet_id === case_store.current_evidence_tab }"
                        @click="handleEvidenceTabChange(snippet.snippet_id)">
                        <div class="flex items-center gap-2">
                            <span class="text-sm font-medium">
                                ({{ snippet.index + 1 }})
                            </span>
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
                                <font-awesome-icon icon="fa-regular fa-file-lines" />

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