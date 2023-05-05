import axios from 'axios'

export function authenticate (userData) {
    return axios.post(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/login`, userData)
}

export function getMonitors () {
    return axios.get(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/monitors`)
}

export function createMonitor (monitorData) {
    return axios.post(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/monitor`, monitorData)
}