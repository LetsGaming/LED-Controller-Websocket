<template>
  <div class="general-controls">
    <!-- Online State -->
    <OnlineStatePanel
      :fetch-online-state="fetchOnline"
      :selected-controller-id="selectedControllerId"
      @message-event="handleMessageEvent"
    />

    <!-- Brightness Panel -->
    <BrightnessPanel
      :fetch-brightness="fetchBrightness"
      :selected-controller-id="selectedControllerId"
      @message-event="handleMessageEvent"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

// Import components
import OnlineStatePanel from "@/components/animation-components/OnlineStatePanel.vue";
import BrightnessPanel from "@/components/animation-components/BrightnessPanel.vue";

export default defineComponent({
  // Declare emits
  emits: ["message_event"],

  // Component registration
  components: {
    OnlineStatePanel,
    BrightnessPanel,
  },

  // Props validation
  props: {
    selectedControllerId: {
      type: [String, Array],
      required: true,
    },
  },
  data() {
    return {
      fetchOnline: false,
      fetchBrightness: false,
    };
  },
  mounted() {
    this.fetchOnline = true;
    setTimeout(() => {
      this.fetchBrightness = true;
    }, 15 * 1000);
    setTimeout(() => {
      this.fetchOnline = false;
      this.fetchBrightness = false;
    }, 30 * 1000);
  },
  // Methods
  methods: {
    handleMessageEvent(message: string) {
      this.$emit("message_event", message);
    },
  },
});
</script>

<style scoped>
/* Add some responsive and spacing adjustments */
.general-controls {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 10px;
}

/* Adjust for mobile view */
@media (max-width: 768px) {
  .general-controls {
    gap: 15px;
  }
}
</style>
