<script setup>
import { onMounted } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  http_records: Array,
});

function updateChart(ctx) {
  if (props.http_records?.length) {
    new Chart(ctx, {
      type: "line",
      data: {
        datasets: [
          {
            label: "Response time (ms)",
            data: props.http_records?.map((record) => {
              return { y: record.response_time, x: record.created_at };
            }),
            borderWidth: 1,
            backgroundColor: "#00ff00",
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
}

onMounted(() => {
  const ctx = document.getElementById("response-time-chart");
  updateChart(ctx);
});
</script>

<template>
  <div class="flex w-full">
    <div
      v-if="props.http_records?.length"
      class="bg-white flex w-full rounded-lg"
    >
      <canvas id="response-time-chart" class="flex w-full"></canvas>
    </div>
    <div v-else>
      <p class="flex text-xl text-white font-bold">
        Sorry there was a problem building the chart!
      </p>
    </div>
  </div>
</template>
