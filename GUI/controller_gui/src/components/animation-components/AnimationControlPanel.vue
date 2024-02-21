<template>
  <div class="align-middle">
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ panelName }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-item style="width: 100%">
      <ion-select v-model="selectedAnimation" label="Choose Animation:">
        <ion-select-option
          v-for="(animation, name) in animations"
          :key="name"
          :value="name"
          :label="animation.name"
        >
          {{ animation.name }}
        </ion-select-option>
      </ion-select>
    </ion-item>

    <AnimationInput
      @animationStart="handleAnimationInput"
      :animationData="selectedAnimationData"
    ></AnimationInput>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonSelect,
  IonSelectOption,
} from "@ionic/vue";

import AnimationInput from "./AnimationInput.vue";

export default defineComponent({
  emits: ["animation_start"],
  components: {
    AnimationInput,
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonSelect,
    IonSelectOption,
  },
  props: {
    panelName: {
      type: String,
      required: true,
    },
    animations: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      selectedAnimation: null,
    };
  },
  computed: {
    selectedAnimationData() {
      if (
        this.animations &&
        typeof this.animations === "object" &&
        this.selectedAnimation
      ) {
        return this.animations[this.selectedAnimation] || {};
      }
      return {};
    },
  },
  methods: {
    handleAnimationInput(data: any) {
      const new_data = { name: this.panelName, ...data } as StartAnimationEvent;
      this.$emit("animation_start", new_data);
    },
  },
});
</script>
