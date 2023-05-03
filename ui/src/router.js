import { createRouter, createWebHashHistory } from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import NotFound from './views/NotFound.vue'
import Monitors from './views/Monitors.vue'
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
    },
    {
        path: '/monitors',
        component: Monitors,
        beforeEnter(to, from, next) {
            const store = useAuthenticationStore()
            if (!store.isAuthenticated) {
                next('/login')
            } else {
                next()
            }
        }
    },
    {
        path: '/:pathMatch(.*)*',
        component: NotFound
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
