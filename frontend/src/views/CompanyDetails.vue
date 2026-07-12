<template>
    <Navbar />
    <div class="container mt-5">
        <button
            class="btn btn-secondary mb-3"
            @click="goBack"
        >
            ← Back
        </button>

        <h2>Company Details</h2>
        <hr>

        <div class="card p-4">

            <h4>{{ company.name }}</h4>

            <p><strong>Website:</strong> {{ company.website }}</p>

            <p><strong>Industry:</strong> {{ company.industry }}</p>

            <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>

            <p><strong>Description:</strong> {{ company.description }}</p>

            <p><strong>Status:</strong> {{ company.status }}</p>

            <div class="mt-3">

                <button
                    v-if="company.status === 'pending' || company.status === 'deactivated'"
                    class="btn btn-success me-2"
                    @click="approveCompany"
                >
                    Approve
                </button>

                <button
                    v-if="company.status === 'approved'"
                    class="btn btn-warning me-2"
                    @click="deactivateCompany"
                >
                    Deactivate
                </button>

                <button
                    class="btn btn-danger"
                    @click="removeCompany"
                >
                    Remove
                </button>

            </div>

        </div>

    </div>
</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import Navbar from "../components/Navbar.vue";
const route = useRoute();
const router = useRouter();

const company = ref({});

async function loadCompany() {

    try {

        const response = await api.get(`/company/${route.params.id}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
        });

        company.value = response.data;

    } catch (error) {

        console.log(error);

    }

}

async function approveCompany() {

    try {

        await api.put(
            `/approve-company/${company.value.id}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            }
        );

        alert("Company Approved Successfully");

        loadCompany();

    } catch (error) {

        console.log(error);

    }

}


async function deactivateCompany() {

    try {

        await api.put(
            `/deactivate-company/${company.value.id}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            }
        );

        alert("Company Deactivated Successfully");

        loadCompany();

    } catch (error) {

        console.log(error);

    }

}
async function removeCompany() {

    try {

        await api.delete(
            `/remove-company/${company.value.id}`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            }
        );

        alert("Company Removed Successfully");

        window.location.href = "/companies";

    } catch (error) {

        console.log(error);

    }

}
function goBack() {

    router.push("/companies");

}
onMounted(() => {

    loadCompany();

});

</script>