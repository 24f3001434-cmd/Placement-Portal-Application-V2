<template>
    <Navbar />
    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/jobs')"
        >
            ← Back
        </button>

        <h2>Job Details</h2>

        <hr>

        <div class="card p-4">

            <p><strong>Company:</strong> {{ job.company }}</p>

            <p><strong>Job Title:</strong> {{ job.title }}</p>

            <p><strong>Description:</strong> {{ job.description }}</p>

            <p><strong>Eligibility:</strong> {{ job.eligibility }}</p>

            <p><strong>Skills:</strong> {{ job.skills }}</p>

            <p><strong>Experience:</strong> {{ job.experience }}</p>

            <p><strong>Salary:</strong> {{ job.salary_package }}</p>

            <p><strong>Status:</strong> {{ job.status }}</p>

            <button
                v-if="job.status == 'pending'"
                class="btn btn-success"
                @click="approveJob"
            >
                Approve
            </button>

        </div>

    </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import Navbar from "../components/Navbar.vue";

const route = useRoute();
const router = useRouter();

const job = ref({});

async function loadJob() {

    try {

        const response = await api.get(`/job/${route.params.id}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
        });

        job.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}
async function approveJob() {

    try {

        await api.put(`/approve-job/${route.params.id}`, {}, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        alert("Job Approved Successfully");

        loadJob();

    }

    catch (error) {

        console.log(error);

    }

}
onMounted(() => {

    loadJob();

});

</script>