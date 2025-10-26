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

          <button type="submit">
            Sign In
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

  const router = useRouter()
  const email = ref('')
  const password = ref('')

  const handleLogin = () => {
    if (email.value && password.value) {
      router.push('/search')
    } else {
      alert('Please enter email and password')
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
  }

  a {
    display: block;
    text-align: center;
    margin-top: 20px;
    color: #5b51d8;
    font-size: 14px;
  }
  </style>