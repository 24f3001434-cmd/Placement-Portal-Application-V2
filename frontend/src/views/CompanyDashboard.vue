<template>

    <Navbar />

    <div class="container mt-5">

        <h2>Company Dashboard</h2>
        <div
            v-if="successMessage"
            class="alert alert-success alert-dismissible fade show"
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
        >
            {{ errorMessage }}
            <button
                type="button"
                class="btn-close"
                @click="errorMessage=''"
            ></button>
        </div>

        <hr>

        <div class="row">

            <div class="col-md-3">

                <div
                    class="card p-4 text-center"
                    style="cursor:pointer;"
                    @click="router.push('/company/jobs')"
                >

                    <h5>Total Jobs Posted</h5>

                    <h3>{{ totalJobs }}</h3>

                </div>

            </div>

            <div class="col-md-3">

                <div
                    class="card p-4 text-center"
                    style="cursor:pointer;"
                    @click="router.push('/company/jobs')"
                >

                    <h5>Total Applications</h5>

                    <h3>{{ totalApplications }}</h3>

                </div>

            </div>

            <div class="col-md-3">

                <div class="card p-4 text-center"
                style="cursor:pointer;"
                @click="router.push('/company/shortlisted')"
                >

                    <h5>Shortlisted</h5>

                    <h3>{{ shortlisted }}</h3>

                </div>

            </div>

            <div class="col-md-3">

                <div
                    class="card p-4 text-center"
                    style="cursor:pointer;"
                    @click="router.push('/post-job')"
                >

                    <h5>Post New Job</h5>

                </div>

            </div>

        </div>
        <div class="row mt-4">

            <div class="col-md-6">

                <div class="card shadow-sm">

                    <div class="card-body">

                        <h4>📊 Monthly Company Report</h4>

                        <p class="text-muted">
                            Generate and download your monthly placement report.
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

            <div class="col-md-6">

                <div class="card shadow-sm">

                    <div class="card-body">

                        <h4>📄 Export Applications</h4>

                        <p class="text-muted">
                            Export all applications as CSV.
                        </p>

                        <div class="d-flex gap-2">

                            <button
                                class="btn btn-primary"
                                @click="exportCSV"
                            >
                                Export CSV
                            </button>

                            <button
                                class="btn btn-success"
                                @click="downloadCSV"
                            >
                                Download CSV
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
import { useRouter } from "vue-router";
import api from "../services/api";
import Navbar from "../components/Navbar.vue";

const router = useRouter();

const totalJobs = ref(0);
const totalApplications = ref(0);
const shortlisted = ref(0);
const successMessage = ref("");
const errorMessage = ref("");

async function loadDashboard() {

    try {

        const response = await api.get("/company/dashboard", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        totalJobs.value = response.data.total_jobs;
        totalApplications.value = response.data.total_applications;
        shortlisted.value = response.data.shortlisted;

    }

    catch (error) {

        console.log(error);

    }

}

async function generateReport() {

    try {

        const response = await api.post("/company/monthly-report");

        successMessage.value = response.data.message;

        setTimeout(() => {
            successMessage.value = "";
        }, 3000);

    }

    catch {

        errorMessage.value = "Unable to generate report.";

        setTimeout(() => {
            errorMessage.value = "";
        }, 3000);

    }

}

function downloadReport() {

    window.open(
        "http://127.0.0.1:5000/download-report/company/company_1_monthly_report.txt",
        "_blank"
    );

}

async function exportCSV() {

    try {

        const response = await api.post("/company/export-csv");

        successMessage.value = response.data.message;

        setTimeout(() => {
            successMessage.value = "";
        }, 3000);

    }

    catch {

        errorMessage.value = "Unable to export CSV.";

        setTimeout(() => {
            errorMessage.value = "";
        }, 3000);

    }

}

function downloadCSV() {

    window.open(
        "http://127.0.0.1:5000/download-report/company/company_1_applications.csv",
        "_blank"
    );

}

onMounted(() => {

    loadDashboard();

});

</script>