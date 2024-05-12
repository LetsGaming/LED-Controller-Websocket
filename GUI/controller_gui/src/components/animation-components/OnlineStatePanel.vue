<template>
  <IonCard class="align-middle">
    <IonCardHeader>
      <IonCardTitle>Online State</IonCardTitle><br>
      <IonButton @click="getOnlineState">Get</IonButton>
    </IonCardHeader>
    
    <IonCardContent style="display: flex; justify-content: center; align-items: center;">
      <IonToggle v-model="online" @ion-change="toggleOnlineState" style="padding: auto;"></IonToggle>
    </IonCardContent>
  </IonCard>
</template>

<script lang="ts">
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonButton,
  IonToggle,
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
    IonButton,
    IonToggle,
  },
  props: {
    selectedControllerId: {
      type: [String, Array],
      required: true,
    },
  },
  data() {
    return {
      online: false,
    };
  },
  methods: {
    async getOnlineState() {
      try {
        const endpoint = this.selectedControllerId == 'all' ? '/led/all/get_online_state' :  `/led/get_online_state/${this.selectedControllerId}`;
        const response = await fetchJson(endpoint, undefined, false);
        this.online = response.message.data; // Update online state
        this.emitMessageEvent(`Online state: ${this.online}`);
      } catch (error) {
        console.error("Error getting online state:", error);
      }
    },
    async toggleOnlineState() {
      const newOnlineState = !this.online; // Toggle online state
      await this.setOnlineState(newOnlineState);
    },
    async setOnlineState(online: boolean) {
      try {
        const endpoint = this.selectedControllerId == 'all' ? `/led/all/set_online_state` : `/led/set_online_state/${this.selectedControllerId}`;
        const data = await fetchJson(
          endpoint,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ online }),
          },
          false
        );
        this.online = online; // Update online state
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
