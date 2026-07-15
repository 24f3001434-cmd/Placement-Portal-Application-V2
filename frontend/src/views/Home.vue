<template>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">

        <div class="container">

            <span class="navbar-brand fw-bold">
                Placement Portal
            </span>

            <div class="ms-auto">

                <button
                    class="btn btn-outline-light me-2"
                    @click="$router.push('/login')"
                >
                    Login
                </button>

                <button
                    class="btn btn-outline-success me-2"
                    @click="$router.push('/register/student')"
                >
                    Students
                </button>

                <button
                    class="btn btn-outline-primary"
                    @click="$router.push('/register/company')"
                >
                    Employers
                </button>

            </div>

        </div>

    </nav>

    <div
        class="container d-flex justify-content-center align-items-center"
        style="min-height:85vh;"
    >

        <div class="text-center">

            <h1 class="display-3 fw-bold">
                Placement Portal
            </h1>

            <p class="lead mt-4">

                A modern Placement Management System for
                Students, Companies and Administrators.

            </p>

            <p class="text-muted">

                Built using Vue.js, Flask, JWT, Celery,
                Redis and SQLite.

            </p>

            <button
                class="btn btn-primary btn-lg mt-3"
                @click="$router.push('/login')"
            >
                Get Started
            </button>

        </div>

    </div>

</template>