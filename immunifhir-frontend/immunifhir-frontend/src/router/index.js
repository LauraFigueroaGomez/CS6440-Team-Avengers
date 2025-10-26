import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import PatientSearch from '../components/PatientSearch.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginForm
  },
  {
    path: '/search',
    name: 'PatientSearch',
    component: PatientSearch
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router