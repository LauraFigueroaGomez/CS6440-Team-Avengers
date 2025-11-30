<template>
  <div class="details-container">
    <header>
      <button @click="goBack" class="back-btn">←</button>
      <div class="logo">
        <h1>ImmuniFHIR</h1>
        <span>Patient Details</span>
      </div>
      <button @click="handleLogout" class="logout-btn" :disabled="loggingOut">
        {{ loggingOut ? 'Logging out...' : 'Log Out' }}
      </button>
    </header>

    <div v-if="loading" class="loading-container">
    <div class="spinner"></div>
    <p>{{ loadingMessage }}</p>
  </div>

  <!-- Only render details if patient is loaded -->
  <div v-else-if="patient">
    <div class="patient-header">
      <div class="patient-info">
        <h2>{{ patient.lastName }}, {{ patient.firstName }}</h2>
        <p>DOB: {{ formatDate(patient.dob) }} (Age {{ patient.age }})</p>
        <p>Gender: {{ patient.gender }}</p>
        <p>MRN: {{ patient.mrn }}</p>
        <p>{{ patient.address }}</p>
      </div>
      <div class="record-count">
        {{ patient.immunizations.length }} Records
      </div>
    </div>

    <div class="state-cards">
      <div class="card" v-for="(state, key) in patient.stateSummary" :key="key">
        <span class="state-label">{{ key }}</span>
        <span class="connected">Connected</span>
        <div class="count">{{ state.count }}</div>
        <div>Immunizations</div>
        <div class="years">{{ state.lastUpdate }}</div>
      </div>
    </div>

    <div class="history-section">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0;">Immunization History ({{ patient.immunizations.length }} records)</h3>
        <input
          v-model="filterText"
          type="text"
          placeholder="Filter records..."
          style="padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; background: white; color: #333;"
        />
      </div>

      <table>
        <thead>
          <tr>
            <th @click="sortTable('date')" style="cursor: pointer">
              Date
              <span v-if="sortColumn === 'date'">{{ sortDirection === 'asc' ? '▲' : '▼' }}</span>
            </th>
            <th @click="sortTable('vaccine')" style="cursor: pointer">
              Vaccine Name
              <span v-if="sortColumn === 'vaccine'">{{ sortDirection === 'asc' ? '▲' : '▼' }}</span>
            </th>
            <th>Dose</th>
            <th>Lot Number</th>
            <th>Provider</th>
            <th @click="sortTable('state')" style="cursor: pointer">
              State
              <span v-if="sortColumn === 'state'">{{ sortDirection === 'asc' ? '▲' : '▼' }}</span>
            </th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in sortedImmunizations" :key="record.lot">
            <td>{{ record.date }}</td>
            <td>{{ record.vaccine }} {{ record.manufacturer ? `(${record.manufacturer})` : '' }}</td>
            <td>{{ record.dose }}</td>
            <td>{{ record.lot }}</td>
            <td>{{ record.provider }}<br>{{ record.location }}</td>
            <td>{{ record.state }}</td>
            <td>✓ {{ record.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>
    <div v-else class="loading-container">
      <p>Patient not found.</p>
    </div>
  </div>
</template>

<script>
import { getPatientDetails, formatDate } from '../lib/api'
import { logout } from '../lib/auth'

export default {
  data() {
    return {
      patient: null,
      loading: true,
      loadingMessage: 'Aggregating immunization records from state registries...',
      sortColumn: null,
      sortDirection: 'asc',
      filterText: '',
      loggingOut: false
    }
  },
  async mounted() {
    this.loading = true
    this.loadingMessage = 'Aggregating immunization records from state registries...'

    try {
      const patientId = this.$route.params.id

      setTimeout(() => {
        this.loadingMessage = 'Normalizing data from multiple states...'
      }, 1000)

      this.patient = await getPatientDetails(patientId)
      console.log('Loaded patient details:', this.patient)
    } catch (err) {
      console.error('Error loading patient details:', err)
      alert('Error loading patient details. Check console for more info.')
    } finally {
      this.loading = false
    }
  },
  methods: {
    goBack() {
      this.$router.push('/search')
    },
    async handleLogout() {
      if (!confirm('Are you sure you want to log out?')) {
        return
      }
      this.loggingOut = true
      try {
        // Clear search state before logging out
        sessionStorage.removeItem('searchState')
        await logout()
        this.$router.push('/')
      } finally {
        this.loggingOut = false
      }
    },
    formatDate,
    sortTable(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortColumn = column
        this.sortDirection = 'asc'
      }
    }
  },
  computed: {
    sortedImmunizations() {
      if (!this.patient || !this.patient.immunizations) return []

      let records = [...this.patient.immunizations]

      if (this.filterText) {
        const searchText = this.filterText.toLowerCase()
        records = records.filter(r =>
          (r.date || '').toLowerCase().includes(searchText) ||
          (r.vaccine || '').toLowerCase().includes(searchText) ||
          (r.manufacturer || '').toLowerCase().includes(searchText) ||
          (r.dose || '').toLowerCase().includes(searchText) ||
          (r.lot || '').toLowerCase().includes(searchText) ||
          (r.provider || '').toLowerCase().includes(searchText) ||
          (r.location || '').toLowerCase().includes(searchText) ||
          (r.state || '').toLowerCase().includes(searchText) ||
          (r.status || '').toLowerCase().includes(searchText)
        )
      }

      if (!this.sortColumn) return records

      records.sort((a, b) => {
        let aVal = a[this.sortColumn]
        let bVal = b[this.sortColumn]

        if (this.sortColumn === 'date') {
          aVal = new Date(aVal).getTime()
          bVal = new Date(bVal).getTime()
        }

        if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1
        if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1
        return 0
      })

      return records
    }
  }
}
</script>

<style scoped>
.details-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f5f5f5;
  overflow: auto;
  padding: 20px;
}

header {
  background: white;
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  text-align: center;
}

header h1 {
  margin: 0;
  font-size: 20px;
  color: #000;
}

header span {
  color: #666;
  font-size: 14px;
}

.patient-header {
  background: white;
  padding: 20px;
  margin-bottom: 20px;
  position: relative;
}

.patient-info h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #000;
}

.patient-info p {
  margin: 5px 0;
  color: #666;
}

.record-count {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 18px;
  color: #333;
}

.back-btn {
  padding: 8px 12px;
  background: white;
  border: 1px solid #ddd;
  cursor: pointer;
  color: #333;
  font-size: 20px;
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

.state-cards {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.card {
  background: white;
  padding: 15px;
  flex: 1;
  border-left: 3px solid #5b51d8;
}

.card .state-label {
  background: #5b51d8;
  color: white;
  padding: 3px 8px;
  font-size: 12px;
}

.card .connected {
  float: right;
  color: green;
  font-size: 12px;
}

.card .count {
  font-size: 28px;
  margin: 10px 0 5px 0;
  color: #000;
}

.card .years {
  color: #666;
  font-size: 12px;
  margin-top: 5px;
}

.history-section {
  background: white;
  padding: 20px;
}

.history-section h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #000;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 10px;
  background: #f8f8f8;
  font-weight: normal;
  color: #666;
  border-bottom: 1px solid #ddd;
}

td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  color: #333;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px;
}

.loading-container p {
  margin-top: 20px;
  color: #666;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #5b51d8;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>