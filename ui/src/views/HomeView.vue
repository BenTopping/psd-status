<script setup>
import { getMonitors } from "../api/index.js";
import { ref, onMounted, onUnmounted, computed } from "vue";
import MonitorCard from "../components/MonitorCard.vue";

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

function formatMonitors(monitorData) {
  return monitorData.map((monitor) => {
    if (monitor.http_records.length > 0) {
      if (
        monitor.http_records[monitor.http_records.length - 1].success == false
      ) {
        // Get last record and check if it failed
        monitor.current_state = "red";
      } else if (
        monitor.http_records.some((record) => record.success == false)
      ) {
        // Check if any of the records are failed
        monitor.current_state = "yellow";
      } else {
        monitor.current_state = "green";
      }
    } else {
      // If there are no records show gray
      monitor.current_state = "gray";
    }
    return monitor;
  });
}

async function fetchMonitors() {
  await getMonitors()
    .then((response) => {
      monitors.value = formatMonitors(response.data);
      lastUpdated.value = new Date().toLocaleString();
    })
    .catch((error) => {
      console.log("Error retrieving monitors: ", error);
    });
}

function setupMonitorsPoll() {
  pollInterval = setInterval(async () => {
    fetchMonitors();
  }, 30 * 1000);
}

onMounted(() => {
  fetchMonitors();
  setupMonitorsPoll();
});

onUnmounted(() => {
  clearInterval(pollInterval);
});
</script>

<template>
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
        <div class="flex items-center gap-x-2" data-attribute="yellow-systems">
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
</template>
