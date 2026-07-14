<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/student/dashboard')"
        >
            ← Back
        </button>

        <h2>Placement History</h2>

        <hr>

        <table class="table table-bordered">

            <thead>

                <tr>

                    <th>Company</th>
                    <th>Job</th>
                    <th>Placement Date</th>
                    <th>Offer Letter</th>

                </tr>

            </thead>

            <tbody>

                <tr v-if="placements.length === 0">

                    <td colspan="4" class="text-center">

                        No placements yet.

                    </td>

                </tr>

                <tr
                    v-for="placement in placements"
                    :key="placement.id"
                >

                    <td>{{ placement.company }}</td>

                    <td>{{ placement.job_title }}</td>

                    <td>{{ placement.placement_date }}</td>

                    <td>

                        <button
                            class="btn btn-success btn-sm"
                            @click="downloadOfferLetter(placement.id)"
                        >
                            Download
                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</template>

<script setup>

import Navbar from "../components/Navbar.vue";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const placements = ref([]);

async function loadPlacements() {

    try {

        const response = await api.get(

            "/student/placements",

            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`
                }
            }

        );

        placements.value = response.data;

    }

    catch (error) {

        console.log(error);

    }

}
async function downloadOfferLetter(id){

    window.open(

        `http://127.0.0.1:5000/student/offer-letter/${id}?token=${localStorage.getItem("access_token")}`,

        "_blank"

    );

}
onMounted(loadPlacements);

</script>