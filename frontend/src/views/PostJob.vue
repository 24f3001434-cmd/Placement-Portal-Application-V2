<template>

    <Navbar />

    <div class="container mt-5">

        <h2>Post New Job</h2>

        <hr>

        <form @submit.prevent="postJob">

            <div class="mb-3">

                <label class="form-label">Job Title</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="job.title"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Description</label>

                <textarea
                    class="form-control"
                    rows="4"
                    v-model="job.description"
                    required
                ></textarea>

            </div>

            <div class="mb-3">

                <label class="form-label">Eligibility</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="job.eligibility"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Skills</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="job.skills"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Experience (Years)</label>

                <input
                    type="number"
                    step="0.1"
                    class="form-control"
                    v-model="job.experience"
                    required
                >

            </div>

            <div class="mb-3">

                <label class="form-label">Salary Package (LPA)</label>

                <input
                    type="number"
                    step="0.1"
                    class="form-control"
                    v-model="job.salary_package"
                    required
                >

            </div>

            <button
                type="submit"
                class="btn btn-success me-2"
            >
                Post Job
            </button>

            <button
                type="button"
                class="btn btn-secondary"
                @click="router.push('/company/dashboard')"
            >
                Cancel
            </button>

        </form>

    </div>

</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const router = useRouter();

const job = ref({

    title: "",
    description: "",
    eligibility: "",
    skills: "",
    experience: "",
    salary_package: ""

});

async function postJob() {

    try {

        await api.post(

            "/post-job",

            job.value,

            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }

        );

        alert("Job posted successfully!");

        router.push("/company/jobs");

    }

    catch (error) {

        console.log(error);

        alert("Failed to post job.");

    }

}

</script>