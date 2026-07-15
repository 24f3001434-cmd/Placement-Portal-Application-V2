<template>

    <Navbar />

    <div class="container mt-5">

        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2>Student Details</h2>

            <button
                class="btn btn-secondary"
                @click="$router.back()"
            >
                Back
            </button>

        </div>

        <div class="card shadow mb-4">

            <div class="card-body">

                <div class="row">

                    <div class="col-md-6">

                        <p><strong>Name:</strong> {{ student.name }}</p>
                        <p><strong>Roll No:</strong> {{ student.roll_number }}</p>
                        <p><strong>Course:</strong> {{ student.course }}</p>
                        <p><strong>CGPA:</strong> {{ student.cgpa }}</p>

                    </div>

                    <div class="col-md-6">

                        <p><strong>Skills:</strong> {{ student.skills }}</p>
                        <p><strong>Experience:</strong> {{ student.experience }}</p>
                        <p><strong>Resume:</strong> {{ student.resume || "Not Uploaded" }}</p>

                    </div>

                </div>

            </div>

        </div>

        <div class="card shadow mb-4">

            <div class="card-header bg-primary text-white">

                Applications

            </div>

            <div class="card-body">

                <table class="table table-hover">

                    <thead>

                        <tr>

                            <th>Company</th>
                            <th>Job</th>
                            <th>Status</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="application in student.applications"
                            :key="application.job_title"
                        >

                            <td>{{ application.company }}</td>

                            <td>{{ application.job_title }}</td>

                            <td>

                                <span
                                    class="badge"
                                    :class="badge(application.status)"
                                >

                                    {{ application.status }}

                                </span>

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

        <div class="card shadow">

            <div class="card-header bg-success text-white">

                Placements

            </div>

            <div class="card-body">

                <table class="table table-hover">

                    <thead>

                        <tr>

                            <th>Company</th>
                            <th>Job</th>
                            <th>Placement Date</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="placement in student.placements"
                            :key="placement.job_title"
                        >

                            <td>{{ placement.company }}</td>

                            <td>{{ placement.job_title }}</td>

                            <td>{{ placement.placement_date }}</td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

    </div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const route = useRoute();

const student = ref({

    applications: [],
    placements: []

});

function badge(status){

    if(status==="selected") return "bg-success";

    if(status==="rejected") return "bg-danger";

    if(status==="interview") return "bg-warning";

    return "bg-primary";

}

async function loadStudent(){

    const response = await api.get(

        `/student/${route.params.id}`

    );

    student.value=response.data;

}

onMounted(loadStudent);

</script>