import axios from "axios";

export function authenticate(userData) {
  return axios.post(
    `${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/login`,
    userData
  );
}

export function getMonitors() {
  return axios.get(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/v1/monitors`);
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
