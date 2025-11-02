import { createRouter } from "@ionic/vue-router";
import { RouteRecordRaw, createWebHashHistory } from "vue-router";

const MainWrapper = () => import("@/views/MainWrapper.vue");
// Import LedControlPanel component
const LedControlPanel = () => import("@/components/LedControlPanel.vue");

// Add the route in your router setup
const routes: Array<RouteRecordRaw> = [
  // Other routes...
  {
    path: "/",
    redirect: "",
  },
  {
    path: "",
    component: MainWrapper,
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
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
