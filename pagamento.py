import psycopg2
import random
import time

# Parâmetros de conexão
dbname = 'desnormalizacao'
user = 'postgres'
password = 'Lipisa99@@'
host = 'localhost'
port = '5432'

# Função para gerar um número inteiro de 16 dígitos
def gerar_numero_inteiro_16_digitos():
    # O primeiro dígito não pode ser zero para garantir que o número tenha 16 dígitos
    primeiro_digito = random.randint(1, 9)
    
    # Gerar os 15 dígitos restantes
    outros_digitos = [random.randint(0, 9) for _ in range(15)]
    
    # Juntar todos os dígitos em uma única string
    numero_string = ''.join(map(str, [primeiro_digito] + outros_digitos))
    
    # Converter a string para um número inteiro
    numero_inteiro = int(numero_string)
    
    return numero_inteiro

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

    cep_inicial = 13330001
    cep = cep_inicial
    
    for linha in resultados:
        id = linha[0]
        nome = linha[1]
        numero_cartao = gerar_numero_inteiro_16_digitos()

        print(nome)

        sql_pagamento_1 = "INSERT INTO pagamento (numero_cartao, bandeira, validade, cvv, id_cliente) "
        sql_pagamento_1 += "VALUES ('" + str(numero_cartao) + "', 'Visa', '2025-01-10', 531, " + str(id) + ")"
        
        numero_cartao = gerar_numero_inteiro_16_digitos()
        sql_pagamento_2 = "INSERT INTO pagamento (numero_cartao, bandeira, validade, cvv, id_cliente) "
        sql_pagamento_2 += "VALUES ('" + str(numero_cartao) + "', 'Mastercard', '2023-06-08', 321, " + str(id) + ")"

        numero_cartao = gerar_numero_inteiro_16_digitos()
        sql_pagamento_3 = "INSERT INTO pagamento (numero_cartao, bandeira, validade, cvv, id_cliente) "
        sql_pagamento_3 += "VALUES ('" + str(numero_cartao) + "', 'Elo', '2026-04-15', 554, " + str(id) + ")"

        # Criar um cursor
        cursor_insert = conn.cursor()
        # Executar o INSERT
        cursor_insert.execute(sql_pagamento_1)
        cursor_insert.execute(sql_pagamento_2)
        cursor_insert.execute(sql_pagamento_3)
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
