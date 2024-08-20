<template>
  <IonCard class="align-middle">
    <IonCardHeader>
      <IonCardTitle>Online State</IonCardTitle>
      <IonButton @click="getOnlineState">Get</IonButton>
    </IonCardHeader>

    <IonCardContent class="center-content">
      <IonToggle v-model="online" @ion-change="toggleOnlineState"></IonToggle>
    </IonCardContent>
  </IonCard>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonButton,
  IonToggle,
} from "@ionic/vue";
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
  mounted() {
    this.getOnlineState();
  },
  setup(props, { emit }) {
    const online = ref(false);

    const emitMessageEvent = (message: string) => {
      emit("messageEvent", message);
    };

    const isAllController = () => {
      return Array.isArray(props.selectedControllerId) && props.selectedControllerId.includes('all')
    }

    const fetchOnlineState = async (endpoint: string) => {
      try {
        const response = await fetchJson(endpoint);
        return response.message?.data || false;
      } catch (error) {
        console.error("Error fetching online state:", error);
        return false;
      }
    };

    const getOnlineState = async () => {
      const endpoint = isAllController()
        ? '/led/all/get_online_state'
        : `/led/get_online_state/${props.selectedControllerId}`;
      
      online.value = await fetchOnlineState(endpoint);
      emitMessageEvent(`Online state: ${online.value}`);
    };

    const toggleOnlineState = async (ev: any) => {
      await setOnlineState(ev.detail.checked);
    };

    const setOnlineState = async (newOnlineState: boolean) => {
      try {
        const endpoint = isAllController()
          ? `/led/all/set_online_state`
          : `/led/set_online_state/${props.selectedControllerId}`;
        
        const response = await fetchJson(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ online: newOnlineState }),
        });

        online.value = newOnlineState;
        emitMessageEvent(response.message?.message || "State updated successfully");
      } catch (error) {
        console.error("Error setting online state:", error);
      }
    };

    return {
      online,
      getOnlineState,
      toggleOnlineState,
    };
  },
});
</script>

<style scoped>
.center-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
