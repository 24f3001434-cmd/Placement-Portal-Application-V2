<template>
    <div class="container mt-5">
        <button
            class="btn btn-secondary mb-3"
            @click="goBack"
        >
            ← Back
        </button>
        <h2>Companies</h2>
        <div class="row mb-3">

            <div class="col-md-6">

                <input
                    type="text"
                    class="form-control"
                    placeholder="Search Company..."
                    v-model="search"
                    @input="loadCompanies"
                >

            </div>

        </div>
        <hr>

        <table class="table table-bordered">

            <thead>

                <tr>
                    <th>Company Name</th>
                    <th>Industry</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>

            </thead>

            <tbody>

                <tr v-for="company in companies" :key="company.id">

                    <td>{{ company.name }}</td>

                    <td>{{ company.industry }}</td>

                    <td>{{ company.status }}</td>

                    <td>
                        <button
                            class="btn btn-primary btn-sm"
                            @click="router.push(`/company/${company.id}`)"
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

const companies = ref([]);
const search = ref("");
const router = useRouter();

async function loadCompanies() {

    try {

        const response = await api.get(`/companies?search=${search.value}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
        });

        companies.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadCompanies();

});

</script>