<script setup>
import { getMonitors, getProtocols } from "../api/index.js";
import { ref } from "vue";
import DataFetcher from "../components/DataFetcher.vue";
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
  const { success, data } = await getMonitors();
  if (success) {
    monitors.value = data;
  } else {
    console.log("Error retrieving protocols: ", data.message);
  }
}

async function fetchProtocols() {
  const { success, data } = await getProtocols();
  if (success) {
    protocols.value = data;
  } else {
    console.log("Error retrieving protocols: ", data.message);
  }
}

async function fetcher() {
  await fetchProtocols();
  await fetchMonitors();
  return { success: true, error: "" };
}
</script>

<template>
  <data-fetcher :fetcher="fetcher">
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
              class="flex flex-row h-32 my-2 bg-white rounded-md drop-shadow-md"
              data-attribute="monitor-item"
            >
              <div
                class="flex w-1/3 bg-sdb-400 items-center rounded-l-md text-center"
              >
                <span
                  class="flex text-xl text-center text-white p-2 text-center font-bold"
                >
                  {{ monitor.name }}
                </span>
              </div>
              <div class="flex flex-col p-3 w-2/3 justify-center w-96">
                <span class="flex text-xl mx-auto space-x-5">
                  <p class="font-light">Target:</p>
                  <p class="break-words max-w-[200px]">{{ monitor.target }}</p>
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
  </data-fetcher>
</template>
