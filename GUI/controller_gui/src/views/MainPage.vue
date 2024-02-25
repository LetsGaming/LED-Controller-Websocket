<template>
  <ion-menu content-id="main-content">
    <ion-header>
      <ion-toolbar>
        <ion-title>Menu Content</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding"
      ><!-- Connected Controllers -->
      <IonCard class="align-middle">
        <IonCardHeader style="text-align: center">
          <IonCardTitle>Connected Controllers</IonCardTitle>
        </IonCardHeader>

        <IonCardContent>
          <IonButton @click="getConnectedControllers" style="display: flex">
            Get Controllers
          </IonButton>
        </IonCardContent>
      </IonCard>
      <IonList v-if="connectedControllers.length > 0" class="align-middle">
        <IonChip
          v-for="(controller, index) in connectedControllers"
          :key="index"
          @click="clickController(controller.id)"
          style="justify-content: center; width: 90%"
        >
          {{ controller.name }}
        </IonChip>
      </IonList>
      <p v-else>No connected controllers</p>
    </ion-content>
  </ion-menu>
  <ion-page id="main-content">
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>Menu</ion-title>
      </ion-toolbar>
    </ion-header>
    <IonContent
      ><IonCard class="align-middle" style="margin-top: 20dvh">
        <IonCardHeader
          ><IonCardTitle>No Controller selected</IonCardTitle> </IonCardHeader
        ><IonCardContent
          >Please select a controller from the menu</IonCardContent
        > </IonCard
      ><ion-router-outlet></ion-router-outlet
    ></IonContent>
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
  IonSelect,
  IonMenu,
  IonSelectOption,
  IonList,
  IonPage,
  IonButtons,
  IonMenuButton,
  IonRouterOutlet,
} from "@ionic/vue";

import { fetchJson } from "@/provider/Utills";

interface Controller {
  name: string;
  id: number;
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
    IonSelect,
    IonMenu,
    IonSelectOption,
    IonList,
    IonPage,
    IonButtons,
    IonMenuButton,
    IonRouterOutlet,
  },
  data() {
    return {
      connectedControllers: [] as Controller[],
      selectedControllerId: null,
    };
  },
  methods: {
    clickController(controllerId: number) {
      // Open LedControlPanel with the selected controller's ID
      this.$router.push({ name: "LedControlPanel", params: { controllerId } });
    },
    async getConnectedControllers() {
      try {
        const response_data = await fetchJson(
          `/led/connected_controller`,
          undefined,
          true
        );

        const connectedControllersArray = Object.values(response_data.data);

        this.connectedControllers = connectedControllersArray.map((item: any) => ({
          id: item.id,
          name: item.name,
        }));
      } catch (error) {
        console.error("Error getting connected controllers:", error);
      }
    },
  },
});
</script>
