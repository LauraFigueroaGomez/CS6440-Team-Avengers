import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import PatientSearch from '../components/PatientSearch.vue'
import PatientDetails from '../components/PatientDetails.vue'

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
  },
  {
    path: '/patient/:id',
    name: 'PatientDetails',
    component: PatientDetails
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router