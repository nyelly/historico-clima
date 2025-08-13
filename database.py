import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def inserir_dados(self, df):
        query = """
        INSERT INTO clima (cidade, temperatura, umidade, data_coleta)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            temperatura = VALUES(temperatura),
            umidade = VALUES(umidade),
            data_coleta = VALUES(data_coleta)
        """
        for _, row in df.iterrows():
            self.cursor.execute(query, (
                row["cidade"],
                row["temperatura"],
                row["umidade"],
                row["data_coleta"]
            ))
        self.conn.commit()
        print("Dados inseridos/atualizados no banco!")

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()
