<template>
  <IonCard class="align-middle" style="display: grid">
    <IonCardHeader>
      <IonCardTitle>Online State</IonCardTitle>
    </IonCardHeader>

    <IonCardContent class="center-content">
      <IonToggle v-model="online" @ion-change="toggleOnlineState"></IonToggle>
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
import { fetchJson } from "@/provider/Utils";

export default {
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
    fetchOnlineState: {
      type: Boolean,
      default: false,
    },
    selectedControllerId: {
      type: [String, Array],
      required: true,
    },
  },
  watch: {
    async fetchOnlineState(newVal: boolean) {
      if (newVal) {
        await this.getOnlineState();
      }
    },
  },
  data() {
    return {
      online: false,
    };
  },
  computed: {
    isAllController() {
      return this.selectedControllerId === "all";
    },
  },
  methods: {
    emitMessageEvent(message: string) {
      this.$emit("messageEvent", message);
    },

    async fetchOnlineStateData(endpoint: string) {
      try {
        const response = await fetchJson(endpoint);
        return response.message?.data || false;
      } catch (error) {
        console.error("Error fetching online state:", error);
        return false;
      }
    },

    async getOnlineState(suppressMessage?: boolean) {
      const endpoint = this.isAllController
        ? "/led/all/get_online_state"
        : `/led/get_online_state/${this.selectedControllerId}`;

      this.online = await this.fetchOnlineStateData(endpoint);

      if (suppressMessage) return;
      this.emitMessageEvent(`Online state: ${this.online}`);
    },

    async toggleOnlineState(ev: any) {
      await this.setOnlineState(ev.detail.checked);
    },

    async setOnlineState(newOnlineState: boolean) {
      try {
        const endpoint = this.isAllController
          ? "/led/all/set_online_state"
          : `/led/set_online_state/${this.selectedControllerId}`;

        const response = await fetchJson(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ online: newOnlineState }),
        });

        this.online = newOnlineState;
        this.emitMessageEvent(
          response.message?.message || "State updated successfully"
        );
      } catch (error) {
        console.error("Error setting online state:", error);
      }
    },
  },
};
</script>

<style scoped>
.center-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
