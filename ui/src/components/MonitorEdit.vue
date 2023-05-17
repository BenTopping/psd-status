<script setup>
import { ref, watchEffect } from "vue";
import { useAuthenticationStore } from "../stores/authStore.js";
import { useAlertStore } from "../stores/alertStore.js"
import { createMonitor } from "../api";

const authStore = useAuthenticationStore();
const alertStore = useAlertStore();
const props = defineProps({
  monitor: Object,
  protocols: Array,
});

const emit = defineEmits(["fetchMonitors"]);

// This clones the monitor prop whilst also updating if the prop changes
const currentMonitor = ref();
watchEffect(() => (currentMonitor.value = { ...props.monitor }));

async function createOrUpdateMonitor() {
  await createMonitor(currentMonitor.value, authStore.jwt)
    .then((response) => {
      alertStore.addAlert('Successfully updated monitor', 'success')
      emit("fetchMonitors");
      return response;
    })
    .catch((error) => {
      alertStore.addAlert(`Error updating monitor: ${error.response.data.message}`, 'danger')
    });
}
</script>

<template>
  <div
    class="flex flex-col w-full max-w-[800px] mt-2 rounded-lg drop-shadow-md bg-white"
    data-attribute="monitor-edit"
  >
    <div class="flex bg-sdb-400 font-bold text-white rounded-t-lg py-5 w-full">
      <h1 class="mx-auto text-2xl">{{ monitor.name || "New" }}</h1>
    </div>
    <form
      class="flex flex-col p-5 w-full gap-y-3"
      @submit.prevent="createOrUpdateMonitor()"
    >
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold"
          >Name</label
        >
        <input
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          placeholder="Name"
          v-model="currentMonitor.name"
          data-attribute="name-input"
          required
        />
      </div>
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold"
          >Protocol</label
        >
        <select
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          v-model="currentMonitor.protocol_id"
          data-attribute="protocol-select"
          required
        >
          <option
            v-for="protocol in protocols"
            :key="protocol.id"
            :value="protocol.id"
          >
            {{ protocol.name }}
          </option>
        </select>
      </div>
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold"
          >Target</label
        >
        <input
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          placeholder="www.test.com"
          v-model="currentMonitor.target"
          data-attribute="target-input"
          required
        />
      </div>
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold"
          >Poll delay</label
        >
        <select
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          v-model="currentMonitor.delay"
          data-attribute="delay-select"
          required
        >
          <option value="60">1m</option>
          <option value="120">2m</option>
          <option value="300">5m</option>
          <option value="600">10m</option>
          <option value="1800">30m</option>
          <option value="3600">1h</option>
          <option value="86400">24h</option>
        </select>
      </div>
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold"
          >Active?</label
        >
        <select
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          v-model="currentMonitor.active"
          data-attribute="active-select"
          required
        >
          <option :value="true">True</option>
          <option :value="false">False</option>
        </select>
      </div>
      <button
        class="mx-auto w-32 bg-sdb-400 p-2 my-2 text-white rounded-lg text-base"
        type="submit"
        data-action="submit-monitor"
      >
        {{ currentMonitor.id ? "Update" : "Create" }}
      </button>
    </form>
  </div>
</template>
