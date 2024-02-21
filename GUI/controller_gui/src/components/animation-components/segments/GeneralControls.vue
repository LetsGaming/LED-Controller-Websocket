<template>
  <div>
    <!-- Online State -->
    <OnlineStatePanel
      :selected-controller-id="selectedControllerId"
      @message-event="handleMessageEvent"
    ></OnlineStatePanel>

    <!-- Brightness -->
    <BirightnessPanel
      :selected-controller-id="selectedControllerId"
      @message-event="handleMessageEvent"
    ></BirightnessPanel>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import OnlineStatePanel from "../OnlineStatePanel.vue";
import BirightnessPanel from "../BirightnessPanel.vue";

export default defineComponent({
  emits: ["message_event"],
  components: {
    OnlineStatePanel,
    BirightnessPanel,
  },
  props: {
    selectedControllerId: {
      type: [String, Array],
      required: true,
    },
  },
  methods: {
    handleMessageEvent(message: string) {
      this.$emit("message_event", message);
    },
  },
});
</script>
