<template>
  <IonPage>
    <!-- Header and Segment Navigation -->
    <IonHeader>
      <IonToolbar color="primary">
        <IonSegment
          :value="selectedSegment"
          scrollable
          @ionChange="changeSelectedSegment"
        >
          <IonSegmentButton value="general">
            <ion-icon :icon="settings" slot="start"></ion-icon>
            <IonLabel>General</IonLabel>
          </IonSegmentButton>

          <IonSegmentButton
            v-for="(animation, index) in animationCategories"
            :key="index"
            :value="animation"
          >
            <IonLabel>{{ capitalize(animation) }}</IonLabel>
          </IonSegmentButton>
        </IonSegment>
      </IonToolbar>
    </IonHeader>

    <!-- Content -->
    <IonContent class="ion-padding">
      <!-- Display message when no controller is selected -->
      <template v-if="!selectedControllerId">
        <IonCard class="ion-margin-top ion-text-center">
          <IonCardHeader>
            <IonCardTitle>No Controller Selected</IonCardTitle>
          </IonCardHeader>
          <IonCardContent>
            Please select a controller from the menu
          </IonCardContent>
        </IonCard>
      </template>

      <!-- General or Animation Panels based on selected segment -->
      <template v-else>
        <!-- General Controls -->
        <GeneralControls
          v-if="selectedSegment === 'general'"
          :selected-controller-id="selectedControllerId"
          @message_event="handleMessageEvent"
        />

        <!-- Animation Control Panels -->
        <template v-for="(animation, index) in Object.keys(animations)">
          <AnimationControlPanel
            v-if="selectedSegment === animation"
            :key="index"
            :panel-name="capitalize(animation) + ' Animations'"
            :animations="animations[animation]"
            @animation_start="handleStartAnimation"
          />
        </template>
      </template>

      <!-- Toast for feedback messages -->
      <IonToast
        :isOpen="isToastVisible"
        :message="toastMessage"
        position="bottom"
        duration="5000"
        @didDismiss="clearToast"
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
  IonHeader,
  IonToolbar,
  IonToast,
  IonSegment,
  IonSegmentButton,
  IonIcon,
  IonLabel,
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
    IonHeader,
    IonToolbar,
    IonToast,
    IonSegment,
    IonSegmentButton,
    IonIcon,
    IonLabel,
  },
  setup() {
    return { settings };
  },
  data() {
    return {
      isToastVisible: false,
      toastMessage: "",
      selectedControllerId: "" as string | string[],
      selectedSegment: "general",
      animations: {} as AnimationData,
      animationCategories: ["static", "standard", "custom", "special"], // Categories of animations
    };
  },
  async mounted() {
    await this.initializeComponent();
  },
  methods: {
    async initializeComponent() {
      const route = useRoute();
      this.selectedControllerId = route.params.controllerId || "";

      // Fetch all animations data at once
      await this.getAnimations();
    },
    async getAnimations() {
      try {
        // Fetch animation data for all categories in parallel
        const categories = this.animationCategories;
        const promises = categories.map((category) =>
          fetchJson(`/led/animations/${category}`, undefined, false)
        );

        const results = await Promise.all(promises);
        categories.forEach((category, index) => {
          this.animations[category] = results[index];
        });
      } catch (error) {
        console.error("Error getting animations:", error);
      }
    },
    changeSelectedSegment(event: any) {
      this.selectedSegment = event.target.value;
    },
    clearToast() {
      this.isToastVisible = false;
      this.toastMessage = "";
    },
    handleMessageEvent(message: string) {
      this.toastMessage = message;
      this.isToastVisible = true;
    },
    async handleStartAnimation(data: any) {
      try {
        const { name, animation, args } = data;
       
        const category = this.splitCategory(name)

        let endpoint = `/led/animations/${category}/${animation}/${this.selectedControllerId}`;
        if (this.selectedControllerId === "all") {
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

        const response = await fetchJson(endpoint, options, false);
        this.handleMessageEvent(response.message.message || response.message);
      } catch (error) {
        const category = this.splitCategory(data.name)
        console.error(`Error starting ${category} animation:`, error);
      }
    },
    splitCategory(name: string) {
      const category = name.split(" ")[0].toLowerCase();
      return category
    },
    capitalize(str: string) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
  },
});
</script>

<style scoped>
.ion-text-center {
  text-align: center;
}

.custom-toast {
  --background: var(--ion-color-primary);
}

.ion-margin-top {
  margin-top: 20vh;
}
</style>
