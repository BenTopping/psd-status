<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-l from-sdb-400 to-red-400">
    <navbar/>
    <router-view />
    <Footer/>
  </div>
</template>

