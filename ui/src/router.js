import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import LoginView from "./views/LoginView.vue";
import NotFoundView from "./views/NotFoundView.vue";
import MonitorsView from "./views/MonitorsView.vue";
import MonitorDetailedView from "./views/MonitorDetailedView.vue";
import { useAuthenticationStore } from "./stores/authStore";

const routes = [
  {
    path: "/",
    component: HomeView,
  },
  {
    path: "/login",
    component: LoginView,
    beforeEnter(to, from, next) {
      const store = useAuthenticationStore();
      if (store.isAuthenticated) {
        next("/");
      } else {
        next();
      }
    },
  },
  {
    path: "/monitors",
    component: MonitorsView,
    beforeEnter(to, from, next) {
      const store = useAuthenticationStore();
      if (!store.isAuthenticated) {
        next("/login");
      } else {
        next();
      }
    },
  },
  {
    path: "/monitor/:id",
    component: MonitorDetailedView
  },
  {
    path: "/:pathMatch(.*)*",
    component: NotFoundView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
