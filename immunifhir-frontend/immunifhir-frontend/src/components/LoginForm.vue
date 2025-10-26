<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
      <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <div class="text-center mb-8">
          <div class="mx-auto w-16 h-16 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
            <span class="text-white text-2xl font-bold">+</span>
          </div>
          <h1 class="text-2xl font-bold text-gray-900">ImmuniFHIR</h1>
          <p class="text-gray-600 mt-2">Healthcare Provider Portal</p>
        </div>
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <input
              v-model="email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <input
              v-model="password"
              type="password"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
            title="Login"
          >
          </button>
        </form>

        <div class="mt-6 text-center">
          <a href="#" class="text-sm text-blue-600 hover:underline">
            No authorized healthcare provider? ›
          </a>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  //imports 
  import { ref } from 'vue'

  const email = ref('')      
  const password = ref('')   

  const handleLogin = () => {

    alert('login button hit')
  }
  </script>