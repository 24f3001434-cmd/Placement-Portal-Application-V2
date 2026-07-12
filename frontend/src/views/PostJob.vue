<template>

    <Navbar />

    <div class="container mt-5">

        <h2>Company Dashboard</h2>

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
                    @click="router.push('/company/applications')"
                >

                    <h5>Total Applications</h5>

                    <h3>{{ totalApplications }}</h3>

                </div>

            </div>

            <div class="col-md-3">

                <div class="card p-4 text-center">

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

async function loadDashboard() {

    try {

        const response = await api.get("/company/jobs", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`
            }
        });

        totalJobs.value = response.data.length;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadDashboard();

});

</script>