import { createApp } from 'vue';  // Import createApp from Vue
import App from './App.vue';
import router from './router'; // Import the router
import VueCookies from 'vue3-cookies';

createApp(App)  // Initialize the Vue app
  .use(VueCookies)
  .use(router)  // Use the router
  .mount('#app');  // Mount the app to the DOM
