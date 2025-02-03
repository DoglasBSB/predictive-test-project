import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Simulação de dados históricos de testes
data = {
    'error_count': [1, 2, 0, 3, 5, 1, 0, 4, 2, 3],
    'response_time': [1.2, 1.5, 1.1, 2.3, 3.1, 1.0, 0.9, 2.8, 1.7, 2.0],
    'test_status': [0, 1, 0, 1, 1, 0, 0, 1, 0, 1]  # 0 = sucesso, 1 = falha
}

df = pd.DataFrame(data)

# Normalizar os dados para melhorar o desempenho da LSTM
scaler = MinMaxScaler()
df[['error_count', 'response_time']] = scaler.fit_transform(df[['error_count', 'response_time']])

# Salvar os dados normalizados
df.to_csv("test_data.csv", index=False)

print("✅ Dados preparados!")
