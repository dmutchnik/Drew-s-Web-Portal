import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import RegistrationForm from './components/RegistrationForm.vue';
import LoginForm from './components/LoginForm.vue';
import Profile from './components/Profile.vue';
import App from './ProfileApp.vue';

const routes = [
  { path: '/', redirect: '/login' }, // Redirect root path to login page
  { path: '/register', component: RegistrationForm },
  { path: '/login', component: LoginForm },
  { path: '/profile', component: Profile }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
