<script setup>
import { useAuthenticationStore } from "../stores/authStore.js";
import { useAlertStore } from "../stores/alertStore.js";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const authStore = useAuthenticationStore();
const alertStore = useAlertStore();
const username = ref("");
const password = ref("");

async function login() {
  const { success, error } = await authStore.login({
    username: username.value,
    password: password.value,
  });
  if (success) {
    router.push({ path: "/", replace: true });
    alertStore.clearAlerts();
    alertStore.addAlert("Successfully logged in!", "success");
  } else {
    alertStore.addAlert(`Error logging in: ${error}`, "danger");
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
    <form
      class="flex flex-col p-5 mx-5 my-5 w-full gap-y-3"
      @submit.prevent="login()"
    >
      <div class="flex flex-col">
        <label class="px-3 text-gray-600">Username</label>
        <input
          class="border-2 border-gray-300 rounded-lg p-2 text-base"
          placeholder="Username"
          v-model="username"
          data-attribute="username-input"
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
          data-attribute="password-input"
          required
        />
      </div>
      <button
        class="mx-auto mt-5 w-32 bg-sdb-400 p-2 text-white rounded-lg text-base"
        type="submit"
        data-action="login"
      >
        Login
      </button>
    </form>
  </div>
</template>
