import { createWebHistory, createRouter } from 'vue-router'

import Home from './pages/Home.vue';
import Login from './pages/Login.vue';

const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Login },
]

const router = createRouter({
    history: createWebHistory(
        import.meta.env.BASE_URL
    ),
    routes,
})

export default router