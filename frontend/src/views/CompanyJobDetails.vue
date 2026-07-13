<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/company/jobs')"
        >
            ← Back
        </button>

        <h2>Job Details</h2>

        <hr>

        <div class="card p-4">

            <p><strong>Job Title:</strong> {{ job.title }}</p>

            <p><strong>Description:</strong> {{ job.description }}</p>

            <p><strong>Eligibility:</strong> {{ job.eligibility }}</p>

            <p><strong>Skills:</strong> {{ job.skills }}</p>

            <p><strong>Experience:</strong> {{ job.experience }}</p>

            <p><strong>Salary Package:</strong> {{ job.salary_package }}</p>

            <p><strong>Status:</strong> {{ job.status }}</p>

            <p><strong>Approval:</strong> {{ job.approval }}</p>

        </div>
        <div class="mt-3">

            <button
                v-if="job.status === 'active'"
                class="btn btn-warning"
                @click="closeJob"
            >
                Close Job
            </button>

            <span
                v-else
                class="badge bg-danger fs-6"
            >
                Job Closed
            </span>

        </div>
        <hr>

<h3>Applications Received</h3>

<table class="table table-bordered">

    <thead>

        <tr>

            <th>Student</th>
            <th>Course</th>
            <th>CGPA</th>
            <th>Status</th>
            <th>Action</th>

        </tr>

    </thead>

    <tbody>

        <tr
            v-for="application in applications"
            :key="application.application_id"
        >

            <td>{{ application.student_name }}</td>
            <td>{{ application.course }}</td>
            <td>{{ application.cgpa }}</td>
            <td>{{ application.status }}</td>

            <td>

                <button
                    class="btn btn-success btn-sm"
                    @click="router.push(`/application/${application.application_id}`)"
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
import { useRoute, useRouter } from "vue-router";

import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const route = useRoute();
const router = useRouter();

const job = ref({});
const applications = ref([]);

async function loadJob() {

    try {

        const response = await api.get(
            `/company/job/${route.params.id}`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        job.value = response.data;

    }
    

    catch (error) {

        console.log(error);

    }

}
async function loadApplications() {

    try {

        const response = await api.get(
            `/company/job/${route.params.id}/applications`,
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
async function closeJob() {

    try {

        await api.put(
            `/company/job/${job.value.id}/close`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        job.value.status = "closed";

    }

    catch (error) {

        console.log(error);

    }

}
onMounted(() => {

    loadJob();
    loadApplications();

});

</script>