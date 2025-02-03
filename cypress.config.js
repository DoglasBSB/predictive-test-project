const { defineConfig } = require("cypress");

module.exports = defineConfig({
  chromeWebSecurity: false,
  viewportWidth: 1280,
  viewportHeight: 720,
  e2e: {
    baseUrl: 'https://automationpratice.com.br/',
    specPattern: "cypress/e2e/**/*.cy.js",
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
