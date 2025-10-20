<script setup lang="ts">
import { ref } from 'vue';
import router from '../router';
import { samples } from '../models/Samples';
const input_text = ref('');
const el_textarea = ref(null);
const n_rows = ref(1);

const onClickSubmit = () => {
    console.log(input_text.value);

    router.push('/analyze');
}

const onClickSample = (sample: any) => {
    input_text.value = sample.text;

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

const get_samples = () => {
    // get fixed 3 samples with index
    return [
        samples.questions[2],
        samples.questions[8],
        samples.questions[20],
    ];
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

        <Card v-for="sample in get_samples()" 
            class="lg:w-1/3 cursor-pointer clickable-sample"
            @click="onClickSample(sample)">
            <template #title>
                {{ sample.section }}
            </template>
            <template #content>
                <p class="m-0">
                    {{ sample.text }}
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