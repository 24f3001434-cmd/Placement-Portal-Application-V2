<template>

    <Navbar />

    <div class="container mt-5">

        <div class="d-flex justify-content-between align-items-center mb-4">

            <h2>Students</h2>

            <input
                type="text"
                class="form-control w-25"
                placeholder="Search Student..."
                v-model="search"
            >

        </div>

        <div class="card shadow">

            <div class="card-body">

                <table class="table table-hover align-middle">

                    <thead class="table-dark">

                        <tr>

                            <th>Name</th>
                            <th>Roll No.</th>
                            <th>Course</th>
                            <th>CGPA</th>
                            <th>Applications</th>
                            <th>Placements</th>
                            <th>Action</th>
                            

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="student in filteredStudents"
                            :key="student.id"
                        >

                            <td>{{ student.name }}</td>
                            <td>{{ student.roll_number }}</td>
                            <td>{{ student.course }}</td>
                            <td>{{ student.cgpa }}</td>

                            <td>
                                <span class="badge bg-primary">
                                    {{ student.applications }}
                                </span>
                            </td>

                            <td>
                                <span
                                    class="badge"
                                    :class="student.placements > 0 ? 'bg-success' : 'bg-secondary'"
                                >
                                    {{ student.placements }}
                                </span>
                            </td>

                            <td>
                                <button
                                    class="btn btn-primary btn-sm"
                                    @click="$router.push(`/student/${student.id}`)"
                                >
                                    View
                                </button>
                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

    </div>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import api from "../services/api";
import Navbar from "../components/Navbar.vue";

const students = ref([]);

const search = ref("");

const filteredStudents = computed(() => {

    return students.value.filter(student =>

        student.name.toLowerCase().includes(search.value.toLowerCase()) ||

        student.roll_number.toLowerCase().includes(search.value.toLowerCase())

    );

});

async function loadStudents() {

    const response = await api.get("/students");

    students.value = response.data;

}

onMounted(() => {

    loadStudents();

});

</script>