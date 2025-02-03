describe('Fluxo de Checkout', () => {
  beforeEach(() => {
    //cy.intercept('GET', '**/login').as('getLogin')
    //cy.sessionLogin()
    
  })

  
  it('Deve concluir a compra com sucesso', () => {
    cy.guiLogin()
    cy.buscarProduto()
    cy.selecionarProduto()
    cy.adicionarProduto()
    cy.checkout()

  })

})