<script setup>
import { onMounted, ref } from "vue";
import { useAlertStore } from "../stores/alertStore";
const alertStore = useAlertStore();
const props = defineProps({
  fetcher: {
    type: Function,
    required: true,
    default: () => {},
  },
});
const isLoading = ref(true);
const isError = ref(false);

async function getData() {
  isLoading.value = true;
  isError.value = false;
  const { success, error } = await props.fetcher();
  if (!success) {
    isError.value = true;
    alertStore.addAlert(`Error updating monitor: ${error}`, "danger");
  } else {
    isLoading.value = false;
  }
}

onMounted(() => getData());
</script>
<template>
  <div>
    <div
      v-if="isLoading"
      class="flex flex-col w-full items-center justify-center min-h-screen"
    >
      <img
        class="w-1/2 h-1/2"
        src="../assets/psd-status.svg"
        alt="PSD Status logo"
      />
      <h1 class="p-5 text-5xl text-white font-bold">Loading...</h1>
    </div>
    <div
      v-else-if="isError"
      class="flex flex-col w-full items-center justify-center"
    >
      <p class="flex mb-5 mt-10 text-lg font-bold">
        There was an error retrieving the data
      </p>
      <button
        class="mx-auto mt-5 w-32 bg-sdb-400 p-2 text-white rounded-lg text-base"
        data-action="login"
        @click="getData()"
      >
        Retry
      </button>
    </div>
    <slot v-else />
  </div>
</template>
