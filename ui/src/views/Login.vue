<script setup>
    import { useAuthenticationStore } from '../stores/index.js'
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const store = useAuthenticationStore()
    let username = ref('')
    let password = ref('')

    async function login() {
        const { success, errors } = await store.login({
            username: username.value,
            password: password.value
        })
        if (success) {
            router.push({ path: '/', replace: true })
        }
    }
</script>

<template>
  <div>
    <input v-model="username"/>
    <input v-model="password"/>
    <button @click="login()"/>
  </div>
</template>