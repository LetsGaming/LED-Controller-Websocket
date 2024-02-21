import { createRouter, createWebHistory } from "@ionic/vue-router";
import { RouteRecordRaw } from "vue-router";

import MainPage from "@/views/MainPage.vue";

// Import LedControlPanel component
import LedControlPanel from "@/components/LedControlPanel.vue";

// Add the route in your router setup
const routes: Array<RouteRecordRaw> = [
  // Other routes...
  {
    path: "/",
    redirect: "",
  },
  {
    path: "",
    component: MainPage,
    children: [
      {
        path: "led-control-panel/:controllerId",
        name: "LedControlPanel",
        component: LedControlPanel,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
