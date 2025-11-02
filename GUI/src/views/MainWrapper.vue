<template>
  <IonPage>
    <IonContent>
      <MainPage></MainPage>
    </IonContent>
  </IonPage>
</template>

<script setup lang="ts">
import MainPage from "./MainPage.vue";

import { IonPage, IonContent } from "@ionic/vue";
</script>

<style>
ion-content::part(scroll)::-webkit-scrollbar {
  display: none;
}
ion-content::part(scroll) {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>