import "primeicons/primeicons.css";
import './assets/style.css';

import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import { my_preset_theme } from './theme';
import { createPinia } from 'pinia';
import router from './router';
import { useDataStore } from './stores/DataStore';
import { vCite } from './directives/v-cite';
import ToastService from 'primevue/toastservice';
import { useCaseStore } from './stores/CaseStore';
import { useUserStore } from './stores/UserStore';

// create the app
const app = createApp(App)

// add the pinia store
const pinia = createPinia()
app.use(pinia)

// add the router
app.use(router)

// add the v-cite directive
app.directive('cite', vCite)

// add the toast service
app.use(ToastService);

///////////////////////////////////////////////////////////
// PrimeVue
///////////////////////////////////////////////////////////
app.use(PrimeVue, {
    theme: {
        preset: my_preset_theme
    }
});

///////////////////////////////////////////////////////////
// Font Awesome
///////////////////////////////////////////////////////////
import { library } from '@fortawesome/fontawesome-svg-core';

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';

library.add(fas, far, fab);
// Add the FontAwesomeIcon component globally
app.component('font-awesome-icon', FontAwesomeIcon)

///////////////////////////////////////////////////////////
// Store
///////////////////////////////////////////////////////////
const store = useDataStore();
const case_store = useCaseStore();
const user_store = useUserStore();

// bind to window for debugging
(window as any).store = store;

// @ts-expect-error: Dynamically attaching stores for debugging in dev mode
store.case_store = case_store;
// @ts-expect-error: Dynamically attaching stores for debugging in dev mode
store.user_store = user_store;

// bind color scheme to store
const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

function handleThemeChange(event: MediaQueryListEvent) {
  console.log('* handleThemeChange', event.matches);
  if (event.matches) {
    store.color_scheme = 'dark';
  } else {
    store.color_scheme = 'light';
  }
}

darkModeMediaQuery.addEventListener('change', handleThemeChange);

store.init();

// bind a sample clinical case to the store
import { clinical_case } from "./models/Samples";
store.current_clinical_case = clinical_case;

///////////////////////////////////////////////////////////
// Router
///////////////////////////////////////////////////////////
// bind router with store for navigation
router.beforeEach((to, from, next) => {
    console.log('from', from, 'to', to)
    // set the store.current_page
    store.current_page = to.path.substring(1)
    next()
})



// finally, mount the app
app.mount('#app');
