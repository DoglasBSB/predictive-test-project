//const { Enter } = require('wd/lib/special-keys')

Cypress.on('uncaught:exception', (err, runnable) => {
  // returning false here prevents Cypress from
  // failing the test
  return false
})

//Login
Cypress.Commands.add('guiLogin', (
  username = Cypress.env('USER_EMAIL'),
  password = Cypress.env('USER_PASSWORD')
) => {
  cy.intercept('GET', '**/login').as('getLogin')
  cy.visit('/login')
  cy.get('#user').type(username)
  cy.get('#password').type(password, { log: false })
  cy.get('#btnLogin').click()
  cy.wait('@getLogin')
  cy.contains('h2', 'Login realizado').should('be.visible')
  cy.get('.swal2-confirm').click()
})

//Session
Cypress.Commands.add('sessionLogin', (
  username = Cypress.env('USER_EMAIL'),
  password = Cypress.env('USER_PASSWORD')
) => {
  const login = () => cy.guiLogin(username, password)
  cy.session(username, login)
})

Cypress.Commands.add('buscarProduto', () => {
  // Campo de Busca
  cy.intercept('GET', '**/my-account#search').as('getSearch')
  cy.visit('/my-account#search')
  cy.get(':nth-child(3) > .search_width > img').click()
  cy.get('form > input').type('mobile').type('{enter}')
  cy.get('.swal2-confirm').click()
  //cy.wait('@getSearch')
})

Cypress.Commands.add('selecionarProduto', () => {
  //Selecionar produto "Monitor"
  cy.intercept('GET', '**/shop').as('getShop')
  cy.visit('/shop')
  cy.get(':nth-child(1) > .product_wrappers_one > .content > .title > a').click()
  cy.wait('@getShop')
})

Cypress.Commands.add('adicionarProduto', () => {
 //Adicionar no carrinho
 cy.intercept('GET', '**/product-details-one/1').as('getProduct')
 cy.visit('/product-details-one/1')
 //ERRO AQUI
 cy.get('.inks_Product_areas > .theme-btn-one').click()
 cy.wait(3000)
 cy.get('.modal_product_content_one > h3').should('have.text', 'Green Dress For Woman')
 cy.wait('@getProduct')

 //Verificar se o produto está no carrinho
 cy.get('.col-12 > .header-action-link > :nth-child(2) > .offcanvas-toggle > .fa').click()
 cy.get('.offcanvas-cart-action-button > :nth-child(1) > .theme-btn-one').click()
 cy.get(':nth-child(4) > .product_name > a').should('be.visible')
})

Cypress.Commands.add('checkout', () => {
//Prosseguir para o checkout
cy.intercept('GET', '**/checkout-one').as('getCheckout')
cy.visit('/checkout-one')
//cy.get('.checkout_btn > .theme-btn-one').click()
cy.wait('@getCheckout')

//Preencher formulário
cy.get('#fname').type('Marcia Gonzalez')
cy.get('#lname').type('Caldeira')
cy.get('#cname').type('DQAtest ')
cy.get('#email').type('qatest@gmail.com')
cy.get('#country').type('usa')
cy.get('#city').type('Aland Islands')
cy.get('#zip').type('72548-508')
cy.get('#faddress').type('Quadra QR 218 Conjunto H')
cy.get('#messages').type('Realizando teste de regressão!')

//save
cy.get('.form-check-label').click()
cy.get('.checkout-area-bg > .theme-btn-one').click()

//assert
cy.get(':nth-child(2) > h3').should('have.text', 'Billings Information registred with success!')

//Payment
cy.get(':nth-child(2) > .check-heading > h3').should('be.visible')

//button
cy.get(':nth-child(2) > :nth-child(2) > .theme-btn-one').click()

//assert
cy.contains('h2', 'Order success!').should('be.visible')
cy.get('.offer_modal_left > h3').should('have.text', 'Congrats! Your order was created with sucess!')
})

Cypress.Commands.add('finalizarCompra', () => {

//button
cy.get(':nth-child(2) > :nth-child(2) > .theme-btn-one').click()

//assert
cy.contains('h2', 'Order success!').should('be.visible')
cy.get('.offer_modal_left > h3').should('have.text', 'Congrats! Your order was created with sucess!')
})