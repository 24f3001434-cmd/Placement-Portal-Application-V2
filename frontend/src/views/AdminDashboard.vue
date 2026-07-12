<template>
  <Navbar />
  <div class="container mt-5">

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

async function loadDashboard() {
  try {
    const response = await api.get("/dashboard");

    dashboard.value = response.data;
  } catch (error) {
    console.log(error);
  }
}

onMounted(() => {
  loadDashboard();
});
</script>