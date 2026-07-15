<template>

    <Navbar />

    <div class="container mt-5">
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

        <h2>Student Dashboard</h2>

        <hr>

        <div class="row">

            <div class="col-md-4">

                <div
                    class="card p-4 text-center"
                    style="cursor:pointer;"
                    @click="router.push('/student/jobs')"
                >

                    <h5>Available Jobs</h5>

                </div>

            </div>

            <div class="col-md-4">

                <div
                    class="card p-4 text-center"
                    style="cursor:pointer;"
                    @click="router.push('/student/applications')"
                >

                    <h5>Applied Jobs</h5>

                </div>

            </div>

            <div class="col-md-4">

                <div class="card p-4 text-center"
                style="cursor:pointer;"
                @click="router.push('/student/placements')">

                    <h5>Placement History</h5>

                </div>

            </div>

        </div>
        <div class="row mt-4">

            <div class="col-md-6">

                <div class="card shadow-sm">

                    <div class="card-body">

                        <h4>📄 Placement History Export</h4>

                        <p class="text-muted">
                            Export your complete placement and application history as CSV.
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

import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

import Navbar from "../components/Navbar.vue";

const router = useRouter();
const successMessage = ref("");
const errorMessage = ref("");

async function exportCSV() {

    try {

        const response = await api.post("/student/export-csv");

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
        "http://127.0.0.1:5000/download-report/student/student_1_history.csv",
        "_blank"
    );

}
</script>