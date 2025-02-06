const { defineConfig } = require('cypress')
require('dotenv').config(); // Carregar variáveis do .env

module.exports = defineConfig({
  projectId: 'to1eev',
  chromeWebSecurity: false,
  viewportWidth: 1280,
  viewportHeight: 720,
  reporter: 'cypress-multi-reporters',
  reporterOptions: {
    reporterEnabled: 'cypress-mochawesome-reporter, cypress-qase-reporter',
    cypressMochawesomeReporterReporterOptions: {
      charts: true,
    },
    cypressQaseReporterReporterOptions: {
      debug: true,

      testops: {
        api: {
          token: process.env.QASE_API_KEY, // Agora usa a variável de ambiente
        },

        project: 'CPQ',
        uploadAttachments: true,

        run: {
          complete: true,
        },
      },

      framework: {
        cypress: {
          screenshotsFolder: 'cypress/screenshots',
        }
      }
    },
  },
  video: false,
  e2e: {
     baseUrl: 'https://automationpratice.com.br/',
     setupNodeEvents(on, config) {
      require('cypress-qase-reporter/plugin')(on, config)
      require('cypress-qase-reporter/metadata')(on)
    },
  },
});