import { defineStore } from "pinia";
import { ref, computed } from "vue";

// A central store to handle alerts across components
export const useAlertStore = defineStore("alerts", () => {
  const alerts = ref([]);

  function addAlert(message, variant) {
    alerts.value.push({ message, variant });
  }

  function removeAlert(alertIndex) {
    alerts.value.splice(alertIndex, 1);
  }

  function clearAlerts() {
    alerts.value = [];
  }

  const hasAlerts = computed(() => !!Object.keys(alerts.value).length);

  return { alerts, addAlert, removeAlert, clearAlerts, hasAlerts };
});
