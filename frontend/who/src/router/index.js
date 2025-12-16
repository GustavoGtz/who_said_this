import { createRouter, createWebHistory } from "vue-router";
import Desktop from "@/views/Desktop.vue";
import Mobile from "@/views/Mobile.vue";

const routes = [
  { path: "/", redirect: "/desktop" },
  { path: "/desktop", component: Desktop },
  { path: "/mobile", component: Mobile }
];

export default createRouter({
  history: createWebHistory(),
  routes
});
