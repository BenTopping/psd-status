import axios from 'axios'

export function authenticate (userData) {
    return axios.post(`${import.meta.env.VITE_PSD_STATUS_BASE_URL}/login`, userData)
}