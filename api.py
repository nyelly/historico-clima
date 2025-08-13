from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "9990c81e5c84b63299f7503255f90592"

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "projeto_dados"
}

def salvar_clima_no_banco(cidade, temperatura, umidade):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO clima (cidade, temperatura, umidade, data_coleta)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (cidade, temperatura, umidade, datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Erro ao inserir no banco: {e}")

def get_clima_api(cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade},BR&appid={API_KEY}&units=metric&lang=pt_br"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperatura = data["main"]["temp"]
            umidade = data["main"]["humidity"]
            return {
                "cidade": cidade,
                "temperatura": temperatura,
                "umidade": umidade,
                "data_coleta": datetime.now().isoformat()
            }
        else:
            return None
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clima', methods=['GET'])
def clima():
    cidade = request.args.get('cidade')
    if not cidade:
        return jsonify({"error": "Parâmetro 'cidade' é obrigatório."}), 400

    dados_api = get_clima_api(cidade)
    if dados_api:
        salvar_clima_no_banco(cidade, dados_api["temperatura"], dados_api["umidade"])
        dados_api["data_coleta"] = datetime.now().isoformat()
        return jsonify(dados_api)
    else:
        return jsonify({"error": "Cidade não encontrada na API."}), 404

@app.route('/historico', methods=['GET'])
def historico():
    cidade = request.args.get('cidade')
    if not cidade:
        return jsonify({"error": "Parâmetro 'cidade' é obrigatório."}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT cidade, temperatura, umidade, data_coleta
        FROM clima
        WHERE cidade = %s
        ORDER BY data_coleta DESC
        """
        cursor.execute(query, (cidade,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        for r in resultados:
            r["data_coleta"] = r["data_coleta"].isoformat()

        return jsonify(resultados)
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
