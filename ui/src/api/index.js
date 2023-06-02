import axios from "axios";

export async function authenticate(userData) {
  return await axios
    .post(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/login`, userData)
    .then((response) => {
      return { success: true, data: response.data };
    })
    .catch((error) => {
      return { success: false, data: error.response.data };
    });
}

export async function getMonitors(ids = []) {
  const query_string = ids.length ? `?ids=${ids}` : "";
  return await axios
    .get(
      `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/monitors` + query_string
    )
    .then((response) => {
      return { success: true, data: response.data };
    })
    .catch((error) => {
      return { success: false, data: error.response.data };
    });
}

export async function getHttpRecords(monitor_ids = [], limit = "") {
  let query_string = `?monitor_ids=${monitor_ids}`;
  query_string = limit ? query_string + `&limit=${limit}` : query_string;
  return await axios
    .get(
      `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/http_records` +
        query_string
    )
    .then((response) => {
      return { success: true, data: response.data };
    })
    .catch((error) => {
      return { success: false, data: error.response.data };
    });
}

export async function getProtocols() {
  return await axios
    .get(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/protocols`)
    .then((response) => {
      return { success: true, data: response.data };
    })
    .catch((error) => {
      return { success: false, data: error.response.data };
    });
}

export async function createMonitor(monitorData, jwt) {
  return await axios
    .post(
      `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/monitor`,
      monitorData,
      { headers: { Authorization: `Bearer: ${jwt}` } }
    )
    .then((response) => {
      return { success: true, data: response.data };
    })
    .catch((error) => {
      return { success: false, data: error.response.data };
    });
}
