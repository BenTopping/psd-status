<script setup>
import NavBar from "./components/NavBar.vue";
import FooterBar from "./components/FooterBar.vue";
import AlertStack from "./components/AlertStack.vue";
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-t from-sdb-400 to-sp">
    <nav-bar />
    <router-view />
    <alert-stack />
    <footer-bar />
  </div>
</template>
