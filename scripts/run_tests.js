const { execSync } = require('child_process');
const path = require('path');

try {
    console.log("🔍 Executando previsão de falha...");
    const pythonCmd = process.platform === "win32" ? "python" : "python3";
    const predictionOutput = execSync(`${pythonCmd} ../ml_model/predict_test_failure.py`, { encoding: 'utf-8' });

    console.log(`📊 Resultado da previsão:\n${predictionOutput}`);

    if (predictionOutput.includes("Alta chance de falha!")) {
        console.log("🚀 Rodando testes Cypress...");
        execSync('npx cypress run --spec cypress/e2e/checkout.cy.js', { stdio: 'inherit', cwd: path.resolve(__dirname, '..') });
    } else {
        console.log("✅ Baixa chance de falha. Cypress não será executado.");
    }
} catch (error) {
    console.error("❌ Erro ao executar previsão:", error.message);
}

