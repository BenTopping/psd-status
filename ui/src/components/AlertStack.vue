<script setup>
import { useAlertStore } from "../stores/alertStore.js";
const store = useAlertStore();

function calculateVariant(message) {
  switch (message.variant) {
    case "primary":
      return "bg-blue-200";
    case "success":
      return "bg-green-200";
    case "warning":
      return "bg-yellow-200";
    case "danger":
      return "bg-red-300";
    default:
      return "bg-blue-200";
  }
}
</script>

<template>
  <div
    v-if="store.hasAlerts"
    class="bottom-0 fixed right-0 -top-2 z-[1051] mb-2 max-w-[500px] w-full"
  >
    <div
      class="flex justify-end mb-2 border-sp border-b-2 tracking-tight leading-relaxed"
    >
      <button
        class="mt-5 mb-2 w-32 bg-sdb-400 p-2 text-white rounded-lg text-base"
        @click="store.clearAlerts()"
      >
        Clear
      </button>
    </div>
    <div class="overflow-y-scroll w-full break-words max-h-[500px]">
      <div
        v-for="(alert, index) in store.alerts"
        ref="alert"
        :key="index"
        v-bind="alert"
        :class="`rounded-lg flex flex-row items-center space-between px-6 py-2 my-2 text-black ${calculateVariant(
          alert
        )}`"
        role="alert"
      >
        <p class="flex w-full">{{ alert.message }}</p>
        <button
          @click="store.removeAlert(index)"
          class="mx-2 p-2 rounded-lg w-10 h-10"
        >
          X
        </button>
      </div>
    </div>
  </div>
</template>
