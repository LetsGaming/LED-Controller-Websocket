<template>
  <!-- Side Menu -->
  <ion-menu content-id="main-content">
    <ion-header>
      <ion-toolbar color="primary">
        <ion-title>Controllers</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <!-- Connected Controllers Card -->
      <IonCard>
        <IonCardHeader class="ion-text-center">
          <IonCardTitle>Connected Controllers</IonCardTitle>
        </IonCardHeader>

        <IonCardContent>
          <IonButton
            expand="block"
            @click="getConnectedControllers"
            :disabled="isLoading"
          >
            <ion-spinner v-if="isLoading" name="dots"></ion-spinner>
            <span v-else>Get Controllers</span>
          </IonButton>
        </IonCardContent>
      </IonCard>

      <!-- Controller List -->
      <IonList>
        <ion-menu-toggle
          ><IonChip
            @click="clickController('all')"
            class="controllerChip"
            color="secondary"
          >
            All Controllers
          </IonChip></ion-menu-toggle
        >

        <!-- Connected Controllers -->
        <template v-if="connectedControllers.length > 0">
          <ion-menu-toggle
            ><IonChip
              v-for="(controller, index) in connectedControllers"
              :key="index"
              @click="clickController(controller.id)"
              class="controllerChip"
              color="tertiary"
            >
              {{ controller.name }}
            </IonChip></ion-menu-toggle
          >
        </template>

        <!-- No controllers message -->
        <p v-else class="ion-text-center no-controllers-text">
          No connected controllers
        </p>
      </IonList>
    </ion-content>
  </ion-menu>

  <!-- Main Content -->
  <ion-page id="main-content">
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>LED Controller</ion-title>
      </ion-toolbar>
    </ion-header>

    <IonContent>
      <IonCard class="ion-margin-top ion-text-center">
        <IonCardHeader>
          <IonCardTitle>No Controller Selected</IonCardTitle>
        </IonCardHeader>
        <IonCardContent>
          Please select a controller from the menu
        </IonCardContent>
      </IonCard>
      <ion-router-outlet></ion-router-outlet>
    </IonContent>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {
  IonContent,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonChip,
  IonButton,
  IonList,
  IonPage,
  IonButtons,
  IonMenuButton,
  IonMenuToggle,
  IonRouterOutlet,
  IonMenu,
  IonSpinner,
} from "@ionic/vue";

import { fetchJson } from "@/provider/Utils";

interface Controller {
  name: string;
  id: string;
}

export default defineComponent({
  components: {
    IonContent,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonChip,
    IonButton,
    IonList,
    IonPage,
    IonButtons,
    IonMenuButton,
    IonMenuToggle,
    IonRouterOutlet,
    IonMenu,
    IonSpinner,
  },
  data() {
    return {
      connectedControllers: [] as Controller[],
      isLoading: false,
    };
  },
  methods: {
    async clickController(controllerId: string) {
      this.$router.push({ name: "LedControlPanel", params: { controllerId } });
    },
    async getConnectedControllers() {
      this.isLoading = true;
      try {
        const response_data = await fetchJson(
          `/led/connected_controller`,
          undefined,
          false
        );
        const connectedControllersArray = Object.values(response_data.data);
        this.connectedControllers = connectedControllersArray.map(
          (item: any) => ({
            id: item.id,
            name: item.name,
          })
        );
      } catch (error) {
        console.error("Error getting connected controllers:", error);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
</script>

<style scoped>
.controllerChip {
  justify-content: center;
  width: 100%;
  margin-top: 8px;
  margin-bottom: 8px;
}

.no-controllers-text {
  color: var(--ion-color-medium);
  font-size: 0.9em;
  margin-top: 20px;
}

.ion-text-center {
  text-align: center;
}
</style>
