<template>
  <Navbar />
  <div class="container mt-5">
    <div
      v-if="successMessage"
      class="alert alert-success alert-dismissible fade show"
      role="alert"
    >
      {{ successMessage }}
      <button
        type="button"
        class="btn-close"
        @click="successMessage=''"
      ></button>
    </div>

    <div
      v-if="errorMessage"
      class="alert alert-danger alert-dismissible fade show"
      role="alert"
    >
      {{ errorMessage }}
      <button
        type="button"
        class="btn-close"
        @click="errorMessage=''"
      ></button>
    </div>

    <h2>Admin Dashboard</h2>

    <hr>

    <div class="row">

      <div class="col-md-3">
        <div 
          class ="card p-3"
          style="cursor:pointer"
          @click="$router.push('/students')"
          >
          <h5>Total Students</h5>
          <h3>{{ dashboard.students }}</h3>
        </div>
      </div>

      <div class="col-md-3">
        <div
          class="card p-3"
          style="cursor:pointer"
          @click="$router.push('/companies')"
        >
          <h5>Total Companies</h5>
          <h3>{{ dashboard.companies }}</h3>
        </div>
      </div>

      <div class="col-md-3">
        <div
          class="card p-3"
          style="cursor:pointer"
          @click="$router.push('/jobs')"
        >
          <h5>Total Jobs</h5>
          <h3>{{ dashboard.jobs }}</h3>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card p-3">
          <h5>Total Applications</h5>
          <h3>{{ dashboard.applications }}</h3>
        </div>
      </div>

    </div>
    <div class="row mt-4">

      <div class="col-md-6">

        <div class="card shadow-sm">

          <div class="card-body">

            <h4 class="card-title">
              📊 Monthly Placement Report
            </h4>

            <p class="text-muted">
              Generate the latest placement report asynchronously using Celery.
            </p>

            <div class="d-flex gap-2">

              <button
                class="btn btn-primary"
                @click="generateReport"
              >
                Generate Report
              </button>

              <button
                class="btn btn-success"
                @click="downloadReport"
              >
                Download Report
              </button>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import Navbar from "../components/Navbar.vue";

const dashboard = ref({
  students: 0,
  companies: 0,
  jobs: 0,
  applications: 0,
});
const successMessage = ref("");
const errorMessage = ref("");

async function loadDashboard() {
  try {
    const response = await api.get("/dashboard");

    dashboard.value = response.data;
  } catch (error) {
    console.log(error);
  }
}
async function generateReport() {

  try {

    const response = await api.post("/monthly-report");

    successMessage.value = response.data.message;

    setTimeout(() => {
        successMessage.value = "";
    }, 3000);

  } catch (error) {

    errorMessage.value = "Unable to generate monthly report.";

    setTimeout(() => {
        errorMessage.value = "";
    }, 3000);

    console.log(error);

  }

}
function downloadReport() {

  window.open(
    "http://127.0.0.1:5000/download-report/admin/monthly_report.txt",
    "_blank"
  );

}

onMounted(() => {
  loadDashboard();
});
</script>