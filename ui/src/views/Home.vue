<script setup>
  import { getMonitors } from '../api/index.js'
  import { ref, onMounted, computed } from 'vue'
  import MonitorCard from '../components/MonitorCard.vue'

  let monitors = ref([])
  let lastUpdated = ref(new Date().toLocaleString())

  const numOfRedSystems = computed(() => {
    return monitors.value.filter((monitor) => monitor.current_state == 'red').length
  })
  const numOfGreenSystems = computed(() => {
    return monitors.value.filter((monitor) => monitor.current_state == 'green').length
  })
  const numOfYellowSystems = computed(() => {
    return monitors.value.filter((monitor) => monitor.current_state == 'yellow').length
  })


  async function fetchMonitors() {
    await getMonitors()
    .then(response => {
      monitors.value = response.data
      lastUpdated.value = new Date().toLocaleString()
    })
    .catch(error => {
      console.log('Error Authenticating: ', error)
    })
  }

  function setupMonitorsPoll() {
    setInterval(async () => {
      fetchMonitors()
    }, 30 * 1000)
  }

  onMounted(() => {
    fetchMonitors();
    setupMonitorsPoll()
  })

</script>

<template>
  <div class="w-full items-center">
    <div class="flex bg-sdb-400 font-bold text-white py-20 w-full">
      <h1 class="mx-auto text-6xl">PSD Status</h1>
    </div>
    <div class="flex bg-sdb-400 text-black w-full flex-col">
      <div class="flex flex-row space-x-4 mx-auto bg-white px-10 w-auto h-12 rounded-full items-center">
        <div class="flex items-center gap-x-2">
          <span class="h-10 w-10 rounded-full bg-green-400"></span>
          <p>{{numOfGreenSystems}} systems</p>
        </div>
        <div class="flex items-center gap-x-2">
          <span class="h-10 w-10 rounded-full bg-yellow-400"></span>
          <p>{{numOfYellowSystems}} systems</p>
        </div>
        <div class="flex items-center gap-x-2">
          <span class="h-10 w-10 rounded-full bg-red-400"></span>
          <p>{{numOfRedSystems}} systems</p>
        </div>
      </div>
      <div class="flex m-5 mx-auto text-sdb-100"> 
        <p>Last updated: {{ lastUpdated }}</p>
      </div>
    </div>
    <div class="flex flex-wrap p-10 mx-auto justify-center">
      <div v-for="monitor in monitors" :key="monitor.id">
        <monitor-card :monitor="monitor"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>