<template>
    <Navbar />
    <div class="container mt-5">

        <h2>Company Registration</h2>
        <hr>

        <input
            class="form-control mb-3"
            v-model="company.email"
            placeholder="Email"
        >

        <input
            type="password"
            class="form-control mb-3"
            v-model="company.password"
            placeholder="Password"
        >

        <input
            class="form-control mb-3"
            v-model="company.company_name"
            placeholder="Company Name"
        >

        <input
            class="form-control mb-3"
            v-model="company.website"
            placeholder="Website"
        >

        <input
            class="form-control mb-3"
            v-model="company.industry"
            placeholder="Industry"
        >

        <textarea
            class="form-control mb-3"
            v-model="company.description"
            placeholder="Description"
        ></textarea>

        <input
            class="form-control mb-3"
            v-model="company.hr_contact"
            placeholder="HR Contact"
        >

        <button
            class="btn btn-primary"
            @click="registerCompany"
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

const company = ref({
    email: "",
    password: "",
    company_name: "",
    website: "",
    industry: "",
    description: "",
    hr_contact: ""
});

async function registerCompany() {

    try {

        const response = await api.post(
            "/register/company",
            company.value
        );

        message.value = response.data.message;

        alert("Registration Successful. Wait for Admin Approval.");

        router.push("/login");

    }

    catch (error) {

        message.value = error.response.data.message;

    }

}

</script>