<template>
  <div class="search-container">
    <header>
      <div class="logo">
        <div>
          <h1>ImmuniFHIR</h1>
          <span>Multi-State Registry Access</span>
        </div>
      </div>
    </header>

    <main>
      <h2>Search Patient Records</h2>
      <p>Query immunization records across NY, NJ, and PA state registries</p>

      <form @submit.prevent="searchPatients">
        <div class="form-row">
          <div class="field">
            <label>First Name *</label>
            <input
              v-model="firstName"
              type="text"
              placeholder="John"
            />
          </div>

          <div class="field">
            <label>Last Name *</label>
            <input
              v-model="lastName"
              type="text"
              placeholder="Doe"
            />
          </div>

          <div class="field">
            <label>Date of Birth</label>
            <input
              v-model="dob"
              type="date"
            />
          </div>
        </div>

        <button type="submit" class="search-btn">
          <span>🔍</span>
          Search All States
        </button>
      </form>

      <div class="info-box">
        <span class="icon">ℹ️</span>
        <div>
          <strong>Multi-State Query</strong>
          <p>This search queries 3 state immunization registries simultaneously. Typically completes in 2-5 seconds.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      dob: ''
    }
  },
  methods: {
    searchPatients() {
      if (!this.firstName || !this.lastName) {
        alert('Please enter first and last name')
        return
      }

      const searchData = {
        first: this.firstName,
        last: this.lastName,
        birthdate: this.dob
      }

      console.log('Searching for:', searchData)
    }
  }
}
</script>

<style scoped>
.search-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f5f5f5;
  overflow: auto;
}

header {
  background: white;
  padding: 16px 24px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.logo h1 {
  font-size: 20px;
  margin: 0;
  color: #333;
  font-weight: 600;
}

.logo span {
  font-size: 14px;
  color: #666;
}

main {
  padding: 60px 120px;
}

main h2 {
  font-size: 28px;
  margin-bottom: 12px;
  color: #111;
  text-align: center;
}

main > p {
  color: #666;
  margin-bottom: 40px;
  text-align: center;
  font-size: 15px;
}

form {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.field {
  flex: 1;
}

.field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.field input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 15px;
  background: #fafafa;
}

.field input:focus {
  outline: none;
  border-color: #5b51d8;
  background: white;
}

.search-btn {
  background: #5b51d8;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;
  font-weight: 500;
}

.search-btn:hover {
  background: #4c43b8;
}

.info-box {
  margin-top: 24px;
  padding: 16px;
  background: #f0f7ff;
  border-radius: 8px;
  display: flex;
  gap: 12px;
  border: 1px solid #d0e2ff;
}

.info-box .icon {
  font-size: 20px;
}

.info-box strong {
  display: block;
  margin-bottom: 4px;
  font-size: 14px;
  color: #333;
}

.info-box p {
  color: #666;
  margin: 0;
  font-size: 13px;
  line-height: 1.4;
}

@media (max-width: 640px) {
  .form-row {
    flex-direction: column;
  }

  main {
    margin: 20px auto;
  }
}
</style>