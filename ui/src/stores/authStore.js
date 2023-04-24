import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authenticate } from '../api'
import { isValidJwt } from '../utils'

export const useAuthenticationStore = defineStore('authentication', () => {
    let user = ref({})
    let jwt = ref('')

    async function login(userData) {
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

    function logout() {
        user.value = {}
        jwt.value = ''
        localStorage.token = ''
    }

    const isAuthenticated = computed(() => {
        if (localStorage.token) {
            jwt.value = localStorage.token
        }
        return isValidJwt(jwt.value)
    })

    return { user, jwt, login, logout, isAuthenticated }
})