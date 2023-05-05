<script setup>
import { ref, computed, watchEffect } from "vue";
import { createMonitor } from '../api'

const props = defineProps({
  monitor: {},
});

// This clones the monitor prop whilst also updating if the prop changes
const currentMonitor = ref();
watchEffect(() => (currentMonitor.value = { ...props.monitor }));

async function createOrUpdateMonitor() {
    console.log('creating monitor')
}
</script>

<template>
  <div
    class="flex flex-col w-full max-w-[800px] mt-2 rounded-lg drop-shadow-md bg-white"
  >
    <div class="flex bg-sdb-400 font-bold text-white rounded-t-lg py-5 w-full">
        <h1 class="mx-auto text-2xl">{{ currentMonitor.name || "New" }}</h1>
    </div>
    <form class="flex flex-col p-5 w-full gap-y-3" @submit.prevent="createOrUpdateMonitor()">
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold">Protocol</label>
        <select
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          v-model="currentMonitor.protocol_name"
          required
        >
          <option value="http">http</option>
          <option value="https">https</option>
        </select>
      </div>
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold">Target</label>
        <input
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          placeholder="www.test.com"
          v-model="currentMonitor.target"
          required
        />
      </div>
      <div class="flex flex-col">
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold">Poll delay</label>
        <select
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          v-model="currentMonitor.delay"
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
        <label class="text-sp px-3 m-3 border-b-2 border-sp font-bold">Active?</label>
        <select
          class="border-2 border-gray-300 rounded-lg p-2 text-black mx-3"
          v-model="currentMonitor.active"
          required
        >
          <option value="True">True</option>
          <option value="False">False</option>
        </select>
      </div>
      <button
        class="mx-auto w-32 bg-sdb-400 p-2 my-2 text-white rounded-lg text-base"
        type="submit"
      >
        {{ currentMonitor.id ? "Update" : "Create" }}
      </button>
    </form>
  </div>
</template>
