import { createApp } from 'vue';
import './assets/style.css';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import { my_preset_theme } from './theme';

// create the app
const app = createApp(App)

///////////////////////////////////////////////////////////
// PrimeVue
///////////////////////////////////////////////////////////
app.use(PrimeVue, {
    theme: {
        preset: my_preset_theme
    }
});

// finally, mount the app
app.mount('#app');
