<script setup>
import { getMonitors, getHttpRecords, getProtocols } from "../api/index.js";
import { onMounted, computed, ref } from "vue";
import { useRoute } from "vue-router";
import { useAlertStore } from "../stores/alertStore.js";
import ResponseTimeChart from "../components/ResponseTimeChart.vue";
import StatusTable from "../components/StatusTable.vue";

const alertStore = useAlertStore();
const route = useRoute();
const monitor_id = computed(() => route.params.id);
const monitor = ref({});
const protocols = ref([]);

// TODO: Extract all this common behaviour to an external file and consolidate
function formatMonitors(monitorData, httpRecords) {
  // Join http records and monitors together
  monitorData.http_records = httpRecords;
  // Calculate monitors current state based on its http_records
  if (monitorData.http_records.length > 0) {
    if (
      monitorData.http_records[monitorData.http_records.length - 1].success ==
      false
    ) {
      // Get last record and check if it failed
      monitorData.current_state = "red";
    } else if (
      // Get last 10 records
      monitorData.http_records
        .slice(Math.max(monitorData.http_records.length - 10, 0))
        .some((record) => record.success == false)
    ) {
      // Check if any of the records are failed
      monitorData.current_state = "yellow";
    } else {
      monitorData.current_state = "green";
    }
  } else {
    // If there are no records show gray
    monitorData.current_state = "gray";
  }
  return monitorData;
}

async function fetchMonitor() {
  return await getMonitors(monitor_id.value)
    .then((response) => {
      return { success: true, response: response.data };
    })
    .catch((error) => {
      return { success: false, response: error.response.data };
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

async function fetchHttpRecords(monitor_ids) {
  return await getHttpRecords(monitor_ids)
    .then((response) => {
      return { success: true, response: response.data };
    })
    .catch((error) => {
      return { success: false, response: error.response.data };
    });
}

async function fetchData() {
  await fetchMonitor().then(async ({ success, response: monitor_response }) => {
    if (success) {
      // We are expecting a list of monitors but we want the first
      monitor.value = monitor_response[0];
      await fetchHttpRecords(monitor_id.value).then(
        ({ success, response: http_records_response }) => {
          if (success) {
            monitor.value = formatMonitors(
              monitor_response[0],
              http_records_response
            );
          } else {
            alertStore.addAlert(http_records_response.message, "danger");
          }
        }
      );
    } else {
      alertStore.addAlert(monitor_response.message, "danger");
    }
  });
}

function getProtocolName(protocol_id) {
  return (
    protocols.value.find((protocol) => protocol.id == protocol_id)?.name ||
    "Unknown"
  );
}

onMounted(async () => {
  await fetchData();
  await fetchProtocols();
});
</script>
<template>
  <div class="w-full min-h-screen items-center text-white text-xl">
    <div class="items-center mx-16 my-10">
      <div
        class="flex border-b-2 border-gray-200 justify-center items-center pb-10"
      >
        <div class="flex pr-20">
          <span
            :class="`w-64 h-64 rounded-full drop-shadow-md bg-${monitor.current_state}-400`"
          ></span>
        </div>
        <div class="w-full">
          <div class="flex flex-col">
            <h2 class="flex text-5xl text-white font-bold py-5">
              {{ monitor.name || "Unknown" }}
            </h2>
            <div class="flex flex-row space-x-20">
              <div class="flex-col">
                <span class="flex flex-row space-x-3">
                  <p>Last response time:</p>
                  <p class="text-black">
                    {{
                      monitor.http_records
                        ? monitor.http_records[monitor.http_records.length - 1]
                            .response_time
                        : 0
                    }}s
                  </p>
                </span>
                <span class="flex flex-row space-x-3">
                  <p>Average uptime:</p>
                  <p class="text-black">{{ monitor.average_uptime }}%</p>
                </span>
                <span class="flex flex-row space-x-3">
                  <p>SSL expiry date:</p>
                  <p class="text-black">
                    {{ monitor.ssl_expiry_date || "None" }}
                  </p>
                </span>
              </div>
              <div class="flex-col">
                <span class="flex flex-row space-x-3">
                  <p>Protocol:</p>
                  <p class="text-black">
                    {{ getProtocolName(monitor.protocol_id) }}
                  </p>
                </span>
                <span class="flex flex-row space-x-3">
                  <p>Target:</p>
                  <p class="text-black">{{ monitor.target }}</p>
                </span>
                <span class="flex flex-row space-x-3">
                  <p>Poll interval:</p>
                  <p class="text-black">{{ monitor.delay }}s</p>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex space-x-5">
        <div class="flex w-full py-5 rounded-lg">
          <response-time-chart
            v-if="monitor.http_records?.length"
            :http_records="monitor.http_records"
          />
        </div>
        <div class="flex flex-col w-full py-5 rounded-lg">
          <div
            class="flex bg-sdb-400 font-bold text-white rounded-t-lg py-5 w-full"
          >
            <h1 class="mx-auto text-2xl">Incidents</h1>
          </div>
          <div
            class="flex w-full h-full bg-white rounded-b-lg overflow-y-scroll"
          >
            <status-table
              v-if="monitor.http_records?.length"
              :items="
                monitor.http_records.filter(
                  (http_record) => http_record.success == false
                )
              "
              :fields="[
                { key: 'id', label: 'Record id' },
                { key: 'errors', label: 'Error' },
                { key: 'created_at', label: 'Incident time' },
              ]"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
