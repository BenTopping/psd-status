<script setup>
import Navbar from "./components/NavBar.vue";
import Footer from "./components/FooterBar.vue";
import AlertStack from "./components/AlertStack.vue";
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-t from-sdb-400 to-sp">
    <navbar />
    <router-view />
    <alert-stack />
    <Footer />
  </div>
</template>
