<template>
  <div class="animation-control-panel">
    <ion-header class="align-middle">
      <ion-toolbar style="text-align: center;">
        <ion-title>{{ panelName }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <!-- Animation Selection -->
    <ion-item class="align-middle">
      <ion-select v-model="selectedAnimation" label="Choose Animation">
        <ion-select-option
          v-for="(animation, name) in animations"
          :key="name"
          :value="name"
        >
          {{ animation.name }}
        </ion-select-option>
      </ion-select>
    </ion-item>

    <!-- Animation Input Panel -->
    <AnimationInput
      v-if="selectedAnimationData"
      @animationStart="handleAnimationInput"
      :animationData="selectedAnimationData"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonItem,
  IonSelect,
  IonSelectOption,
} from "@ionic/vue";

import AnimationInput from "./AnimationInput.vue";

export default defineComponent({
  emits: ["animation_start"],
  components: {
    AnimationInput,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonItem,
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
  setup(props, { emit }) {
    const selectedAnimation = ref<string | null>(null);

    const selectedAnimationData = computed(() => {
      return selectedAnimation.value ? props.animations[selectedAnimation.value] : {};
    });

    const handleAnimationInput = (data: any) => {
      emit("animation_start", { name: props.panelName, ...data });
    };

    return {
      selectedAnimation,
      selectedAnimationData,
      handleAnimationInput,
    };
  },
});
</script>

<style scoped>
.animation-control-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 15px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .animation-control-panel {
    gap: 15px;
    padding: 10px;
  }
}
</style>
