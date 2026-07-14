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
                    <th>Interview Schedule</th>
                    <th>Feedback</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="application in applications"
                    :key="application.application_id"
                >

                    <td>{{ application.job_title }}</td>

                    <td>{{ application.company }}</td>

                    <td>

                        <span
                            class="badge bg-warning"
                            v-if="application.status==='applied'"
                        >
                            Applied
                        </span>

                        <span
                            class="badge bg-info"
                            v-else-if="application.status==='shortlisted'"
                        >
                            Shortlisted
                        </span>

                        <span
                            class="badge bg-primary"
                            v-else-if="application.status==='interview'"
                        >
                            Interview
                        </span>

                        <span
                            class="badge bg-success"
                            v-else-if="application.status==='selected'"
                        >
                            Selected
                        </span>

                        <span
                            class="badge bg-danger"
                            v-else
                        >
                            Rejected
                        </span>

                    </td>

                    <td>{{ application.applied_on }}</td>

                    <td>

                        <div v-if="application.interview_date">

                            {{ application.interview_date }}

                            <br>

                            <small class="text-muted">

                                {{ application.interview_mode }}

                            </small>

                        </div>

                        <span v-else>

                            --

                        </span>

                    </td>

                    <td>

                        <span v-if="application.feedback">

                            {{ application.feedback }}

                        </span>

                        <span v-else>

                            --

                        </span>

                    </td>

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