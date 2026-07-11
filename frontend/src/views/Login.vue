<template>
  <div>
    <h2>Placement Portal Login</h2>

    <input type="email" v-model="email" placeholder="Enter Email" />

    <br /><br />

    <input type="password" v-model="password" placeholder="Enter Password" />

    <br /><br />

    <select v-model="role">
      <option value="student">Student</option>
      <option value="company">Company</option>
      <option value="admin">Admin</option>
    </select>

    <br /><br />

    <button @click="login">Login</button>

    <p>{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";
import router from "../router";

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
