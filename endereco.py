import psycopg2
import random
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

    # Criar um cursor
    cursor = conn.cursor()

    # Executar uma consulta SQL
    cursor.execute("SELECT c.id, c.nome FROM cliente c ORDER BY c.nome ASC")

    # Recuperar os resultados
    resultados = cursor.fetchall()
    
    for linha in resultados:
        id = linha[0]
        nome = linha[1]
        numero = random.randint(1, 3000)

        print(nome)

        sql_endereco_1 = "INSERT INTO endereco (logradouro, numero, bairro, cidade, estado, tipo, id_cliente) "
        sql_endereco_1 += "VALUES ('Rua Luiz Romanelli', '" + str(numero) + "', 'Jardim Primavera', 'Piracicaba', 'SP', 'Residencial', " + str(id) + ")"
        
        numero = random.randint(1, 3000)
        sql_endereco_2 = "INSERT INTO endereco (logradouro, numero, bairro, cidade, estado, tipo, id_cliente) "
        sql_endereco_2 += "VALUES ('Rua Sargento Fábio Pavani', '" + str(numero) + "', 'Vila Monte Alegre', 'Pedreira', 'SP', 'Comercial', " + str(id) + ")"

        # Criar um cursor
        cursor_insert = conn.cursor()
        # Executar o INSERT
        cursor_insert.execute(sql_endereco_1)
        cursor_insert.execute(sql_endereco_2)
        # Commit da transação
        conn.commit()
        cursor_insert.close()

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

    # Registrar o tempo de término
    fim = time.time()
    # Calcular o tempo decorrido
    tempo_decorrido = fim - inicio
    print("Tempo decorrido:", tempo_decorrido, "segundos")
except Exception as e:
    print("Ocorreu um erro:", e)
