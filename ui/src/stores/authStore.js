import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authenticate } from "../api";
import { isValidJwt } from "../utils";

// A store to handle user sessions
export const useAuthenticationStore = defineStore("authentication", () => {
  const user = ref({});
  const jwt = ref("");

  async function login(userData) {
    user.value = userData;
    return authenticate(userData)
      .then((response) => {
        jwt.value = response.data.token;
        localStorage.token = response.data.token;
        return { success: true, error: "" };
      })
      .catch((error) => {
        return { success: false, error: error.response.data.message };
      });
  }

  function logout() {
    user.value = {};
    jwt.value = "";
    localStorage.token = "";
    return { success: true, error: "" };
  }

  const isAuthenticated = computed(() => {
    if (localStorage.token) {
      jwt.value = localStorage.token;
    }
    return isValidJwt(jwt.value);
  });

  return { user, jwt, login, logout, isAuthenticated };
});
