<template>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">

        <div class="container">

            <a
                class="navbar-brand fw-bold"
                style="cursor:pointer;"
                href="#"
                @click.prevent="goDashboard"
            >
                Placement Portal
            </a>

            <div class="ms-auto">

                <button
                    class="btn btn-outline-light me-2"
                    @click="goDashboard"
                >
                    Dashboard
                </button>

                <button
                    class="btn btn-danger"
                    @click="logout"
                >
                    Logout
                </button>

            </div>

        </div>

    </nav>

</template>

<script setup>

import { useRouter } from "vue-router";

const router = useRouter();

const role = localStorage.getItem("role");

function goDashboard() {

    if (role === "admin") {

        router.push("/admin/dashboard");

    }

    else if (role === "company") {

        router.push("/company/dashboard");

    }

    else if (role === "student") {

        router.push("/student/dashboard");

    }

}

function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("role");

    router.push("/login");

}

</script>