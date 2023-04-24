import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMonitorStore = defineStore('monitor', () => {

    async function getMonitors() {
        user = userData
        return authenticate(userData)
            .then(response => {
                jwt.value = response.data.token
                localStorage.token = response.data.token
                return { success: true, error: "" }
            })
            .catch(error => {
                console.log('Error Authenticating: ', error)
                return { success: false, error: error }
            })
    }

    return { getMonitors }
})