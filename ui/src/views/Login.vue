<script setup>
import { useAuthenticationStore } from "../stores/authStore.js";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useAuthenticationStore();
let username = ref("");
let password = ref("");

async function login() {
  const { success, errors } = await store.login({
    username: username.value,
    password: password.value,
  });
  if (success) {
    router.push({ path: "/", replace: true });
  }
}
</script>

<template>
  <div
    class="flex flex-col rounded-lg bg-white mx-auto my-auto items-center w-96 h-96"
  >
    <div class="flex bg-sdb-400 font-bold text-white rounded-t-lg py-5 w-full">
      <h1 class="mx-auto text-2xl">PSD Status</h1>
    </div>
    <form class="flex flex-col p-5 mx-5 my-5 w-full gap-y-3" @submit.prevent="login()">
      <div class="flex flex-col">
        <label class="px-3 text-gray-600">Username</label>
        <input
          class="border-2 border-gray-300 rounded-lg p-2 text-base"
          placeholder="Username"
          v-model="username"
          required
        />
      </div>
      <div class="flex flex-col">
        <label class="px-3 text-gray-600">Password</label>
        <input
          class="border-2 border-gray-300 rounded-lg p-2 text-base"
          placeholder="Password"
          type="password"
          v-model="password"
          required
        />
      </div>
      <button
        class="mx-auto mt-5 w-32 bg-sdb-400 p-2 text-white rounded-lg text-base"
        type="submit"
      >
        Login
      </button>
    </form>
  </div>
</template>
