import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { VitePWA } from 'vite-plugin-pwa'  // Проверь, чтобы импорт был именно таким

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt'],
    })
  ],
  resolve: {
    alias: {
      '@': '/src',  // Убедитесь, что это соответствует вашей структуре проекта
    },
  },
});
