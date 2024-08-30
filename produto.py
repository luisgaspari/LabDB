import psycopg2
import random
import csv
import time

# Parâmetros de conexão
dbname = 'desnormalizacao'
user = 'postgres'
password = 'Lipisa99@@'
host = 'localhost'
port = '5432'

try:
    # Registrar o tempo de início
    inicio = time.time()

    # Conectar ao banco de dados
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Abre o arquivo CSV em modo de leitura
    with open('livros.csv', 'r', newline='', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Lê os dados linha por linha
        for linha in leitor_csv:
            titulo = linha[0].split(';')[0]
            titulo = titulo.replace("'", "")
            valor = round(random.uniform(0, 100), 2)
            print(titulo, ' ', valor)
            sql = "INSERT INTO produto (descricao, preco_unitario) VALUES ('" + titulo + "', '" + str(valor) + "')"
            
            # Criar um cursor
            cursor = conn.cursor()
            # Executar o INSERT
            cursor.execute(sql)
            # Commit da transação
            conn.commit()

    conn.close()

    # Registrar o tempo de término
    fim = time.time()
    # Calcular o tempo decorrido
    tempo_decorrido = fim - inicio
    print("Tempo decorrido:", tempo_decorrido, "segundos")
except Exception as e:
    print("Ocorreu um erro:", e)