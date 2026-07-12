<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/student/dashboard')"
        >
            ← Back
        </button>

        <h2>Available Jobs</h2>

        <div class="row mb-3">

            <div class="col-md-6">

                <input
                    type="text"
                    class="form-control"
                    placeholder="Search Job by position , Company Name"
                    v-model="search"
                    @input="loadJobs"
                >

            </div>

        </div>

        <hr>

        <table class="table table-bordered">

            <thead>

                <tr>
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Salary</th>
                    <th>Action</th>
                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="job in jobs"
                    :key="job.id"
                >

                    <td>{{ job.title }}</td>
                    <td>{{ job.company }}</td>
                    <td>{{ job.salary_package }}</td>

                    <td>

                        <button
                            class="btn btn-primary btn-sm"
                            @click="router.push(`/student/job/${job.id}`)"
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

import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const router = useRouter();

const jobs = ref([]);
const search = ref("");

async function loadJobs() {

    try {

        const response = await api.get("/student/jobs", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        const keyword = search.value.toLowerCase();

        jobs.value = response.data.filter(job =>
            job.title.toLowerCase().includes(keyword) ||
            job.company.toLowerCase().includes(keyword)
        );

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadJobs();

});

</script>