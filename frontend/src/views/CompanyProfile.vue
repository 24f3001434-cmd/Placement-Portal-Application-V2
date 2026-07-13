<template>

    <Navbar />

    <div class="container mt-5">

        <div class="d-flex justify-content-between align-items-center">

            <h2>Company Profile</h2>

            <button
                class="btn btn-secondary"
                @click="router.push('/company/dashboard')"
            >
                Dashboard
            </button>

        </div>

        <hr>

        <div class="card p-4">

            <p><strong>Company Name:</strong> {{ company.company_name }}</p>

            <p><strong>Website:</strong> {{ company.website }}</p>

            <p><strong>Industry:</strong> {{ company.industry }}</p>

            <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>

            <p><strong>Description:</strong> {{ company.description }}</p>

            <p><strong>Approval:</strong> {{ company.approval }}</p>

            <button
                class="btn btn-primary mt-3"
                @click="router.push('/company/profile/edit')"
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

const company = ref({});

async function loadProfile() {

    try {

        const response = await api.get(
            "/company/profile",
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        company.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadProfile();

});

</script>