import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Carregar modelo treinado
model = tf.keras.models.load_model("../ml_model/test_failure_predictor.h5")

# Simulação: Dados de um novo teste (exemplo: 3 erros recentes, 2.5s de resposta)
new_test_data = np.array([[3, 2.5]])

# Normalizar os dados
scaler = MinMaxScaler()
df = pd.read_csv("../ml_model/test_data.csv")
scaler.fit(df[['error_count', 'response_time']])
new_test_data = scaler.transform(new_test_data)

# Reshape para o formato esperado pelo LSTM
new_test_data = new_test_data.reshape((1, 1, 2))

# Fazer previsão
prediction = model.predict(new_test_data)
probability = prediction[0][0]

print(f"🔮 Probabilidade de falha: {probability:.2f}")

if probability > 0.5:
    print("🔥 Alta chance de falha!")
else:
    print("✅ Baixa chance de falha. Teste não necessário.")
