<template>
  <div class="search-container">
    <header>
      <div class="logo">
        <div>
          <h1>ImmuniFHIR</h1>
          <span>Multi-State Registry Access</span>
        </div>
      </div>
      <button @click="handleLogout" class="logout-btn" :disabled="loggingOut">
        {{ loggingOut ? 'Logging out...' : 'Log Out' }}
      </button>
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
            />
          </div>

          <div class="field">
            <label>Last Name *</label>
            <input
              v-model="lastName"
              type="text"
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

        <button type="submit" class="search-btn" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Searching...' : 'Search All States' }}
        </button>
      </form>

      <div class="info-box" v-if="!showResults">
        <div style="text-align: center; width: 100%;">
          <strong>Multi-State Query</strong>
          <p>This search queries 3 state immunization registries simultaneously. Typically completes in 2-5 seconds.</p>
        </div>
      </div>

      <div v-if="showResults" class="results-section">
        <div class="results-header">
          <h3>Search Results</h3>
          <button @click="clearSearch">New Search</button>
        </div>
        <p>Found {{ searchResults.length }} patients matching your search</p>

        <table>
          <thead>
            <tr>
              <th>Patient Name</th>
              <th>Date of Birth</th>
              <th>Records Found</th>
              <th>State Sources</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in searchResults" :key="patient.id">
              <td>{{ patient.lastName }}, {{ patient.firstName }}</td>
              <td>{{ patient.dob }}</td>
              <td>{{ patient.immunizations.length }}</td>
              <td>NY, NJ, PA</td>
              <td>
                <button @click="viewDetails(patient.id)">View Details</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script>
import mockData from '../data/mockPatients.json'
import { logout } from '../lib/auth'

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      dob: '',
      showResults: false,
      searchResults: [],
      loading: false,
      loggingOut: false
    }
  },
  methods: {
    searchPatients() {
      if (!this.firstName || !this.lastName) {
        alert('Please enter first and last name')
        return
      }

      this.loading = true
      this.showResults = false

      // fake search - just show all the mock data
      setTimeout(() => {
        this.loading = false
        // just return all patients for now
        this.searchResults = mockData.patients
        this.showResults = true
      }, 1500)
    },
    clearSearch() {
      this.showResults = false
      this.searchResults = []
      this.firstName = ''
      this.lastName = ''
      this.dob = ''
    },
    viewDetails(patientId) {
      this.$router.push('/patient/' + patientId)
    },
    async handleLogout() {
      this.loggingOut = true
      try {
        await logout()
        this.$router.push('/')
      } catch (error) {
        alert('Logout failed')
        this.loggingOut = false
      }
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.logout-btn {
  padding: 8px 16px;
  background: white;
  border: 1px solid #ddd;
  cursor: pointer;
  color: #333;
  font-size: 14px;
}

.logout-btn:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
  color: #9ca3af;
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
  gap: 50px;
  margin-bottom: 30px;
  padding: 0 20px;
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
  background: white;
  color: #000;
}

.field input:focus {
  outline: none;
  border-color: #5b51d8;
  background: white;
  color: #000;
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
  justify-content: center;
  gap: 8px;
  margin: 0 auto;
  font-weight: 500;
}

.search-btn:hover {
  background: #4c43b8;
}

.search-btn:disabled {
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
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.results-section {
  margin-top: 30px;
  background: white;
  padding: 30px;
  border-radius: 8px;
}

.results-section p {
  color: #666;
  margin-bottom: 10px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  align-items: center;
}

.results-header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.results-header button {
  padding: 8px 16px;
  background: white;
  border: 1px solid #ddd;
  cursor: pointer;
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background: white;
}

th {
  text-align: left;
  padding: 10px;
  background: #f8f8f8;
  border: 1px solid #ddd;
  font-weight: normal;
  color: #333;
}

td {
  padding: 10px;
  border: 1px solid #ddd;
  color: #000;
  background: white;
}

td button {
  padding: 6px 12px;
  background: #5b51d8;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
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