# Projeto de Teste Preditivo

Este projeto visa implementar um sistema de testes preditivos utilizando dados de testes de software para prever falhas ou sucessos nos testes. O fluxo é integrado ao Qase para gerenciamento de casos de teste, com execução automatizada de testes utilizando o Cypress e modelagem preditiva com Python.

## Estrutura do Projeto

- **Qase**: Ferramenta de gestão e gerenciamento de casos de teste, onde os dados são coletados para treinar o modelo preditivo.
- **Cypress**: Framework de testes automatizados, com foco na regressão da funcionalidade "checkout.cy.js".
- **Cypress Cloud**: Dashboard para monitoramento e visualização dos resultados dos testes automatizados.
- **GitHub Actions**: Pipeline de CI/CD que executa os testes automaticamente em cada push para o repositório.
- **Python**: Scripts utilizados para preparar os dados, treinar o modelo preditivo e realizar previsões de falhas.

## Tecnologias e Ferramentas

- **Cypress**: Testes E2E automatizados.
- **Qase**: Gestão de testes.
- **GitHub Actions**: Automação de CI/CD.
- **Python**: Para modelagem preditiva com aprendizado de máquina.
  - **Random Forest**: Algoritmo de ML utilizado para treinamento do modelo.
  - **LSTM (Long Short-Term Memory)**: Usado para prever falhas em testes.

## Como Funciona

### Fluxo de Execução

1. **Coleta de Dados**: A cada execução de testes, os dados de falhas ou sucessos são registrados no Qase.
2. **Treinamento do Modelo**: O script `train_lstm.py` utiliza esses dados para treinar um modelo preditivo.
3. **Predição de Falhas**: O script `predict_test_failure.py` carrega o modelo treinado e faz previsões sobre a probabilidade de falha de novos testes.
4. **Execução dos Testes**: Com base na previsão do modelo, a pipeline de CI/CD executa ou pula os testes.
5. **Monitoramento**: Os resultados dos testes são exibidos no **Cypress Cloud** e registrados no Qase.

### Arquivos e Scripts

- **scripts/**
  - `run_tests.js`: Roda os testes Cypress.
  - `prepare_data.py`: Prepara os dados de falhas/sucessos para o treinamento.
  - `train_lstm.py`: Treina o modelo de previsão.
  - `predict_test_failure.py`: Faz previsões usando o modelo treinado.

- **workflow GitHub Actions**: Configuração de CI/CD para execução automatizada dos testes e previsão de falhas.

## Como Configurar

1. **Clone o repositório**:

   ```bash
   git clone <URL do repositório>

2. **Instale as dependências:**:

   ```bash
   npm install

  ```bash
   pip install -r requirements.txt


3. **Configure o Qase:**:
    - Adicione sua chave de API do Qase no arquivo de configuração

4. **Configure o GitHub Actions:**:
    - Acesse o seu repositório no GitHub e habilite o fluxo de CI/CD no Actions.

3. **Execute os testes:**:
    - Rode os testes localmente:
      ```bash
     npm run cypress:open

     Obs:. A execução dos testes na pipeline será automaticamente disparada com cada novo push.

## Contribuindo

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias no projeto.

## Licença
Este projeto é licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.