import psycopg2
import random
import time

# Parâmetros de conexão
dbname = 'desnormalizacao'
user = 'postgres'
password = 'Lipisa99@@'
host = 'localhost'
port = '5432'

id_inicial_produto = 1
id_final_produto = 11967

try:
    # Registrar o tempo de início
    inicio = time.time()

    # Conectar ao banco de dados
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Criar um cursor
    cursor = conn.cursor()

    # Executar uma consulta SQL
    sql = "SELECT c.id, c.nome, e.id AS id_endereco, p.id AS id_pagamento FROM cliente c "
    sql += "LEFT JOIN endereco e ON e.id_cliente = c.id AND e.tipo = 'Residencial' "
    sql += "LEFT JOIN pagamento p ON p.id_cliente = c.id AND p.bandeira = 'Visa' "
    sql += "ORDER BY c.nome ASC"
    cursor.execute(sql)

    # Recuperar os resultados
    resultados = cursor.fetchall()
    
    for linha in resultados:
        id = linha[0]
        nome = linha[1]
        id_endereco = linha[2]
        id_pagamento = linha[3]
        print(nome)
        
        for i in range(3):
            numero_parcelas = random.randint(1, 6)
            sql_pedido = "INSERT INTO pedido (id_cliente, id_pagamento, id_endereco, parcelas) "
            sql_pedido += "VALUES (" + str(id) + ", " + str(id_pagamento) + ", " + str(id_endereco) + ", " + str(numero_parcelas) + ") RETURNING id"

            # Criar um cursor
            cursor_insert = conn.cursor()
            # Executar o INSERT
            cursor_insert.execute(sql_pedido)

            # Recuperar o ID do registro inserido
            id_pedido = cursor_insert.fetchone()[0]
            # print("ID_PEDIDO ", id_pedido)

            for j in range(3): 
                id_produto = random.randint(id_inicial_produto, id_final_produto)
                quantidade = random.randint(1, 10)
                sql_item_pedido = "INSERT INTO item_pedido (id_produto, id_pedido, quantidade, desconto) "
                sql_item_pedido += "VALUES (" + str(id_produto) + ", " + str(id_pedido) + ", " + str(quantidade) + ", 1.5)"
                # Executar o INSERT
                cursor_insert.execute(sql_item_pedido)

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