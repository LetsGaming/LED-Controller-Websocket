<template>
  <IonPage>
    <IonHeader>
      <IonToolbar>
        <IonSegment
          :scrollable="true"
          :value="selectedSegment"
          @ion-change="changeSelectedSegment"
        >
          <IonSegmentButton value="general"
            ><ion-icon :icon="settings"></ion-icon
          ></IonSegmentButton>
          <IonSegmentButton
            v-for="(animation, index) in Object.keys(animations)"
            :value="animation"
            :key="index"
            >{{ animation }}</IonSegmentButton
          >
        </IonSegment>
      </IonToolbar>
    </IonHeader>

    <IonContent>
      <template v-if="!selectedControllerId">
        <IonCard class="align-middle" style="margin-top: 20dvh">
          <IonCardHeader
            ><IonCardTitle>No Controller selected</IonCardTitle> </IonCardHeader
          ><IonCardContent
            >Please select a controller from the menu</IonCardContent
          >
        </IonCard>
      </template>
      <template v-else>
        <GeneralControls
          v-if="selectedSegment == 'general'"
          :selected-controller-id="selectedControllerId"
          @message_event="handleMessageEvent"
          style="margin-top: 20dvh"
        ></GeneralControls>
        <template
          v-for="(animation, index) in Object.keys(animations)"
          :key="index"
        >
          <AnimationControlPanel
            v-if="selectedSegment == animation"
            :panel-name="`${
              animation.charAt(0).toUpperCase() + animation.slice(1)
            } Animations`"
            :animations="animations[animation]"
            @animation_start="handleStartAnimation"
            style="margin-top: 20dvh"
          />
        </template>
      </template>
      <IonToast
        :isOpen="isToastVisible"
        :message="toastMessage"
        position="top"
        duration="5000"
        @onDidDismiss="clearToast"
        class="custom-toast"
      />
    </IonContent>
  </IonPage>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import {
  IonPage,
  IonContent,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonInput,
  IonSelect,
  IonItem,
  IonList,
  IonTitle,
  IonToolbar,
  IonHeader,
  IonButton,
  IonSelectOption,
  IonLabel,
  IonToast,
  IonSegment,
  IonSegmentButton,
  IonIcon,
} from "@ionic/vue";
import { settings } from "ionicons/icons";

import GeneralControls from "@/components/animation-components/segments/GeneralControls.vue";
import AnimationControlPanel from "@/components/animation-components/AnimationControlPanel.vue";

import { fetchJson } from "@/provider/Utils";

interface AnimationData {
  [key: string]: {};
}

export default defineComponent({
  components: {
    GeneralControls,
    AnimationControlPanel,
    IonPage,
    IonContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonInput,
    IonSelect,
    IonItem,
    IonList,
    IonTitle,
    IonToolbar,
    IonHeader,
    IonButton,
    IonSelectOption,
    IonLabel,
    IonToast,
    IonSegment,
    IonSegmentButton,
    IonIcon,
  },
  setup() {
    return { settings };
  },
  async mounted() {
    await this.initializeComponent();
  },
  data() {
    return {
      isToastVisible: false,
      toastMessage: "",
      selectedControllerId: "" as string | string[],
      brightness: 0,
      animations: {} as AnimationData,

      selectedSegment: "general",
    };
  },
  methods: {
    changeSelectedSegment(event: any) {
      this.selectedSegment = event.target.value;
    },
    async initializeComponent() {
      await this.getAnimations();
      const route = useRoute();
      const { controllerId } = route.params;
      this.selectedControllerId = controllerId;
    },
    clearToast() {
      this.isToastVisible = false;
      this.toastMessage = "";
    },
    handleMessageEvent(message: string) {
      this.toastMessage = message;
      this.isToastVisible = true;
    },
    async handleStartAnimation(data: StartAnimationEvent) {
      const animationCategory = data.name.split(" ")[0];
      switch (animationCategory) {
        case "Static":
          await this.startAnimation(
            animationCategory.toLowerCase(),
            data.animation,
            data.args
          );
          break;
        case "Standard":
          await this.startAnimation(
            animationCategory.toLowerCase(),
            data.animation,
            {}
          );
          break;
        case "Custom":
          await this.startAnimation(
            animationCategory.toLowerCase(),
            data.animation,
            data.args
          );
          break;
        case "Special":
          await this.startAnimation(
            animationCategory.toLowerCase(),
            data.animation,
            data.args
          );
          break;
        default:
          break;
      }
    },
    async startAnimation(category: string, animation: string, args = {}) {
      try {
        let endpoint = `/led/animations/${category}/${animation}/${this.selectedControllerId}`;
        if (this.selectedControllerId == "all") {
          endpoint = `/led/all/${animation}`;
        }

        const method = args ? "POST" : "GET";
        const options = args
          ? {
              method: method,
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(args),
            }
          : undefined;

        const data = await fetchJson(endpoint, options, false);
        this.handleMessageEvent(data.message.message || data.message);
      } catch (error) {
        console.error(`Error starting ${category} animation:`, error);
      }
    },
    async getAnimations() {
      try {
        const categories = ["static", "standard", "custom", "special"];
        await Promise.all(
          categories.map(async (category: string) => {
            const response = await fetchJson(
              `/led/animations/${category}`,
              undefined,
              false
            );
            this.animations[category] = response;
          })
        );
      } catch (error) {
        console.error("Error getting animations:", error);
      }
    },
  },
});
</script>
