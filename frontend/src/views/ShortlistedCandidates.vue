<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/company/dashboard')"
        >
            ← Back
        </button>

        <h2>Shortlisted Candidates</h2>

        <hr>

        <table class="table table-bordered">

            <thead>

                <tr>

                    <th>Student</th>
                    <th>Job</th>
                    <th>Course</th>
                    <th>CGPA</th>

                    <th>Action</th>

                </tr>

            </thead>

            <tbody>

                <tr v-if="shortlisted.length === 0">

                    <td colspan="5" class="text-center">
                        No shortlisted candidates.
                    </td>

                </tr>

                <tr
                    v-for="student in shortlisted"
                    :key="student.application_id"
                >

                    <td>{{ student.student_name }}</td>
                    <td>{{ student.job_title }}</td>
                    <td>{{ student.course }}</td>
                    <td>{{ student.cgpa }}</td>

                    <td>

                        <button
                            class="btn btn-primary btn-sm"
                            @click="router.push(`/company/interview/${student.application_id}`)"
                        >
                            Schedule Interview
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</template>

<script setup>

import Navbar from "../components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const shortlisted = ref([]);

async function loadShortlisted() {

    try {

        const response = await api.get(

            "/company/shortlisted",

            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }

        );

        shortlisted.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(loadShortlisted);

</script>