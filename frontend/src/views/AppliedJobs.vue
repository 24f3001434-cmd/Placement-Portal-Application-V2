<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/student/dashboard')"
        >
            ← Back
        </button>

        <h2>Applied Jobs</h2>

        <hr>

        <table class="table table-bordered">

            <thead>

                <tr>
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th>Applied On</th>
                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="application in applications"
                    :key="application.application_id"
                >

                    <td>{{ application.job_title }}</td>

                    <td>{{ application.company }}</td>

                    <td>{{ application.status }}</td>

                    <td>{{ application.applied_on }}</td>

                </tr>

            </tbody>

        </table>

    </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const router = useRouter();

const applications = ref([]);

async function loadApplications() {

    try {

        const response = await api.get(
            "/student/applications",
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        applications.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadApplications();

});

</script>