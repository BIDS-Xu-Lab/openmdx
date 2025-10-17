<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from '../stores/UserStore';

const userStore = useUserStore();

const password = ref('');
const check_remember_me = ref(true);
</script>
<template>
    <div class="bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-20 lg:px-80">
        <div class="bg-surface-0 dark:bg-surface-900 p-8 md:p-12 shadow-sm rounded-2xl w-full max-w-sm mx-auto flex flex-col gap-8">
            <div class="flex flex-col items-center gap-4">
                <div class="flex flex-col items-center gap-2 w-full">
                    <div class="text-surface-900 dark:text-surface-0 text-2xl font-semibold leading-tight text-center w-full">Welcome Back</div>
                </div>
            </div>
            <div class="flex flex-col gap-6 w-full">
                <div class="flex flex-col gap-2 w-full">
                    <label for="email1" class="text-surface-900 dark:text-surface-0 font-medium leading-normal">Email Address</label>
                    <InputText id="email1" type="text" placeholder="Email address" class="w-full px-3 py-2 shadow-sm rounded-lg" />
                </div>
                <div class="flex flex-col gap-2 w-full">
                    <label for="password1" class="text-surface-900 dark:text-surface-0 font-medium leading-normal">Password</label>

                    <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" :feedback="false" input-class="w-full!" />
                </div>
                <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between w-full gap-3 sm:gap-0">
                    <div class="flex items-center gap-2">
                        <Checkbox id="rememberme1" v-model="check_remember_me" :binary="true" />
                        <label for="rememberme1" class="text-surface-900 dark:text-surface-0 leading-normal">Remember me</label>
                    </div>
                </div>
            </div>
            <Button label="Sign In" icon="pi pi-user" 
                class="w-full py-2 rounded-lg flex justify-center items-center gap-2">
                <template #icon>
                    <i class="pi pi-user text-base! leading-normal!" />
                </template>
            </Button>
        </div>
    </div>
</template>
