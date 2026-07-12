<template>
    <Navbar />
    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/admin/dashboard')"
        >
            ← Back
        </button>

        <h2>Job Postings</h2>

        <div class="row mb-3">

            <div class="col-md-6">

                <input
                    type="text"
                    class="form-control"
                    placeholder="Search Job..."
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
                    <td>{{ job.company }}</td>
                    <td>{{ job.status }}</td>

                    <td>

                        <button
                            class="btn btn-primary btn-sm"
                            @click="router.push(`/job/${job.id}`)"
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
const search = ref("");

async function loadJobs() {

    try {

        const response = await api.get("/jobs", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        jobs.value = response.data.filter(job =>
            job.title.toLowerCase().includes(search.value.toLowerCase())
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