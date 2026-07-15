<template>

<Navbar />

<div class="container d-flex justify-content-center align-items-center"
style="min-height:85vh;">

<div class="card shadow p-4" style="width:420px;">

<h2 class="text-center mb-4">
Placement Portal Login
</h2>

<input
class="form-control mb-3"
type="email"
v-model="email"
placeholder="Email"
/>

<input
class="form-control mb-3"
type="password"
v-model="password"
placeholder="Password"
/>

<div class="mb-3">

    <label class="form-label fw-bold">

        Login As

    </label>

    <div
        class="btn-group w-100"
        role="group"
    >

        <button
            class="btn"
            :class="role==='student'
                ? 'btn-primary'
                : 'btn-outline-primary'"
            @click="role='student'"
        >

            Student

        </button>

        <button
            class="btn"
            :class="role==='company'
                ? 'btn-success'
                : 'btn-outline-success'"
            @click="role='company'"
        >

            Company

        </button>

        <button
            class="btn"
            :class="role==='admin'
                ? 'btn-dark'
                : 'btn-outline-dark'"
            @click="role='admin'"
        >

            Admin

        </button>

    </div>

</div>

<button
class="btn btn-primary w-100 mb-3"
@click="login"
>

Login

</button>

<div class="d-grid gap-2">

<button
class="btn btn-outline-primary"
@click="$router.push('/register/company')"
>

Register as Company

</button>

<button
class="btn btn-outline-success"
@click="$router.push('/register/student')"
>

Register as Student

</button>

</div>

<p
v-if="message"
class="text-center mt-3 text-danger"
>

{{ message }}

</p>

</div>

</div>

</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";
import router from "../router";
import Navbar from "../components/Navbar.vue";

const email = ref("");
const password = ref("");
const role = ref("student");
const message = ref("");

async function login() {
    try {

        const response = await api.post(`/login/${role.value}`, {
            email: email.value,
            password: password.value,
        });

        message.value = response.data.message;

        localStorage.setItem(
            "access_token",
            response.data.access_token
        );

        localStorage.setItem(
            "role",
            response.data.role
        );

        if (response.data.role === "student") {
            router.push("/student/dashboard");
        } else if (response.data.role === "company") {
            router.push("/company/dashboard");
        } else if (response.data.role === "admin") {
            router.push("/admin/dashboard");
        }

    } catch (error) {

        console.log("FULL ERROR:", error);

        if (error.response) {
            message.value = error.response.data.message;
        } else {
            message.value = error.message;
        }

    }
}
</script>
