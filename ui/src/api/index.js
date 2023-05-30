import axios from "axios";

export function authenticate(userData) {
  return axios.post(
    `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/login`,
    userData
  );
}

export function getMonitors(ids = []) {
  const query_string = ids.length ? `?ids=${ids}` : "";
  return axios.get(
    `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/monitors` + query_string
  );
}

export function getHttpRecords(monitor_ids = [], limit = "") {
  let query_string = `?monitor_ids=${monitor_ids}`;
  query_string = limit ? query_string + `&limit=${limit}` : query_string;
  return axios.get(
    `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/http_records` + query_string
  );
}

export function getProtocols() {
  return axios.get(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/protocols`);
}

export function createMonitor(monitorData, jwt) {
  return axios.post(
    `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/monitor`,
    monitorData,
    { headers: { Authorization: `Bearer: ${jwt}` } }
  );
}
