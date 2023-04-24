<script setup>
  import { useAuthenticationStore } from '../stores/authStore.js'
  const store = useAuthenticationStore()
</script>

<template>
  <div class="relative bg-sdb-400">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex flex-row text-white py-5 justify-between">
          <div class="flex gap-x-5">
            <router-link to="/">Home</router-link>
          </div>
          <div>
            <router-link
              v-if="!store.isAuthenticated" 
              class="float-right text-sdb-100" 
              to="/login"
            >
              Login
            </router-link>
            <router-link 
              v-else
              class="float-right text-sdb-100"
              to="/"
              @click="store.logout()"
            >
              Logout
            </router-link>

          </div>
        </div>
    </div>
  </div>
</template>