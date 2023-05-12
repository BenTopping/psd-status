import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    setupNodeEvents() {
      // implement node event listeners here
    },
    baseUrl: "http://localhost:5173/",
    specPattern: "cypress/specs/*.cy.{js,jsx,ts,tsx}",
    video: false,
  },
});
