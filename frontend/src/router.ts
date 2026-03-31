import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import AdminView from './views/AdminView.vue';
import SectionView from './views/SectionView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/shows', component: SectionView, props: { section: 'shows' } },
    { path: '/accomplishments', component: SectionView, props: { section: 'accomplishments' } },
    { path: '/work', component: SectionView, props: { section: 'work' } },
    { path: '/blog', component: SectionView, props: { section: 'blog' } },
    { path: '/gallery', component: SectionView, props: { section: 'gallery' } },
    { path: '/admin', component: AdminView },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
