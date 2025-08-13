import requests
import pandas as pd

class ETLClima:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def extrair(self, cidade):
        url = f"{self.api_url}?q={cidade}&appid={self.api_key}&units=metric&lang=pt_br"
        resposta = requests.get(url)
        dados_json = resposta.json()

        if resposta.status_code == 401:
            print(f"Chave de API inválida ao consultar {cidade}.")
            return None

        return dados_json

    def transformar(self, dados_json):
        if dados_json is None or "name" not in dados_json:
            return None

        dados = {
            "cidade": dados_json.get("name", "Desconhecida"),
            "temperatura": dados_json.get("main", {}).get("temp", None),
            "umidade": dados_json.get("main", {}).get("humidity", None),
            "data_coleta": pd.Timestamp.now()
        }
        return pd.DataFrame([dados])

    def carregar(self, df, database):
        if df is not None and not df.empty:
            database.inserir_dados(df)

    def executar(self, cidade, database):
        dados_json = self.extrair(cidade)
        df = self.transformar(dados_json)
        self.carregar(df, database)
