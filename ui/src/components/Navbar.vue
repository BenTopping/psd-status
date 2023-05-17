<script setup>
import { useAuthenticationStore } from "../stores/authStore.js";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useAlertStore } from "../stores/alertStore.js";

const authStore = useAuthenticationStore();
const alertStore = useAlertStore();

const dropdown = {
  active: ref(false),
  close: () => {
    dropdown.active.value = false;
  },
  toggle: () => {
    dropdown.active.value = !dropdown.active.value;
  },
};

function handleLogout() {
  authStore .logout();
  dropdown.toggle();
  alertStore.addAlert('Successfully logged out!', 'success')
}

onBeforeUnmount(() => {
  document.removeEventListener("click", dropdown.close);
});

onMounted(() => {
  document.addEventListener("click", dropdown.close);
});
</script>

<template>
  <div class="relative bg-sdb-400">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex flex-row text-white items-center py-5 justify-between">
        <div class="flex gap-x-5">
          <router-link to="/">Home</router-link>
        </div>
        <div>
          <router-link
            v-if="!authStore.isAuthenticated"
            class="float-right text-sdb-100"
            to="/login"
          >
            Login
          </router-link>
          <div v-else class="relative inline-block text-left">
            <div>
              <button
                type="button"
                class="inline-flex w-full justify-center gap-x-2 rounded-md bg-sdb-500 px-3 py-2 text-sm font-semibold text-white shadow-sm"
                id="menu-button"
                aria-expanded="true"
                aria-haspopup="true"
                data-action="show-admin-dropdown"
                @click.stop="dropdown.toggle()"
              >
                Admin
                <svg
                  class="-mr-1 h-5 w-5 text-gray-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
            <div
              class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg focus:outline-none"
              role="menu"
              aria-orientation="vertical"
              aria-labelledby="menu-button"
              tabindex="-1"
              v-if="dropdown.active.value"
            >
              <div class="py-1 divide-y-2 divide-gray-300" role="none">
                <div>
                  <router-link
                    class="text-gray-700 block px-4 py-2 text-sm"
                    to="/random"
                    @click="dropdown.toggle()"
                  >
                    Not found
                  </router-link>
                  <router-link
                    class="text-gray-700 block px-4 py-2 text-sm"
                    to="/monitors"
                    @click="dropdown.toggle()"
                  >
                    Manage monitors
                  </router-link>
                </div>
                <router-link
                  class="text-gray-700 block px-4 py-2 text-sm"
                  to="/"
                  @click="handleLogout()"
                >
                  Logout
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
