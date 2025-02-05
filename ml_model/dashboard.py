import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Verificar se o ambiente permite Streamlit
try:
    import streamlit as st
except ModuleNotFoundError:
    print("O pacote 'streamlit' não está disponível neste ambiente. Execute localmente com 'pip install streamlit'.")
    exit()

# Carregar dados simulados de falhas
data = {
    'timestamp': pd.date_range(start='2025-01-01', periods=10, freq='D'),
    'error_count': [5, 8, 3, 10, 7, 2, 9, 4, 6, 11],
    'error_type': ['frontend', 'backend', 'API', 'database', 'frontend', 'backend', 'API', 'database', 'frontend', 'backend'],
    'predict_test_failure': [4, 7, 3, 9, 6, 2, 8, 3, 5, 10]
}
df = pd.DataFrame(data)

# Taxa de acerto do modelo
accuracy = np.mean(df['predict_test_failure'] / df['error_count']) * 100

# Tempo médio até a falha (simulado)
time_to_fail = np.random.randint(5, 60, size=len(df))
df['time_to_fail'] = time_to_fail
mean_time_to_fail = np.mean(time_to_fail)

st.title("Dashboard de Testes Preditivos")

# Taxa de acerto do modelo
st.subheader("Taxa de Acerto do Modelo")
st.metric(label="Precisão", value=f"{accuracy:.2f}%")

# Comparação Falhas Previstas vs. Ocorridas
st.subheader("Falhas Previstas vs. Ocorridas")
st.line_chart(df[['error_count', 'predict_test_failure']])

# Gráfico de falhas ao longo do tempo
st.subheader("Falhas por Período")
fig, ax = plt.subplots()
ax.plot(df['timestamp'], df['error_count'], marker='o', linestyle='-', label='Ocorridas')
ax.plot(df['timestamp'], df['predict_test_failure'], marker='s', linestyle='--', label='Previstas')
ax.set_xlabel("Data")
ax.set_ylabel("Quantidade de Falhas")
ax.legend()
st.pyplot(fig)

# Tempo médio até a falha
st.subheader("Tempo Médio até a Falha")
st.metric(label="Média (minutos)", value=f"{mean_time_to_fail:.2f}")

# Tabela com as falhas recentes
st.subheader("Últimas Falhas Registradas")
st.write(df[['timestamp', 'error_count', 'error_type', 'predict_test_failure']].tail(5))

# Distribuição dos erros
st.subheader("Distribuição dos Tipos de Erro")
error_counts = df['error_type'].value_counts()
st.bar_chart(error_counts)

# Tendência de Falhas ao Longo do Tempo
st.subheader("Tendência de Falhas")
st.line_chart(df.set_index('timestamp')['error_count'])

# Impacto dos Testes Automatizados (simulado)
before_tests = 50  # Bugs antes da automação
after_tests = np.mean(df['error_count'])  # Média de bugs após automação
reduction = ((before_tests - after_tests) / before_tests) * 100

st.subheader("Impacto dos Testes Automatizados")
st.metric(label="Redução de Bugs em Produção", value=f"{reduction:.2f}%")
