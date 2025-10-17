<script setup lang="ts">
import Aurora from './components/backgrounds/Aurora.vue';
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
  <H1>Hello World</H1>
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
