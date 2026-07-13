<template>

    <Navbar />

    <div class="container mt-5">

        <h2>Edit Company Profile</h2>

        <hr>

        <form @submit.prevent="updateProfile">

            <div class="mb-3">

                <label class="form-label">Company Name</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="company.company_name"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Website</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="company.website"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Industry</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="company.industry"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">HR Contact</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="company.hr_contact"
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Description</label>

                <textarea
                    class="form-control"
                    rows="4"
                    v-model="company.description"
                ></textarea>

            </div>

            <button
                class="btn btn-success me-2"
                type="submit"
            >
                Save Changes
            </button>

            <button
                type="button"
                class="btn btn-secondary"
                @click="router.push('/company/profile')"
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

const company = ref({});

async function loadProfile() {

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

async function updateProfile() {

    try {

        await api.put(
            "/company/profile",
            company.value,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }
        );

        alert("Profile updated successfully!");

        router.push("/company/profile");

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(loadProfile);

</script>