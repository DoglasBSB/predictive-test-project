import requests
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 🔐 Configuração da API do Qase
API_KEY = "5900e4ddd12656cd956bbb63438bf96b9f178d07a7a57dadb50f7f01a0b780aa"
PROJECT_CODE = "CPQ"  # Código do projeto no Qase
QASE_API_URL = f"https://api.qase.io/v1/run/{PROJECT_CODE}"

def get_qase_data():
    """
    Obtém dados reais dos casos de teste cadastrados na ferramenta Qase.
    """
    headers = {"Token": API_KEY, "Content-Type": "application/json"}
    
    try:
        response = requests.get(QASE_API_URL, headers=headers)
        response.raise_for_status()
        result = response.json()

        # 📌 Verifica se a resposta contém dados válidos
        test_cases = result.get("result", {}).get("entities", [])
        if not test_cases:
            print("❗Nenhum dado válido retornado da API do Qase.")
            return []

        cases = []
        for case in test_cases:
            cases.append([
                case.get("error_count", 0),
                case.get("response_time", 0),
                1 if case.get("status") == "failed" else 0  # 1 para falha, 0 para sucesso
            ])

        return cases

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter dados do Qase: {e}")
        return []

def prepare_data():
    """
    Obtém os dados do Qase, processa e prepara para treino e teste.
    """
    raw_data = get_qase_data()
    if not raw_data:
        print("❗Nenhum dado processado. Abortando...")
        return None

    df = pd.DataFrame(raw_data, columns=['error_count', 'response_time', 'test_status'])

    # Separar features (X) e target (y)
    X = df[['error_count', 'response_time']]
    y = df['test_status']

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar os dados
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Salvar o scaler para reutilização
    #os.makedirs("ml_model", exist_ok=True)
    joblib.dump(scaler, "scaler.pkl")

    # Ajustar para o formato LSTM (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    return X_train, X_test, y_train, y_test

def train_lstm():
    """
    Treina um modelo LSTM para previsão de falhas em testes.
    """
    X_train, X_test, y_train, y_test = prepare_data()
    if X_train is None:
        print("❌ Erro: Dados não disponíveis para treino.")
        return

    # Criar modelo LSTM
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=(1, X_train.shape[2])),
        Dropout(0.2),
        LSTM(50, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid')  # Saída binária (0 ou 1)
    ])

    # Compilar o modelo
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Treinar o modelo
    model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

    # Salvar o modelo treinado
    model.save("lstm_model.h5")

    print("✅ Modelo LSTM treinado e salvo com sucesso!")

if __name__ == "__main__":
    train_lstm()
