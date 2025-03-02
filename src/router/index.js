import { createRouter, createWebHistory } from 'vue-router';
const MovieSearch = () => import('../components/MovieSearch.vue');
const TopMovies = () => import('../components/TopMovies.vue');
const PlayerPage = () => import('../components/PlayerPage.vue');
const NotFound = () => import('../components/NotFound.vue');
const ContactsPage = () => import('../components/ContactsPage.vue');

const routes = [
  {
    path: '/',
    component: MovieSearch,
    name: 'home',
    meta: {
      title: 'Поиск фильмов',
    },
  },
  {
    path: '/top',
    component: TopMovies,
    name: 'top-movies',
    meta: {
      title: 'Топ фильмов',
    },
  },
  {
    path: '/movie/:kp_id',
    component: PlayerPage,
    name: 'player-page',
    meta: {
      title: 'Просмотр фильма',
    },
  },
  {
    path: '/contact',
    name: 'ContactsPage',
    component: ContactsPage,
    meta: {
      title: 'Контакты',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFound,
    name: 'NotFound',
    meta: {
      title: '404 - Страница не найдена',
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const title = to.meta.title || 'Vue App';
  document.title = title;
  next();
});

export default router;
