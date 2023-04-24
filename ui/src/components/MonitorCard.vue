<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  monitor: {},
})
const statusColour = computed(() => {
    console.log(props.monitor)
    return props.monitor ? `bg-${props.monitor.current_state}-400` : 'bg-gray-400'
})

</script>

<template>
    <div class="flex w-96 h-64 items-center bg-white p-5 m-5 space-x-5 rounded-lg drop-shadow-md">
        <span :class="`flex h-32 w-32 rounded-full ${statusColour}`"></span>
        <div class="flex flex-col">
            <p class="text-lg font-bold">{{ monitor.name }}</p>
            <p class="text-md font-">Last response time: {{ monitor.http_records[monitor.http_records.length - 1]?.response_time }}s</p>
            <p class="text-md font-">Average uptime: {{ monitor.average_uptime }}%</p>
        </div>
    </div>
</template>

