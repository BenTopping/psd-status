<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-t from-sdb-400 to-sp">
    <navbar/>
    <router-view />
    <Footer/>
  </div>
</template>

