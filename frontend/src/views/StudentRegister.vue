<template>
    <Navbar />
    <div class="container mt-5">

        <h2>Student Registration</h2>
        <hr>

        <input
            class="form-control mb-3"
            v-model="student.email"
            placeholder="Email"
        >

        <input
            type="password"
            class="form-control mb-3"
            v-model="student.password"
            placeholder="Password"
        >

        <input
            class="form-control mb-3"
            v-model="student.name"
            placeholder="Name"
        >

        <input
            class="form-control mb-3"
            v-model="student.course"
            placeholder="Course"
        >

        <input
            type="number"
            class="form-control mb-3"
            v-model="student.cgpa"
            placeholder="CGPA"
        >

        <input
            class="form-control mb-3"
            v-model="student.roll_number"
            placeholder="Roll Number"
        >

        <input
            class="form-control mb-3"
            v-model="student.skills"
            placeholder="Skills"
        >

        <textarea
            class="form-control mb-3"
            v-model="student.experience"
            placeholder="Experience"
        ></textarea>

        <button
            class="btn btn-primary"
            @click="registerStudent"
        >
            Register
        </button>

        <p class="mt-3">{{ message }}</p>

    </div>
</template>

<script setup>

import { ref } from "vue";
import api from "../services/api";
import router from "../router";
import Navbar from "../components/Navbar.vue";

const message = ref("");

const student = ref({
    email: "",
    password: "",
    name: "",
    course: "",
    cgpa: "",
    roll_number: "",
    skills: "",
    experience: ""
});

async function registerStudent() {

    try {

        const response = await api.post(
            "/register/student",
            student.value
        );

        message.value = response.data.message;

        alert("Student Registered Successfully");

        router.push("/login");

    }

    catch (error) {

        message.value = error.response.data.message;

    }

}

</script>