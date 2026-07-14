<template>

    <Navbar />

    <div class="container mt-5">

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

    </div>

</template>

<script setup>

import { useRouter } from "vue-router";

import Navbar from "../components/Navbar.vue";

const router = useRouter();

</script>