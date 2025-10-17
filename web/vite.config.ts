import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcss from '@tailwindcss/vite';
import Components from 'unplugin-vue-components/vite';
import {PrimeVueResolver} from '@primevue/auto-import-resolver';
import * as toolbox from './src/utils/toolbox';

// https://vite.dev/config/
export default () => {
  console.log('* loading env vars...');
  console.log(`  SUPABASE_URL: ${toolbox.truncate(process.env.VITE_SUPABASE_URL ?? '')}`);
  console.log(`  SUPABASE_KEY: ${toolbox.truncate(process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? '')}`);
  console.log(`  BASE_URL: ${toolbox.truncate(process.env.VITE_BASE_URL ?? '')}`);


  let BASE_URL = process.env.VITE_BASE_URL ?? './';
  console.log('* VITE_BASE_URL_ALIAS:', process.env.VITE_BASE_URL_ALIAS);


  return defineConfig({
    base: BASE_URL,

    server: {
      host: '0.0.0.0',
      port: 8968,
    },

    define: {
      ENV_CONFIG: process.env,
    },

    plugins: [
      vue(), 
      tailwindcss(),
      Components({
          resolvers: [
            PrimeVueResolver()
          ] 
        }),
    ],

    build: {
      outDir: 'dist',
    },
  })
}
