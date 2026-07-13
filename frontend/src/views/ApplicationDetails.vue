<template>

    <Navbar />

    <div class="container mt-5">

        <button
            class="btn btn-secondary mb-3"
            @click="router.push('/company/job/' + application.job_position_id)"
        >
            ← Back
        </button>

        <h2>Application Details</h2>

        <hr>

        <div class="card p-4">

            <p><strong>Name:</strong> {{ application.student_name }}</p>

            <p><strong>Course:</strong> {{ application.course }}</p>

            <p><strong>CGPA:</strong> {{ application.cgpa }}</p>

            <p><strong>Skills:</strong> {{ application.skills }}</p>

            <p><strong>Experience:</strong> {{ application.experience }}</p>

            <p><strong>Status:</strong> {{ application.status }}</p>

            <hr>

            <button
                class="btn btn-success me-2"
                @click="shortlistStudent"
            >
                Shortlist
            </button>

            <button
                class="btn btn-danger"
                @click="rejectStudent"
            >
                Reject
            </button>

        </div>

    </div>

</template>

<script setup>

import { ref,onMounted } from "vue";
import { useRoute,useRouter } from "vue-router";

import api from "../services/api";
import Navbar from "../components/Navbar.vue";

const route = useRoute();
const router = useRouter();

const application = ref({});

async function loadApplication(){

    try{

        const response = await api.get(

            `/application/${route.params.id}`,

            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("access_token")}`
                }
            }

        );

        application.value=response.data;

    }

    catch(error){

        console.log(error);

    }

}
async function shortlistStudent() {

    try {

        const response = await api.put(

            `/application/${route.params.id}/shortlist`,

            {},

            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("access_token")}`
                }
            }

        );

        alert(response.data.message);

        loadApplication();

    }

    catch(error){

        console.log(error);

    }

}


async function rejectStudent() {

    try {

        const response = await api.put(

            `/application/${route.params.id}/reject`,

            {},

            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("access_token")}`
                }
            }

        );

        alert(response.data.message);

        loadApplication();

    }

    catch(error){

        console.log(error);

    }

}

onMounted(()=>{

    loadApplication();

});

</script>