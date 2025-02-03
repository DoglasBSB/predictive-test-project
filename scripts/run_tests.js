const { execSync } = require('child_process');
const path = require('path');

console.log("🔍 Executando previsão de falha...");
try {
    // Executa o modelo de IA e captura a saída
    const predictionOutput = execSync('python3 ../ml_model/predict_test_failure.py', { encoding: 'utf-8' });

    console.log(`📊 Resultado da previsão:\n${predictionOutput}`);

    // Verifica se há uma alta probabilidade de falha
    if (predictionOutput.includes("Alta chance de falha!")) {
        console.log("🚀 Rodando testes Cypress...");
        const projectRoot = path.resolve(__dirname, '..'); // Caminho para a raiz do projeto
        execSync('npx cypress run --spec cypress/e2e/checkout.cy.js', { stdio: 'inherit', cwd: projectRoot });

        //execSync('npx cypress run --spec cypress/e2e/checkout.cy.js', { stdio: 'inherit' });

    } else {
        console.log("✅ Baixa chance de falha. Cypress não será executado.");
    }
} catch (error) {
    console.error("❌ Erro ao executar previsão:", error.message);
}
