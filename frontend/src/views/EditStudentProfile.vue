<template>

    <Navbar />

    <div class="container mt-5">

        <h2>Edit Student Profile</h2>

        <hr>

        <form @submit.prevent="updateProfile">

            <div class="mb-3">

                <label class="form-label">Name</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="student.name"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Course</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="student.course"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">CGPA</label>

                <input
                    type="number"
                    step="0.01"
                    class="form-control"
                    v-model="student.cgpa"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Roll Number</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="student.roll_number"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Skills</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="student.skills"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Experience (Years)</label>

                <input
                    type="number"
                    step="0.1"
                    class="form-control"
                    v-model="student.experience"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Resume</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="student.resume"
                    placeholder="resume.pdf"
                >

            </div>

            <button
                type="submit"
                class="btn btn-success me-2"
            >
                Save Changes
            </button>

            <button
                type="button"
                class="btn btn-secondary"
                @click="router.push('/student/profile')"
            >
                Cancel
            </button>

        </form>

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

async function updateProfile() {

    try {

        await api.put(
            "/student/profile",
            student.value,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        alert("Profile updated successfully!");

        router.push("/student/profile");

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(loadProfile);

</script>