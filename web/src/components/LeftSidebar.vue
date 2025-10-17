<script setup lang="ts">
import { ref } from "vue";

const flag_sidebar_open = ref(false);

const onClickToggleSidebar = () => {
    flag_sidebar_open.value = !flag_sidebar_open.value;
}

</script>

<template>

<div class="left-sidebar lg:h-screen" 
    :class="{ 'left-sidebar-open': flag_sidebar_open }">
    <div class="menu-item"
        v-tooltip.right="'Open/close sidebar'"
        @click="onClickToggleSidebar">
        <font-awesome-icon icon="fa-solid fa-bars" />
        <div class="menu-item-text">
            <span>
                Toggle Sidebar
            </span>
        </div>
    </div>

    <div class="menu-divider"></div>

    <div class="menu-item"
        v-tooltip.right="'Analyze new clinical case'">
        <font-awesome-icon icon="fa-regular fa-comments" />
        <div class="menu-item-text">
            <span>
                Analyze Case
            </span>
        </div>
    </div>

    <div class="menu-item"
        v-tooltip.right="'Analyze new clinical case'">
        <font-awesome-icon icon="fa-regular fa-folder-open" />
        <div class="menu-item-text">
            <span>
                Past Cases
            </span>
        </div>
    </div>
</div>

</template>

<style scoped>
.left-sidebar {
    position: absolute;
    z-index: 999;
    left: 0;
    top: 0;
    width: 3rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    background: var(--background-color);
    border-right: 1px solid var(--border-color);
    box-shadow: 0 0 10px 0 var(--shadow-color);
    border-radius: 0 0 10px 0;
    padding: 0.5rem;

    display: flex;
    flex-direction: column;
    align-items: start; 
    gap: 0.5rem;
}
.menu-divider {
    width: 100%;
    height: 1px;
    border-bottom: 1px solid var(--border-color);
}
.menu-item {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: start;
    padding: 0.5rem;
    cursor: pointer;
    width: 100%;
    border-radius: 0.25rem;
    height: 2rem;
}
.menu-item:hover {
    background: var(--hover-color);
}
.menu-item-text {
    font-size: 1rem;
    margin-left: 0.5rem;
    display: none;
}
.left-sidebar-open {
    width: 15rem !important;
}
.left-sidebar-open .menu-item-text {
    display: block;
}
</style>
