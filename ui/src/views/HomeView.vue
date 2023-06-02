<script setup>
import { getMonitors, getHttpRecords } from "../api/index.js";
import { ref, onMounted, onUnmounted, computed } from "vue";
import MonitorCard from "../components/MonitorCard.vue";
import { useAlertStore } from "../stores/alertStore";
import { formatMonitors } from "../utils/monitors";
import DataFetcher from "../components/DataFetcher.vue";

const alertStore = useAlertStore();
const monitors = ref([]);
const lastUpdated = ref(new Date().toLocaleString());
let pollInterval = null;

const numOfRedSystems = computed(() => {
  return monitors.value?.filter((monitor) => monitor.current_state == "red")
    .length;
});
const numOfGreenSystems = computed(() => {
  return monitors.value?.filter((monitor) => monitor.current_state == "green")
    .length;
});
const numOfYellowSystems = computed(() => {
  return monitors.value?.filter((monitor) => monitor.current_state == "yellow")
    .length;
});

async function fetchData() {
  const { success, data: monitor_data } = await getMonitors();
  if (success) {
    const monitor_ids = monitor_data.map((monitor) => monitor.id);
    const { success, data: http_records_data } = await getHttpRecords(
      monitor_ids,
      10
    );
    if (success) {
      monitors.value = formatMonitors(monitor_data, http_records_data);
      lastUpdated.value = new Date().toLocaleString();
      return { success: true, error: "" };
    } else {
      alertStore.addAlert(http_records_data.message, "danger");
      return { success: false, error: http_records_data.message };
    }
  } else {
    alertStore.addAlert(monitor_data.message, "danger");
    return { success: false, error: monitor_data.message };
  }
}

function setupMonitorsPoll() {
  pollInterval = setInterval(async () => {
    fetchData();
  }, 30 * 1000);
}

onMounted(() => {
  setupMonitorsPoll();
});

onUnmounted(() => {
  clearInterval(pollInterval);
});
</script>

<template>
  <data-fetcher :fetcher="fetchData">
    <div class="w-full min-h-screen items-center">
      <div class="flex font-bold text-white py-16 w-full">
        <h1 class="mx-auto text-6xl">PSD Status</h1>
      </div>
      <div class="flex text-black w-full flex-col">
        <div
          class="flex flex-row space-x-4 mx-auto bg-white px-10 w-auto h-12 rounded-full items-center drop-shadow-md"
        >
          <div class="flex items-center gap-x-2" data-attribute="green-systems">
            <span class="h-10 w-10 rounded-full bg-green-400"></span>
            <p>{{ numOfGreenSystems }} systems</p>
          </div>
          <div
            class="flex items-center gap-x-2"
            data-attribute="yellow-systems"
          >
            <span class="h-10 w-10 rounded-full bg-yellow-400"></span>
            <p>{{ numOfYellowSystems }} systems</p>
          </div>
          <div class="flex items-center gap-x-2" data-attribute="red-systems">
            <span class="h-10 w-10 rounded-full bg-red-400"></span>
            <p>{{ numOfRedSystems }} systems</p>
          </div>
        </div>
        <div class="flex m-5 mx-auto text-white">
          <p>Last updated: {{ lastUpdated }}</p>
        </div>
      </div>
      <div class="flex flex-wrap p-5 mx-auto justify-center">
        <div v-for="monitor in monitors" :key="monitor.id">
          <monitor-card :monitor="monitor" />
        </div>
      </div>
    </div>
  </data-fetcher>
</template>
