<template>
  <div class="align-middle">
    <ion-card
      v-if="!isObjectEmpty(animationData)"
      class="align-middle"
      style="display: block"
    >
      <IonCardHeader>
        <ion-card-title>{{ animationData?.name }}</ion-card-title>
      </IonCardHeader>
      <ion-card-content>
        <ion-text>{{ animationData?.description }}</ion-text>

        <!-- Single Color Input -->
        <ion-item
          v-if="hasColorArguments && !hasFadingArguments && !hasMultipleColors"
        >
          <ion-label>Color:</ion-label>
          <input v-model="inputArgsColors.color" type="color" />
        </ion-item>

        <!-- Fading Color Inputs -->
        <ion-item
          v-if="hasFadingArguments && !hasColorArguments && !hasMultipleColors"
        >
          <ion-label>From Color:</ion-label>
          <input v-model="inputArgsColors.from_color" type="color" />

          <ion-label>To Color:</ion-label>
          <input v-model="inputArgsColors.to_color" type="color" />
        </ion-item>

        <!-- Multiple Colors Input -->
        <ion-item
          v-if="hasMultipleColors && !hasColorArguments && !hasFadingArguments"
        >
          <ion-label>Colors:</ion-label>
          <div style="display: flex; flex-wrap: wrap; justify-content: center; width: 100%;">
            <div
              v-for="(color, index) in inputArgsColors?.colors"
              :key="index"
              style="margin-right: 10px; margin-bottom: 10px; display: flex;"
            >
              <input v-model="inputArgsColors.colors[index]" type="color" style="align-self: center;"/>
              <ion-button @click="removeColor(index)">Remove</ion-button>
            </div>
          </div>
          <ion-button @click="addColor">Add Color</ion-button>
        </ion-item>

        <!-- Other Arguments -->
        <template
          v-for="(arg, index) in animationData?.args"
          v-if="!hasMultipleColors"
          :key="index"
        >
          <template v-if="!isColorArgument(arg)">
            <ion-item>
              <ion-input
                v-model="(inputArgs[arg] as number)"
                type="number"
                :label="arg"
                label-placement="start"
              ></ion-input>
            </ion-item>
          </template>
        </template>

        <ion-button expand="full" @click="startAnimation"
          >Start Animation</ion-button
        >
      </ion-card-content>
    </ion-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
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

interface InputArgsColors {
  color: string;
  from_color: string;
  to_color: string;
  colors: string[];
}

interface AnimationData {
  name: string;
  animation_name: string;
  description: string;
  args: string[];
}

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
      type: Object as () => AnimationData,
      default: () => ({}),
    },
  },
  data() {
    return {
      inputArgsColors: {
        color: "#000000",
        from_color: "#000000",
        to_color: "#ffffff",
        colors: ["#000000"],
      } as InputArgsColors,
      inputArgs: {} as { [key: string]: number },
    };
  },
  computed: {
    hasColorArguments(): boolean {
      return (
        Array.isArray(this.animationData?.args) &&
        this.animationData?.args.includes("red") &&
        this.animationData?.args.includes("green") &&
        this.animationData?.args.includes("blue")
      );
    },
    hasFadingArguments(): boolean {
      return (
        Array.isArray(this.animationData?.args) &&
        this.animationData?.args.includes("from_red") &&
        this.animationData?.args.includes("from_green") &&
        this.animationData?.args.includes("from_blue") &&
        this.animationData?.args.includes("to_red") &&
        this.animationData?.args.includes("to_green") &&
        this.animationData?.args.includes("to_blue")
      );
    },
    hasMultipleColors(): boolean {
      return (
        Array.isArray(this.animationData?.args) &&
        this.animationData?.args.includes("colors")
      );
    },
  },
  methods: {
    resetInputArgs() {
      this.inputArgs = {} as { [key: string]: number };
    },
    isObjectEmpty(obj: Object) {
      for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
          return false;
        }
      }
      return true;
    },
    isColorArgument(arg: string) {
      return [
        "red",
        "green",
        "blue",
        "from_red",
        "from_green",
        "from_blue",
        "to_red",
        "to_green",
        "to_blue",
      ].includes(arg);
    },
    startAnimation() {
      const inputColors = this.hasMultipleColors
        ? this.inputArgsColors?.colors
        : null;

      const colorArgs = this.hasColorArguments
        ? this.inputArgsColors?.color
        : null;
      const fadingArgs = this.hasFadingArguments ? this.inputArgsColors : null;

      const getColorValues = (color: string | undefined) =>
        color?.match(/\w\w/g)?.map((hex: string) => parseInt(hex, 16)) || [
          0, 0, 0,
        ];

      const getColorData = (args: string | undefined, asArray: boolean) => {
        const [red, green, blue] = getColorValues(args || "#000000");
        if (asArray) return [red, green, blue];
        return { red, green, blue };
      };

      const getFadingArgsData = (fromToColor: string | undefined) => {
        const [red, green, blue] = getColorValues(fromToColor || "#000000");
        return { red, green, blue };
      };

      const colorsArgs: { colors: any[] } = { colors: [] };

      if (inputColors) {
        for (const color of inputColors) {
          const colorData = getColorData(color, true);
          colorsArgs.colors.push(colorData);
        }
      }

      const data = {
        animation: this.animationData?.animation_name,
        args: {
          ...(this.hasMultipleColors ? colorsArgs : {}),
          ...(colorArgs ? getColorData(colorArgs, false) : {}),
          ...(fadingArgs
            ? {
                from_red: getFadingArgsData(fadingArgs.from_color).red,
                from_green: getFadingArgsData(fadingArgs.from_color).green,
                from_blue: getFadingArgsData(fadingArgs.from_color).blue,
                to_red: getFadingArgsData(fadingArgs.to_color).red,
                to_green: getFadingArgsData(fadingArgs.to_color).green,
                to_blue: getFadingArgsData(fadingArgs.to_color).blue,
              }
            : {}),
          ...this.inputArgs,
        },
      };
      this.$emit("animationStart", data);
      this.resetInputArgs();
    },
    // Method to add a new color input
    addColor() {
      this.inputArgsColors?.colors.push("#000000");
    },

    // Method to remove a color input
    removeColor(index: number) {
      this.inputArgsColors?.colors.splice(index, 1);
    },
  },
});
</script>
