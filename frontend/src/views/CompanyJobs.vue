<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/company/dashboard')"
        >
            ← Back
        </button>

        <h2>My Job Postings</h2>

        <hr>

        <table class="table table-bordered">

            <thead>

                <tr>
                    <th>Job Title</th>
                    <th>Salary</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="job in jobs"
                    :key="job.id"
                >

                    <td>{{ job.title }}</td>
                    <td>{{ job.salary_package }}</td>
                    <td>{{ job.status }}</td>

                    <td>

                        <button
                            class="btn btn-primary btn-sm"
                            @click="router.push(`/company/job/${job.id}`)"
                        >
                            View
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import api from "../services/api";
import Navbar from "../components/Navbar.vue";

const router = useRouter();

const jobs = ref([]);

async function loadJobs() {

    try {

        const response = await api.get("/company/jobs", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        jobs.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadJobs();

});

</script>