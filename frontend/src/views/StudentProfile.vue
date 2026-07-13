<template>

    <Navbar />

    <div class="container mt-5">

        <div class="d-flex justify-content-between align-items-center">

            <h2>Student Profile</h2>

            <button
                class="btn btn-secondary"
                @click="router.push('/student/dashboard')"
            >
                Dashboard
            </button>

        </div>

        <hr>

        <div class="card p-4">

            <p><strong>Name:</strong> {{ student.name }}</p>

            <p><strong>Course:</strong> {{ student.course }}</p>

            <p><strong>CGPA:</strong> {{ student.cgpa }}</p>

            <p><strong>Roll Number:</strong> {{ student.roll_number }}</p>

            <p><strong>Skills:</strong> {{ student.skills }}</p>

            <p><strong>Experience:</strong> {{ student.experience }} years</p>

            <p><strong>Resume:</strong> {{ student.resume }}</p>

            <button
                class="btn btn-primary mt-3"
                @click="router.push('/student/profile/edit')"
            >
                Edit Profile
            </button>

        </div>

    </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const router = useRouter();

const student = ref({});

async function loadProfile() {

    try {

        const response = await api.get(
            "/student/profile",
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        student.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(loadProfile);

</script>