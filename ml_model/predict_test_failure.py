import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import os

# Caminhos dos arquivos
MODEL_PATH = "lstm_model.h5"  # Alterado para o nome correto do modelo treinado
SCALER_PATH = "scaler.pkl"
TEST_DATA_PATH = "test_data.csv"  # Atualizado para corresponder ao arquivo gerado

# Verifica se o arquivo de dados existe antes de tentar carregar
if not os.path.exists(TEST_DATA_PATH):
    print("⚠️ Arquivo test_data.csv não encontrado! Usando valores padrão.")
    new_test_data = np.array([[0, 0, 0]])  # Valores padrão para evitar erro
else:
    
    # Carregar os dados reais mais recentes para previsão
    df = pd.read_csv(TEST_DATA_PATH)

    # Selecionar apenas as colunas usadas no treinamento do modelo
# Aqui, ajustamos para 'failed_tests' e 'response_time' (apenas 2 características)
feature_columns = ['failed_tests', 'response_time']  # Certifique-se de que são 2 características
new_test_data = df[feature_columns].iloc[-1:].values

# Carregar o scaler salvo durante o treinamento
if not os.path.exists(SCALER_PATH):
    print("⚠️ Arquivo scaler.pkl não encontrado! Normalização pode estar incorreta.")
    scaler = None
else:
    scaler = joblib.load(SCALER_PATH)
    new_test_data = scaler.transform(new_test_data)  # 🚀 Agora com as colunas corretas

# Reshape para o formato esperado pelo LSTM
new_test_data = new_test_data.reshape((1, 1, new_test_data.shape[1]))

# Carregar modelo treinado
if not os.path.exists(MODEL_PATH):
    print("❌ Modelo não encontrado! Certifique-se de que o treinamento foi realizado.")
else:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)

    # Fazer previsão
    prediction = model.predict(new_test_data)
    probability = prediction[0][0]

    print(f"🔮 Probabilidade de falha: {probability:.2f}")

    if probability > 0.5:
        print("🔥 Alta chance de falha!")
    else:
        print("✅ Baixa chance de falha. Teste não necessário.")
