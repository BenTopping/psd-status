<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
defineProps({
  monitor: Object,
});
</script>

<template>
  <div
    class="flex flex-col w-96 h-64 bg-white p-3 m-5 rounded-lg drop-shadow-md cursor-pointer"
    data-attribute="monitor-card"
    @click="router.push(`monitor/${monitor.id}`)"
  >
    <span class="flex border-b-2 mb-5 p-2 w-full">
      <h2 class="text-lg w-full text-center font-semibold">
        {{ monitor.name }}
      </h2>
    </span>
    <div class="flex flex-row w-full space-x-5">
      <div class="flex">
        <span
          :class="`w-40 h-40 rounded-full drop-shadow-md bg-${monitor.current_state}-400`"
        ></span>
      </div>
      <div class="flex flex-col justify-center font-sm">
        <span class="flex flex-col">
          <p>Last response time:</p>
          <p class="text-gray-500">
            {{
              monitor.http_records[monitor.http_records.length - 1]
                ?.response_time || 0
            }}s
          </p>
        </span>
        <span class="flex flex-col">
          <p>Average uptime:</p>
          <p class="text-gray-500">{{ monitor.average_uptime }}%</p>
        </span>
        <span v-if="monitor.ssl_expiry_date" class="flex flex-col">
          <p>SSL expiry date:</p>
          <p class="text-gray-500">{{ monitor.ssl_expiry_date }}</p>
        </span>
      </div>
    </div>
  </div>
</template>
