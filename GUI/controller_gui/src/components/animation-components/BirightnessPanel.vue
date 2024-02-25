<template>
  <IonCard class="align-middle" style="display: grid">
    <IonCardHeader>
      <IonCardTitle style="align-self: center">Brightness</IonCardTitle>
    </IonCardHeader>

    <IonCardContent>
      <IonButton @click="getBrightness" style="display: flex"
        >Get Brightness</IonButton
      >
      <div style="display: flex">
        <IonInput
          v-model="brightness"
          type="number"
          placeholder="Enter brightness"
          lab
        ></IonInput>
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
  IonInput,
  IonButton,
  IonToast,
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
  data() {
    return {
      brightness: 0,
    };
  },
  methods: {
    async getBrightness() {
      try {
        const data = await fetchJson(
          `/led/get_brightness/${this.selectedControllerId}`,
          undefined,
          true
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
          true
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
