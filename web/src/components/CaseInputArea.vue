<script setup lang="ts">
import { ref } from 'vue';
import router from '../router';
const input_text = ref('');
const el_textarea = ref(null);
const n_rows = ref(1);

const onClickSubmit = () => {
    console.log(input_text.value);

    router.push('/analyze');
}

const samples = {
    "sample-dgx-guideline": "What are the recommended guidelines for the initial management of a patient presenting with acute chest pain?",
    "sample-dgx-diagnosis": "What is the differential diagnosis for a 32-year-old woman with acute onset of shortness of breath and chest pain?",
    "sample-dgx-treatment": "What is the treatment plan for a 32-year-old man with acute onset of shortness of breath and chest pain?",
};

const onClickSample = (sample_id: keyof typeof samples) => {
    input_text.value = samples[sample_id];

    onInputTextarea();
}

const onInputTextarea = () => {
    // get the number of characters in the textarea

    const n_chars = input_text.value.length;

    // set the number of rows to the number of characters / 60
    let n = Math.ceil(n_chars / 60);

    if (n > 10) {
        n = 10;
    } else if (n < 1) {
        n = 1;
    }

    n_rows.value = n;
}

const flag_show_more_samples = ref(false);
const onClickSeeMore = () => {
    flag_show_more_samples.value = !flag_show_more_samples.value;
}
</script>

<template>
<div class="flex flex-col items-center mt-8 gap-3 w-full">

    <div class="w-full flex flex-row align-items-end justify-end" style="max-width: 40rem;">
        <div class="relative w-full">
            <textarea
                ref="el_textarea"
                id="input-textarea"
                wrap="soft"
                v-model="input_text"
                :rows="n_rows"
                class="w-full p-4 pr-16 rounded-2xl border resize-none shadow focus:outline-red-500"
                placeholder="Describe a clinical case or question..."
                @input="onInputTextarea"
                style="overflow: auto; max-height: 20rem;"
            ></textarea>
            <div style="position: absolute; bottom: 0; right: 0; transform: translateX(-40%) translateY(-38%);">
                <Button @click="onClickSubmit" class="!p-2 !h-10">
                    <font-awesome-icon icon="fa-solid fa-paper-plane" class="text-2xl"/>
                </Button>
            </div>
        </div>
    </div>

    <!-- Samples -->
    <div class="flex lg:flex-row max-sm:flex-col gap-4 mb-2 lg:w-1/2">

        <Card class="lg:w-1/3 cursor-pointer clickable-sample"
            @click="onClickSample('sample-dgx-guideline')">
            <template #title>
                Ask about guideline
            </template>
            <template #content>
                <p class="m-0">
                    {{ samples['sample-dgx-guideline'] }}
                </p>
            </template>
        </Card>

        <Card class="lg:w-1/3 cursor-pointer clickable-sample"
            @click="onClickSample('sample-dgx-diagnosis')">
            <template #title>
                Differential diagnosis
            </template>
            <template #content>
                <p class="m-0">
                    {{ samples['sample-dgx-diagnosis'] }}
                </p>
            </template>
        </Card>

        <Card class="lg:w-1/3 cursor-pointer clickable-sample"
            @click="onClickSample('sample-dgx-treatment')">
            <template #title>
                Treatment plan
            </template>
            <template #content>
                <p class="m-0">
                    {{ samples['sample-dgx-treatment'] }}
                </p>
            </template>
        </Card>

    </div>


    <!-- More samples -->
    <div class="flex flex-col items-center gap-4 mb-2 w-1/2 justify-center mt-4">
        <p class="cursor-pointer" @click="onClickSeeMore">
            See more case samples ... 
            <template v-if="flag_show_more_samples">
                <font-awesome-icon icon="fa-solid fa-chevron-up" />
            </template>
            <template v-else>
                <font-awesome-icon icon="fa-solid fa-chevron-down" />
            </template>
        </p>

        <template v-if="flag_show_more_samples">
            <Fieldset legend="Type 2 Diabetes Mellitus">
                <p class="m-0">
                    
                </p>
            </Fieldset>
        </template>
    </div>
    
</div>
</template>

<style scoped>
.clickable-sample:hover {
    background: var(--hover-color);
}
</style>