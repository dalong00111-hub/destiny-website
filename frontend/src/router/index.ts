import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ServiceView from '../views/ServiceView.vue'
import ResultView from '../views/ResultView.vue'
import AboutView from '../views/AboutView.vue'
import FAQView from '../views/FAQView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/service',
      name: 'service',
      component: ServiceView
    },
    {
      path: '/result',
      name: 'result',
      component: ResultView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/faq',
      name: 'faq',
      component: FAQView
    }
  ]
})

export default router