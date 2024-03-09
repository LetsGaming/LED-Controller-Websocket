<template>
  <IonCard class="align-middle" style="display: grid">
    <IonCardHeader>
      <IonCardTitle style="align-self: center">Brightness</IonCardTitle>
    </IonCardHeader>

    <IonCardContent>
      <IonButton @click="getBrightness" style="display: flex"
        >Get Brightness</IonButton
      >
      <div class="brightness-control">
        <IonRange
          @ion-change="calcBrightness"
          placeholder="Enter brightness"
          :pin="true"
          :pin-formatter="pinFormatter"
        ></IonRange>
        <IonButton @click="setBrightness">Set Brightness</IonButton>
      </div>
    </IonCardContent>
  </IonCard>
</template>

<script lang="ts">
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonRange,
  IonButton,
  IonToast,
  IonRow,
  IonCol,
} from "@ionic/vue";

import { defineComponent } from "vue";

import { fetchJson } from "@/provider/Utills";

export default defineComponent({
  emits: ["messageEvent"],
  components: {
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonRange,
    IonButton,
    IonToast,
    IonRow,
    IonCol,
  },
  props: {
    selectedControllerId: {
      type: [String, Array],
      required: true,
    },
  },
  setup() {
    return {
      pinFormatter: (value: number) => `${value}%`,
    };
  },
  data() {
    return {
      brightness: 0,
    };
  },
  methods: {
    calcBrightness(ev: any) {
      const brightnessPercentage = ev.detail.value;
      this.brightness = Math.round((brightnessPercentage / 100) * 255);
    },
    async getBrightness() {
      try {
        const data = await fetchJson(
          `/led/get_brightness/${this.selectedControllerId}`,
          undefined,
          false
        );
        this.emitMessageEvent(`Controller brightness: ${data.message.data}`);
      } catch (error) {
        console.error("Error getting brightness:", error);
      }
    },
    async setBrightness() {
      try {
        const data = await fetchJson(
          `/led/set_brightness/${this.selectedControllerId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ brightness: this.brightness }),
          },
          false
        );
        this.emitMessageEvent(data.message.message);
      } catch (error) {
        console.error("Error setting brightness:", error);
      }
    },
    emitMessageEvent(message: string) {
      this.$emit("messageEvent", message);
    },
  },
});
</script>

<style scoped>
.brightness-control {
  display: flex;
  justify-content: space-between; /* Adjust as needed */
  align-items: center; /* Adjust as needed */
}

.brightness-control ion-range {
  min-width: 150px;
  margin: 5px;
}
</style>