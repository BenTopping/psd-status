import { createRouter, createWebHashHistory } from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import { useAuthenticationStore } from './stores/authStore'

const routes = [
    {
        path: '/',
        component: Home,
    },
    {
        path: '/login',
        component: Login,
        beforeEnter(to, from, next) {
            const store = useAuthenticationStore()
            if (store.isAuthenticated) {
                next('/')
            } else {
                next()
            }
        }
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
