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

            <div v-if="application.interview_date">
                <p><strong>Interview Date:</strong> {{ application.interview_date }}</p>
                <p><strong>Interview Mode:</strong> {{ application.interview_mode }}</p>
            </div>

            <div
                v-if="application.feedback"
                class="alert alert-warning mt-3"
            >
                <strong>Feedback:</strong><br>
                {{ application.feedback }}
            </div>

            <hr>

            <!-- Applied -->

            <div v-if="application.status === 'applied'">

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

            <!-- Shortlisted -->

            <div v-else-if="application.status === 'shortlisted'">

                <div class="mb-3">

                    <label class="form-label">
                        Interview Date
                    </label>

                    <input
                        type="datetime-local"
                        class="form-control"
                        v-model="interview.interview_date"
                    >

                </div>

                <div class="mb-3">

                    <label class="form-label">
                        Interview Mode
                    </label>

                    <select
                        class="form-control"
                        v-model="interview.interview_mode"
                    >

                        <option>Online</option>
                        <option>Offline</option>

                    </select>

                </div>

                <div class="mb-3">

                    <label class="form-label">
                        Feedback
                    </label>

                    <textarea
                        class="form-control"
                        rows="3"
                        v-model="interview.feedback"
                        placeholder="Enter feedback"
                    ></textarea>

                </div>

                <button
                    class="btn btn-primary"
                    @click="scheduleInterview"
                >
                    Schedule Interview
                </button>

            </div>

            <!-- Interview -->

            <div v-else-if="application.status === 'interview'">

                <div class="mb-3">

                    <label class="form-label">
                        Feedback
                    </label>

                    <textarea
                        class="form-control"
                        rows="3"
                        v-model="feedback"
                        placeholder="Enter feedback"
                    ></textarea>

                </div>

                <button
                    class="btn btn-success me-2"
                    @click="selectStudent"
                >
                    Select
                </button>

                <button
                    class="btn btn-danger"
                    @click="rejectStudent"
                >
                    Reject
                </button>

            </div>

            <!-- Reject -->

            <div v-if="showReject" class="mt-4">

                <textarea
                    class="form-control"
                    rows="4"
                    v-model="feedback"
                    placeholder="Enter feedback"
                ></textarea>

                <button
                    class="btn btn-danger mt-3"
                    @click="rejectStudent"
                >
                    Confirm Reject
                </button>

            </div>

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

const showReject = ref(false);

const feedback = ref("");

const interview = ref({

    interview_date:"",
    interview_mode:"Online",
    feedback:""
});

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

async function shortlistStudent(){

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

async function scheduleInterview(){

    const response = await api.put(

        `/company/application/${route.params.id}/interview`,

        interview.value,

        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            }
        }

    );

    alert(response.data.message);

    loadApplication();

}

async function selectStudent(){

    const response = await api.put(

        `/application/${route.params.id}/select`,

        {
            feedback: feedback.value
        },

        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            }
        }

    );

    alert(response.data.message);

    loadApplication();

}

async function rejectStudent(){

    const response = await api.put(

        `/application/${route.params.id}/reject`,

        {
            feedback:feedback.value
        },

        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            }
        }

    );

    alert(response.data.message);

    showReject.value=false;

    loadApplication();

}

onMounted(()=>{

    loadApplication();

});

</script>