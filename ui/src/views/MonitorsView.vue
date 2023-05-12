<script setup>
import { getMonitors, getProtocols } from "../api/index.js";
import { ref, onMounted } from "vue";
import MonitorEdit from "../components/MonitorEdit.vue";

const monitors = ref([]);
const protocols = ref([]);
const currentMonitor = ref({});

function getProtocolName(protocol_id) {
  return (
    protocols.value.find((protocol) => protocol.id == protocol_id)?.name ||
    "Unknown"
  );
}

async function fetchMonitors() {
  await getMonitors()
    .then((response) => {
      monitors.value = response.data;
    })
    .catch((error) => {
      console.log("Error retrieving monitors: ", error);
    });
}

async function fetchProtocols() {
  await getProtocols()
    .then((response) => {
      protocols.value = response.data;
    })
    .catch((error) => {
      console.log("Error retrieving protocols: ", error);
    });
}

onMounted(async () => {
  await fetchProtocols();
  fetchMonitors();
});
</script>

<template>
  <div class="flex flex-grow p-10 mx-auto w-full max-w-screen justify-center">
    <div>
      <div class="flex border-b-2 border-gray-200 items-center">
        <p class="w-full text-xl text-white font-bold">Monitors</p>
        <button
          class="mx-auto w-16 bg-sdb-400 p-2 my-2 text-white rounded-lg text-base"
          @click="currentMonitor = {}"
          data-action="select-new-monitor"
        >
          New
        </button>
      </div>
      <div class="flex flex-col mx-auto">
        <div
          v-for="monitor in monitors"
          :key="monitor.id"
          @click="currentMonitor = monitor"
        >
          <div
            class="flex flex-row w-96 h-32 my-2 bg-white rounded-md drop-shadow-md"
            data-attribute="monitor-item"
          >
            <div
              class="flex w-1/3 bg-sdb-400 items-center rounded-l-md text-center"
            >
              <span
                class="flex text-xl text-center text-white p-2 text-center font-bold bg-sdb-400"
              >
                {{ monitor.name }}
              </span>
            </div>
            <div class="flex flex-col p-3 w-2/3 justify-center">
              <span class="flex text-xl mx-auto space-x-5">
                <p class="font-light">Target:</p>
                <p>{{ monitor.target }}</p>
              </span>
              <span class="flex text-xl mx-auto space-x-5">
                <p class="font-light">Protocol:</p>
                <p>{{ getProtocolName(monitor.protocol_id) }}</p>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mx-10 w-full max-w-[800px]">
      <div class="flex border-b-2 border-gray-200">
        <p class="w-full text-xl text-white font-bold py-3">
          {{ currentMonitor.name || "New" }}
        </p>
      </div>
      <MonitorEdit
        :monitor="currentMonitor"
        :protocols="protocols"
        @fetch-monitors="fetchMonitors"
      />
    </div>
  </div>
</template>