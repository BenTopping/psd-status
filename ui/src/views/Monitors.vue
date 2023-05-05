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
          <div class="flex flex-row w-96 h-32 my-2 bg-white rounded-md drop-shadow-md">
            <div class="flex w-1/3 bg-sdb-400 items-center rounded-l-md text-center">
                <span class="flex text-xl text-center text-white p-2 text-center font-bold bg-sdb-400">
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
                <p>{{ monitor.protocol_name }}</p>
              </span>
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
