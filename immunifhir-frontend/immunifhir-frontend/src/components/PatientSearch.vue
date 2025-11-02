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

        <button type="submit" class="search-btn">
          <span>🔍</span>
          Search All States
        </button>
      </form>

      <div class="info-box" v-if="!showResults">
        <div>
          <strong>Multi-State Query</strong>
          <p>This search queries 3 state immunization registries simultaneously. Typically completes in 2-5 seconds.</p>
        </div>
      </div>

      <div v-if="showResults" class="results-section">
        <div class="results-header">
          <h3>Search Results</h3>
          <button @click="clearSearch">New Search</button>
        </div>
        <p>Found 1 patient matching your search</p>

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
            <tr>
              <td>{{ searchResult.lastName }}, {{ searchResult.firstName }}</td>
              <td>{{ searchResult.dob }}</td>
              <td>3</td>
              <td>NY, NJ, PA</td>
              <td>
                <button @click="viewDetails">View Details</button>
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

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      dob: '',
      showResults: false,
      searchResult: null
    }
  },
  methods: {
    searchPatients() {
      if (!this.firstName || !this.lastName) {
        alert('Please enter first and last name')
        return
      }

      // fake search - just show the mock data
      setTimeout(() => {
        this.searchResult = mockData.patients[0]
        this.showResults = true
      }, 500)
    },
    clearSearch() {
      this.showResults = false
      this.searchResult = null
      this.firstName = ''
      this.lastName = ''
      this.dob = ''
    },
    viewDetails() {
      this.$router.push('/patient/P001')
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