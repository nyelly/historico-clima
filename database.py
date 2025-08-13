import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=root,
                password=root,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("Conexão com o banco MySQL estabelecida!")
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            self.conn = None
            self.cursor = None

    def inserir_dados(self, df, atualizar=False):
        """
        Insere dados no banco.
        :param df: DataFrame com colunas 'cidade', 'temperatura', 'umidade', 'data_coleta'
        :param atualizar: se True, atualiza os dados se a cidade já existir (mantém apenas último registro)
        """
        if self.conn is None:
            print("⚠ Conexão com o banco não disponível.")
            return

        try:
            if atualizar:
                query = """
                INSERT INTO clima (cidade, temperatura, umidade, data_coleta)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    temperatura = VALUES(temperatura),
                    umidade = VALUES(umidade),
                    data_coleta = VALUES(data_coleta)
                """
            else:
                query = """
                INSERT INTO clima (cidade, temperatura, umidade, data_coleta)
                VALUES (%s, %s, %s, %s)
                """

            for _, row in df.iterrows():
                self.cursor.execute(query, (
                    row["cidade"],
                    row["temperatura"],
                    row["umidade"],
                    row["data_coleta"]
                ))

            self.conn.commit()
            print(f"{len(df)} registros inseridos/atualizados com sucesso!")

        except Error as e:
            print(f"Erro ao inserir/atualizar dados: {e}")

    def buscar_historico(self, cidade, limite=10):
        """Retorna o histórico da cidade (últimos registros)"""
        if self.conn is None:
            print("⚠ Conexão com o banco não disponível.")
            return []

        try:
            query = """
            SELECT cidade, temperatura, umidade, data_coleta
            FROM clima
            WHERE cidade = %s
            ORDER BY data_coleta DESC
            LIMIT %s
            """
            self.cursor.execute(query, (cidade, limite))
            resultados = self.cursor.fetchall()
            return resultados
        except Error as e:
            print(f"Erro ao buscar histórico: {e}")
            return []

    def fechar_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Conexão com o banco encerrada.")
