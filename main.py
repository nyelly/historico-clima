import schedule
import time
from etl import ETLClima
from database import MySQLDatabase
from datetime import datetime

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "9990c81e5c84b63299f7503255f90592"
CIDADES = ["Natal", "São Paulo", "Rio de Janeiro"]

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "projeto_dados"
}

def job():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{agora}] 🔄 Iniciando coleta das cidades...")
    
    database = MySQLDatabase(**db_config)
    etl = ETLClima(API_URL, API_KEY)
    
    for cidade in CIDADES:
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌤 Coletando dados de {cidade}...")
            etl.executar(cidade, database)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Dados de {cidade} inseridos/atualizados com sucesso.")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erro ao processar {cidade}: {e}")
    
    database.fechar_conexao()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔚 Coleta finalizada.\n")

if __name__ == "__main__":
    job()
    
    schedule.every(1).minutes.do(job)
    
    print("🕒 Agendador iniciado. Pressione Ctrl+C para parar.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
