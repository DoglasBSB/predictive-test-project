import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

# 🔐 Chave de API do Qase (Substitua pela sua)
API_KEY = "5900e4ddd12656cd956bbb63438bf96b9f178d07a7a57dadb50f7f01a0b780aa"
PROJECT_CODE = "CPQ"  # Código do projeto no Qase
QASE_API_URL = f"https://api.qase.io/v1/run/{PROJECT_CODE}"


def get_qase_data():
    """
    Obtém dados reais dos casos de teste cadastrados na ferramenta Qase.
    Retorna uma lista de execuções de testes.
    """
    headers = {"Token": API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.get(QASE_API_URL, headers=headers)
        response.raise_for_status()

        # Verificar toda a resposta da API
        data = response.json()
        print("🔍 Resposta completa da API:", data)  # Debug

        return data.get('result', {}).get('entities', [])  # Acessa corretamente os runs

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao obter dados do Qase: {e}")
        return []


def process_data(raw_data):
    """
    Processa os dados brutos obtidos da API do Qase para extrair as informações relevantes.
    Retorna um DataFrame do Pandas com os dados formatados.
    """
    processed_data = []

    for run in raw_data:
        total_tests = run['stats'].get('total', 0)  # Total de testes no run
        failed_tests = run['stats'].get('failed', 0)  # Testes falhos
        passed_tests = run['stats'].get('passed', 0)  # Testes passados
        response_time = run.get('time_spent', 0) / 1000  # Tempo gasto no run em segundos

        # Verificação para evitar divisões por zero
        if total_tests == 0:
            continue

        # Define erro como a porcentagem de testes falhos
        error_rate = failed_tests / total_tests

        # Se houver falha, marca como 1 (problema identificado), senão 0 (sem falhas)
        test_status = 1 if failed_tests > 0 else 0

        processed_data.append([total_tests, failed_tests, passed_tests, response_time, error_rate, test_status])

    # Se nenhum dado foi processado, aborta
    if not processed_data:
        print("⚠️ Nenhum dado processado. Abortando...")
        return None

    # Convertendo para um DataFrame
    df = pd.DataFrame(processed_data, columns=['total_tests', 'failed_tests', 'passed_tests', 'response_time', 'error_rate', 'test_status'])

    print(f"📊 Dados processados:\n{df}")  # Depuração: visualizar os dados extraídos
    return df


def prepare_data():
    """
    Obtém os dados do Qase, processa e prepara para treino e teste.
    """
    raw_data = get_qase_data()

    if not raw_data:
        print("⚠️ Nenhum dado processado. Abortando...")
        return None

    df = process_data(raw_data)

    if df is None or len(df) < 2:  # Verifica se há dados suficientes
        print("⚠️ Dados insuficientes para treinar o modelo! Precisamos de pelo menos 2 amostras.")
        return None

    # Separar features (X) e target (y)
    X = df[['failed_tests', 'response_time', 'error_rate']]  # Correção das colunas
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

    # Ajustar para o formato LSTM (se for necessário no futuro)
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    # Salvar os dados para treinamento
    pd.DataFrame(X_train.reshape(X_train.shape[0], -1)).to_csv("X_train.csv", index=False)
    pd.DataFrame(y_train).to_csv("y_train.csv", index=False)
    pd.DataFrame(X_test.reshape(X_test.shape[0], -1)).to_csv("X_test.csv", index=False)
    pd.DataFrame(y_test).to_csv("y_test.csv", index=False)

    # Para salvar `test_data.csv` que será consumido pelo arquivo predict_test_failure.py**
    df[['failed_tests', 'response_time', 'error_rate']].to_csv("test_data.csv", index=False)


    print("✅ Dados preparados e salvos com sucesso!")
    print("📊 Estatísticas dos dados:")
    print(df.describe())

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    prepare_data()
