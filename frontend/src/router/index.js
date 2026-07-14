import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PostListView from '../views/community/PostListView.vue'
import PostDetailView from '../views/community/PostDetailView.vue'
import PostFormView from '../views/community/PostFormView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/community', name: 'community-list', component: PostListView },
    { path: '/community/new', name: 'community-new', component: PostFormView },
    { path: '/community/:id', name: 'community-detail', component: PostDetailView, props: true },
    { path: '/community/:id/edit', name: 'community-edit', component: PostFormView, props: true },
  ],
})

export default router
