<script setup>
import { getMonitors } from "../api/index.js";
import { ref, onMounted } from "vue";
import MonitorEdit from "../components/MonitorEdit.vue";

let monitors = ref([]);
let currentMonitor = ref({})

async function fetchMonitors() {
  await getMonitors()
    .then((response) => {
      monitors.value = response.data;
    })
    .catch((error) => {
      console.log("Error retrieving monitors: ", error);
    });
}

onMounted(() => {
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
        >
          New
        </button>
      </div>
      <div class="flex flex-col mx-auto">
        <div v-for="monitor in monitors" :key="monitor.id" @click="currentMonitor = monitor">
          <div class="flex flex-row w-96 h-32 items-center my-2 bg-white rounded-md drop-shadow-md">
            <span class="flex text-xl p-2 text-center font-bold">
              {{ monitor.name }}
            </span>
            <div class="flex flex-col p-3 w-full">
              <span class="flex text-xl mx-auto space-x-5">
                <p class="font-light">Target:</p>
                <p>{{ monitor.target }}</p>
              </span>
              <span class="flex text-xl mx-auto space-x-5">
                <p class="font-light">Protocol:</p>
                <p>{{ monitor.protocol }}</p>
              </span>
              <span class="flex text-xl mx-auto">{{ monitor.protocol }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mx-10 w-full max-w-[800px]">
      <div class="flex border-b-2 border-gray-200">
        <p class="w-full text-xl text-white font-bold py-3">{{ currentMonitor.name || 'New' }}</p>
      </div>
      <MonitorEdit :monitor="currentMonitor"/>
    </div>
  </div>
</template>
