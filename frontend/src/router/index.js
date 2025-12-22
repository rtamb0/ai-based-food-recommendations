import { createRouter, createWebHistory } from "vue-router";

import Onboarding from "../views/Onboarding.vue";
import Result from "../views/Result.vue";

const routes = [
  {
    path: "/",
    name: "Onboarding",
    component: Onboarding,
  },
  {
    path: "/result",
    name: "Result",
    component: Result,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
