<template>
  <IonCard class="align-middle">
    <IonCardHeader>
      <IonCardTitle>Online State</IonCardTitle>
    </IonCardHeader>

    <IonCardContent>
      <IonButton @click="getOnlineState">Get Online State</IonButton>
      <IonButton @click="setOnlineState(true)">Set Online</IonButton>
      <IonButton @click="setOnlineState(false)">Set Offline</IonButton>
    </IonCardContent>
  </IonCard>
</template>

<script lang="ts">
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonInput,
  IonButton,
  IonToast,
} from "@ionic/vue";

import { defineComponent } from "vue";

import { fetchJson } from "@/provider/Utils";

export default defineComponent({
  emits: ["messageEvent"],
  components: {
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonInput,
    IonButton,
    IonToast,
  },
  props: {
    selectedControllerId: {
      type: [String, Array],
      required: true,
    },
  },
  methods: {
    async getOnlineState() {
      try {
        const response = await fetchJson(
          `/led/get_online_state/${this.selectedControllerId}`,
          undefined,
          false
        );
        this.emitMessageEvent(`Online state: ${response.message.data}`);
      } catch (error) {
        console.error("Error getting online state:", error);
      }
    },
    async setOnlineState(online: boolean) {
      try {
        const data = await fetchJson(
          `/led/set_online_state/${this.selectedControllerId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ online }),
          },
          false
        );
        this.emitMessageEvent(data.message.message);
      } catch (error) {
        console.error("Error setting online state:", error);
      }
    },
    emitMessageEvent(message: string) {
      this.$emit("messageEvent", message);
    },
  },
});
</script>
