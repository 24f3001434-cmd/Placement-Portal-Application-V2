import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";
import CompanyRegister from "../views/CompanyRegister.vue";
import StudentRegister from "../views/StudentRegister.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import Companies from "../views/Companies.vue";
import Jobs from "../views/Jobs.vue";
import JobDetails from "../views/JobDetails.vue";
import CompanyDetails from "../views/CompanyDetails.vue";
import StudentJobs from "../views/StudentJobs.vue";
import StudentJobDetails from "../views/StudentJobDetails.vue";
import PostJob from "../views/PostJob.vue";
import CompanyJobs from "../views/CompanyJobs.vue";
import CompanyJobDetails from "../views/CompanyJobDetails.vue";
import ApplicationDetails from "../views/ApplicationDetails.vue";

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
    {
      path: "/register/company",
      component: CompanyRegister,
    },
    {
      path: "/register/student",
      component: StudentRegister,
    },
    {
      path: "/jobs",
      component: Jobs,
    },
    {
      path: "/job/:id",
      component: JobDetails,
    },
    {
      path: "/student/jobs",
      component: StudentJobs,
    },
    {
      path: "/student/job/:id",
      component: StudentJobDetails,
    },
    {
      path: "/post-job",
      component: PostJob,
    },
    {
      path: "/company/jobs",
      component: CompanyJobs,
    },
    {
      path: "/company/job/:id",
      component: CompanyJobDetails,
    },
    {
      path:"/application/:id",
      component:ApplicationDetails,
    }
  ],
});

export default router;
