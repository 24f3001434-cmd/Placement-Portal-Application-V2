import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import Companies from "../views/Companies.vue";
import CompanyDetails from "../views/CompanyDetails.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/student/dashboard",
      name: "StudentDashboard",
      component: StudentDashboard,
    },
    {
      path: "/company/dashboard",
      name: "CompanyDashboard",
      component: CompanyDashboard,
    },
    {
      path: "/admin/dashboard",
      name: "AdminDashboard",
      component: AdminDashboard,
    },
    {
      path: "/companies",
      name: "Companies",
      component: Companies,
    },
    {
      path: "/company/:id",
      name: "CompanyDetails",
      component: CompanyDetails,
    },
  ],
});

export default router;
