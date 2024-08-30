import psycopg2
import json
import pymongo
import csv
import random
import time

# Parâmetros de conexão
conexao_uri = "mongodb://localhost:27017/"
nome_banco_dados = "desnormalizacao"

# Parâmetros de conexão
dbname = 'desnormalizacao'
user = 'postgres'
password = 'Lipisa99@@'
host = 'localhost'
port = '5432'

contador = 1

try:
    # Registrar o tempo de início
    inicio = time.time()

    livros = []
    print("Carregando em memoria os produtos")
    contador_item = 1
    # Abre o arquivo CSV em modo de leitura
    with open('livros.csv', 'r', newline='', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Lê os dados linha por linha
        for linha in leitor_csv:
            titulo = linha[0].split(';')[0]
            titulo = titulo.replace("'", "")
            valor = round(random.uniform(0, 100), 2)
            
            livros.append({"titulo": titulo, "valor": valor, "id": contador_item})
            contador_item += 1
    
    print("Produtos carregados em memoria")

    # Conectar ao MongoDB
    conexao_mongo = pymongo.MongoClient(conexao_uri)
    # Selecionar o banco de dados e a coleção
    banco_dado_mongo = conexao_mongo[nome_banco_dados]
    # Selecionar a coleção
    colecao = banco_dado_mongo["pedido"]

    # Conectar ao banco de dados
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Criar um cursor
    cursor = conn.cursor()

    # Executar uma consulta SQL
    sql = "SELECT p.id, p.data_hora, p.parcelas, "
    sql += "c.nome, c.cpf, "
    sql += "e.logradouro, e.numero, e.bairro, e.cidade, e.estado, e.tipo, "
    sql += "pg.numero_cartao, pg.bandeira "
    sql += "FROM pedido p "
    sql += "INNER JOIN cliente c ON p.id_cliente = c.id "
    sql += "INNER JOIN endereco e ON p.id_endereco = e.id "
    sql += "INNER JOIN pagamento pg ON p.id_pagamento = pg.id "

    cursor.execute(sql)

    # Recuperar os resultados
    resultados = cursor.fetchall()
    
    for linha in resultados:
        id_pedido = linha[0]
        data_hora = linha[1]
        parcelas = linha[2]
        cliente_nome = linha[3]
        cliente_cpf = linha[4]
        endereco_logradouro = linha[5]
        endereco_numero = linha[6]
        endereco_bairro = linha[7]
        endereco_cidade = linha[8]
        endereco_estado = linha[9]
        endereco_tipo = linha[10]
        pagamento_numero_cartao = linha[11]
        pagamento_bandeira = linha[12]

        itens = []
        
        for i in range(3):
            posicao = random.randint(0, len(livros) -1)
            quantidade = random.randint(1, 10)
            livro = livros[posicao]
            # Adicionar um novo item à lista
            item = {
                "codigo": livro["id"],
                "descricao": livro["titulo"],
                "preco_unitario": livro["valor"],
                "quantidade": quantidade,
                "desconto": 1.5,
                "subtotal": round(((livro["valor"] * quantidade) - 1.5), 2)
            }
            itens.append(item)

        pedido = {
            "_id": id_pedido,
            "data": data_hora,
            "cliente_nome": cliente_nome,
            "cliente_cpf": cliente_cpf,
            "endereco": {
                "logradouro": endereco_logradouro,
                "numero": endereco_numero,
                "bairro": endereco_bairro,
                "cidade": endereco_cidade,
                "estado": endereco_estado
            },
            "pagamento": {
                "numero_cartao": pagamento_numero_cartao,
                "bandeira_cartao": pagamento_bandeira,
                "parcelas": parcelas
            },
            "itens": itens
        }

        # Inserir o documento na coleção
        resultado = colecao.insert_one(pedido)
        print("CONTADOR: ", contador)
        contador += 1

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
