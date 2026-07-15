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
import AppliedJobs from "../views/AppliedJobs.vue";
import CompanyProfile from "../views/CompanyProfile.vue";
import EditCompanyProfile from "../views/EditCompanyProfile.vue";
import StudentProfile from "../views/StudentProfile.vue";
import EditStudentProfile from "../views/EditStudentProfile.vue";
import ShortlistedCandidates from "../views/ShortlistedCandidates.vue";
import StudentPlacements from "../views/StudentPlacements.vue";
import Students from "../views/Students.vue";
import StudentDetails from "../views/StudentDetails.vue";
import Home from "../views/Home.vue";



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: Home,
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
      meta: { role: "student" }
    },
    {
      path: "/company/dashboard",
      name: "CompanyDashboard",
      component: CompanyDashboard,
      meta: { role: "company" }
    },
    {
      path: "/admin/dashboard",
      name: "AdminDashboard",
      component: AdminDashboard,
      meta: { role: "admin" }
    },
    {
      path: "/companies",
      name: "Companies",
      component: Companies,
      meta: { role: "admin" }
    },
    {
      path: "/students",
      component: Students,
      meta: { role: "admin" }
    },
    {
      path: "/company/:id",
      name: "CompanyDetails",
      component: CompanyDetails,
      meta: { role: "admin" }
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
      meta: { role: "admin" }
    },
    {
      path: "/job/:id",
      component: JobDetails,
      meta: { role: "admin" }
    },
    {
      path: "/student/jobs",
      component: StudentJobs,
      meta: { role: "student" }
    },
    {
      path: "/student/job/:id",
      component: StudentJobDetails,
      meta: { role: "student" }
    },
    {
      path: "/post-job",
      component: PostJob,
      meta: { role: "company" }
    },
    {
      path: "/company/jobs",
      component: CompanyJobs,
      meta: { role: "company" }
    },
    {
      path: "/company/job/:id",
      component: CompanyJobDetails,
      meta: { role: "company" }
    },
    {
      path:"/application/:id",
      component:ApplicationDetails,
      meta: { role: "company" }
    },
    {
      path: "/student/applications",
      component: AppliedJobs,
      meta: { role: "student" }
    },
    {
      path: "/company/profile",
      component: CompanyProfile,
      meta: { role: "company" }
    },
    {
      path: "/company/profile/edit",
      component: EditCompanyProfile,
      meta: { role: "company" }
    },
    {
      path: "/student/profile",
      component: StudentProfile,
      meta: { role: "student" }
    },
    {
      path: "/student/profile/edit",
      component: EditStudentProfile,
      meta: { role: "student" }
    },
    {
      path: "/company/shortlisted",
      component: ShortlistedCandidates,
      meta: { role: "company" }
    },
    {
      path: "/student/placements",
      component: StudentPlacements,
      meta: { role: "student" }
    },
    {
      path: "/student/:id",
      component: StudentDetails,
      meta: { role: "admin" }
    },
  ],
});
router.beforeEach((to) => {

    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    if (!to.meta.role) {
        return true;
    }

    if (!token) {
        return "/login";
    }

    if (role !== to.meta.role) {
        return "/";
    }

    return true;

});
export default router;