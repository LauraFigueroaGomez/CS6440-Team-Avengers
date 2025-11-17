<template>
    <div class="login-container">
      <div class="login-box">
        <div class="login-header">
          <div class="logo-icon">
            <span>+</span>
          </div>
          <h1>ImmuniFHIR</h1>
          <p>Healthcare Provider Portal</p>
        </div>
        <form @submit.prevent="handleLogin">
          <div class="form-field">
            <input
              v-model="email"
              type="email"
              required
              placeholder="Email"
            />
          </div>

          <div class="form-field">
            <input
              v-model="password"
              type="password"
              required
              placeholder="Password"
            />
          </div>

          <button type="submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="footer-link">
          <a href="#">No authorized healthcare provider? ›</a>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  //imports
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { supabase } from '../lib/supabase'

  const router = useRouter()
  const email = ref('')
  const password = ref('')
  const loading = ref(false)

  const handleLogin = async () => {
    if (!email.value || !password.value) {
      alert('Please enter email and password')
      return
    }

    loading.value = true

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: email.value,
        password: password.value
      })

      if (error) {
        alert('Login failed: ' + error.message)
      } else if (data.user) {
        // login successful
        console.log('Logged in:', data.user.email)
        router.push('/search')
      }
    } catch (err) {
      alert('Something went wrong')
    } finally {
      loading.value = false
    }
  }
  </script>

  <style scoped>
  .login-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: #f5f5f5;
    display: grid;
    place-items: center;
  }

  .login-box {
    background: white;
    padding: 40px;
    width: 400px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }

  .login-header {
    text-align: center;
    margin-bottom: 30px;
  }

  .logo-icon {
    width: 60px;
    height: 60px;
    background: #5b51d8;
    margin: 0 auto 20px;
    display: grid;
    place-items: center;
  }

  .logo-icon span {
    color: white;
    font-size: 30px;
  }

  h1 {
    margin: 0;
    font-size: 24px;
    color: #000;
  }

  p {
    margin: 5px 0 0 0;
    color: #666;
  }

  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    background: white;
    color: #000;
  }

  button {
    width: 100%;
    padding: 12px;
    background: #5b51d8;
    color: white;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }

  .spinner {
    border: 2px solid #f3f3f3;
    border-top: 2px solid white;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
    margin-right: 8px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  a {
    display: block;
    text-align: center;
    margin-top: 20px;
    color: #5b51d8;
    font-size: 14px;
  }
  </style>