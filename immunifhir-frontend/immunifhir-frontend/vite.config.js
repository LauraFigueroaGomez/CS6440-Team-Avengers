import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  preview: {
    host: true,
    port: 10000,
    allowedHosts: ['cs6440-team-avengers-1-frontend.onrender.com']
  }
})