<template>
  <IonCard class="align-middle" style="display: grid">
    <IonCardHeader>
      <IonCardTitle style="align-self: center">Brightness</IonCardTitle>
    </IonCardHeader>

    <IonCardContent>
      <IonButton @click="getBrightness" style="display: flex"
        >Get</IonButton
      >
      <div class="brightness-control">
        <IonRange
          @ion-change="calcBrightness"
          placeholder="Enter brightness"
          :pin="true"
          :pin-formatter="pinFormatter"
          v-model="brightnessPercentage"
        ></IonRange>
        <IonButton @click="setBrightness">Set</IonButton>
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
    IonRange,
    IonButton,
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
      brightnessPercentage: 0
    };
  },
  methods: {
    calcBrightness(ev: any) {
      this.brightnessPercentage = ev.detail.value;
      this.brightness = Math.round((this.brightnessPercentage / 100) * 255);
    },
    async getBrightness() {
      try {
        const endpoint = this.selectedControllerId == 'all' ?  '/led/all/get_brightness' : `/led/get_brightness/${this.selectedControllerId}`;

        const data = await fetchJson(
          endpoint,
          undefined,
          false
        );
        this.brightness = data.message.data; // Update brightness from server
        this.brightnessPercentage = (this.brightness * 100) / 255;
        this.emitMessageEvent(`Controller brightness: ${this.brightness}`);
      } catch (error) {
        console.error("Error getting brightness:", error);
      }
    },
    async setBrightness() {
      try {
        const endpoint = this.selectedControllerId == 'all' ? '/led/all/set_brightness' : `/led/set_brightness/${this.selectedControllerId}`;

        const data = await fetchJson(
          endpoint,
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
