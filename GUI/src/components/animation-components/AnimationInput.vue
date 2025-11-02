<template>
  <div class="animation-input-panel" v-if="!isObjectEmpty(animationData)">
    <ion-card class="align-middle">
      <IonCardHeader style="width: 100%;">
        <ion-card-title style="text-align: center;">{{ animationData.name }}</ion-card-title>
      </IonCardHeader>

      <ion-card-content>
        <ion-text>{{ animationData.description }}</ion-text>

        <!-- Single Color Input -->
        <ion-item v-if="hasColorArguments && !hasFadingArguments && !hasMultipleColors">
          <ion-label>Color:</ion-label>
          <input v-model="inputArgsColors.color" type="color" />
        </ion-item>

        <!-- Fading Color Inputs -->
        <ion-item v-if="hasFadingArguments && !hasColorArguments && !hasMultipleColors">
          <ion-label>From Color:</ion-label>
          <input v-model="inputArgsColors.from_color" type="color" />
          <ion-label>To Color:</ion-label>
          <input v-model="inputArgsColors.to_color" type="color" />
        </ion-item>

        <!-- Multiple Colors Input -->
        <ion-item v-if="hasMultipleColors && !hasColorArguments && !hasFadingArguments">
          <ion-label>Colors:</ion-label>
          <div class="color-inputs">
            <div v-for="(color, index) in inputArgsColors.colors" :key="index" class="color-input">
              <input v-model="inputArgsColors.colors[index]" type="color" />
              <ion-button @click="removeColor(index)">Remove</ion-button>
            </div>
          </div>
          <ion-button @click="addColor">Add Color</ion-button>
        </ion-item>

        <!-- Other Arguments -->
        <template v-for="(arg, index) in animationData.args" v-if="!hasMultipleColors" :key="index">
          <template v-if="!isColorArgument(arg)">
            <ion-item>
              <ion-input v-model.number="inputArgs[arg]" type="number" :label="arg" label-placement="start" min="1"></ion-input>
            </ion-item>
          </template>
        </template>

        <ion-button expand="full" @click="startAnimation">Start Animation</ion-button>
      </ion-card-content>
    </ion-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import {
  IonCardHeader,
  IonCardTitle,
  IonItem,
  IonInput,
  IonButton,
  IonText,
  IonLabel,
  IonCard,
  IonCardContent,
} from "@ionic/vue";

export default defineComponent({
  emits: ["animationStart"],
  components: {
    IonCardHeader,
    IonCardTitle,
    IonItem,
    IonInput,
    IonButton,
    IonText,
    IonLabel,
    IonCard,
    IonCardContent,
  },
  props: {
    animationData: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, { emit }) {
    const inputArgsColors = ref({
      color: "#000000",
      from_color: "#000000",
      to_color: "#ffffff",
      colors: ["#000000"],
    });

    const inputArgs = ref<{ [key: string]: number }>({});

    const hasColorArguments = computed(() =>
      ["red", "green", "blue"].every((color) => props.animationData?.args?.includes(color))
    );
    const hasFadingArguments = computed(() =>
      ["from_red", "from_green", "from_blue", "to_red", "to_green", "to_blue"].every((arg) =>
        props.animationData?.args?.includes(arg)
      )
    );
    const hasMultipleColors = computed(() => props.animationData?.args?.includes("colors"));

    const isObjectEmpty = (obj: Object) => !Object.keys(obj).length;

    const isColorArgument = (arg: string) =>
      ["red", "green", "blue", "from_red", "from_green", "from_blue", "to_red", "to_green", "to_blue"].includes(arg);

    const getColorValues = (color: string | undefined) =>
      color?.match(/\w\w/g)?.map((hex) => parseInt(hex, 16)) || [0, 0, 0];

    const getColorData = (color: string | undefined) => {
      const [red, green, blue] = getColorValues(color);
      return { red, green, blue };
    };

    const startAnimation = () => {
      const colorArgs = hasColorArguments.value ? inputArgsColors.value.color : null;
      const fadingArgs = hasFadingArguments.value ? inputArgsColors.value : null;
      const multipleColors = hasMultipleColors.value ? inputArgsColors.value.colors : null;

      const colorsArgs = multipleColors
        ? { colors: multipleColors.map((color) => getColorValues(color)) }
        : {};

      const argsData = {
        ...(colorArgs ? getColorData(colorArgs) : {}),
        ...(fadingArgs ? getColorData(fadingArgs.from_color) : {}),
        ...(multipleColors ? colorsArgs : {}),
        ...inputArgs.value,
      };

      emit("animationStart", {
        animation: props.animationData?.animation_name,
        args: argsData,
      });

      resetInputArgs();
    };

    const resetInputArgs = () => {
      inputArgs.value = {};
    };

    const addColor = () => {
      inputArgsColors.value.colors.push("#000000");
    };

    const removeColor = (index: number) => {
      inputArgsColors.value.colors.splice(index, 1);
    };

    return {
      inputArgsColors,
      inputArgs,
      hasColorArguments,
      hasFadingArguments,
      hasMultipleColors,
      isObjectEmpty,
      isColorArgument,
      startAnimation,
      addColor,
      removeColor,
    };
  },
});
</script>

<style scoped>
.animation-input-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 15px;
}

.color-inputs {
  display: flex;
  flex-wrap: wrap;
}

.color-input {
  display: flex;
  align-items: center;
  margin-right: 10px;
  margin-bottom: 10px;
}

/* Responsive styling */
@media (max-width: 768px) {
  .animation-input-panel {
    gap: 15px;
    padding: 10px;
  }
}
</style>
