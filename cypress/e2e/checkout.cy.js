import { qase } from 'cypress-qase-reporter/mocha'

describe('Fluxo de Checkout', () => {
  beforeEach(() => {
  })

  qase(1, it('Deve concluir a compra com sucesso', () => {
    cy.guiLogi()
    cy.buscarProduto()
    cy.selecionarProduto()
    cy.adicionarProduto()
    cy.checkout()
  }))
})