<template>
  <div class="details-container">
    <header>
      <h1>ImmuniFHIR</h1>
      <span>Patient Details</span>
    </header>

    <div class="patient-header">
      <div class="patient-info">
        <h2>{{ patient.lastName }}, {{ patient.firstName }}</h2>
        <p>DOB: {{ patient.dob }} (Age {{ patient.age }})</p>
        <p>Gender: {{ patient.gender }}</p>
        <p>MRN: {{ patient.mrn }}</p>
        <p>{{ patient.address }}</p>
      </div>
      <div class="record-count">
        {{ patient.immunizations.length }} Records
      </div>
      <button @click="goBack">← Back to Search</button>
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
      <h3>Immunization History ({{ patient.immunizations.length }} records)</h3>

      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Vaccine Name</th>
            <th>Dose</th>
            <th>Lot Number</th>
            <th>Provider</th>
            <th>State</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in patient.immunizations" :key="record.lot">
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
</template>

<script>
import mockData from '../data/mockPatients.json'

export default {
  data() {
    return {
      patient: mockData.patients[0]
    }
  },
  methods: {
    goBack() {
      this.$router.push('/search')
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

button {
  position: absolute;
  bottom: 20px;
  right: 20px;
  padding: 8px 15px;
  background: white;
  border: 1px solid #ddd;
  cursor: pointer;
  color: #333;
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
</style>