import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split

# Carregar os dados
df = pd.read_csv("test_data.csv")

# Separar recursos (X) e rótulo (y)
X = df[['error_count', 'response_time']].values
y = df['test_status'].values

# Reshape para o formato que o LSTM espera (samples, timesteps, features)
X = X.reshape((X.shape[0], 1, X.shape[1]))

# Dividir dados para treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar modelo LSTM
model = Sequential([
    LSTM(50, activation='relu', return_sequences=True, input_shape=(1, 2)),
    LSTM(50, activation='relu'),
    Dense(1, activation='sigmoid')  # Saída binária (0 = sucesso, 1 = falha)
])

# Compilar o modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Treinar modelo
model.fit(X_train, y_train, epochs=50, batch_size=1, verbose=1)

# Salvar modelo treinado
model.save("test_failure_predictor.h5")

print("✅ Modelo LSTM treinado e salvo!")
