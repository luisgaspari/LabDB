import psycopg2
from datetime import datetime
import time

# Parâmetros de conexão
dbname = 'desnormalizacao'
user = 'postgres'
password = 'Lipisa99@@'
host = 'localhost'
port = '5432'

numero_pedido = 303283

'''
Função que completa com espaços vazios uma string, de acordo
com a quantidade desejada
'''
def completar_com_espacos(texto, comprimento_desejado):
    # Calcula o número de espaços necessários para atingir o comprimento desejado
    espacos_necessarios = max(0, comprimento_desejado - len(texto))
    
    # Retorna o texto original concatenado com espaços adicionais
    return texto + ' ' * espacos_necessarios

try:
    # Registrar o tempo de início
    inicio = time.time()

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
    sql += "WHERE p.id = " + str(numero_pedido)

    cursor.execute(sql)

    # Recuperar os resultados
    resultados = cursor.fetchall()
    
    for linha in resultados:
        id_pedido = linha[0]
        data_hora = linha[1]
        # Formatar a data como uma string no padrão brasileiro
        data_formatada = data_hora.strftime('%d/%m/%Y %H:%M:%S')

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

        sql_itens = "SELECT p.id, p.descricao, p.preco_unitario, ip.quantidade, ip.desconto "
        sql_itens += "FROM item_pedido ip "
        sql_itens += "INNER JOIN produto p ON p.id = ip.id_produto "
        sql_itens += "WHERE ip.id_pedido = " + str(id_pedido)

        # Criar um cursor
        cursor_itens = conn.cursor()
        cursor_itens.execute(sql_itens)
        # Recuperar os resultados
        resultados_itens = cursor_itens.fetchall()

        print("--------------------- INFORMACOES -----------------------")
        print("PEDIDO: ", id_pedido)
        print("DATA: ", data_formatada)
        print("CLIENTE: ", cliente_nome)
        print("CPF: ", cliente_cpf)
        print("---------------------------------------------------------")

        print("------------------------ ITENS --------------------------")
        print("ID \t|Descrição \t\t\t\t|Preço unitário \t|Quantidade \t|Desconto \t|Subtotal")
        for linha_item in resultados_itens:
            produto_id = linha_item[0]
            produto_descricao = completar_com_espacos(linha_item[1], 35)
            produto_preco_unitario = linha_item[2]
            produto_quantidade = linha_item[3]
            produto_desconto = linha_item[4]

            print(produto_id, "\t|", end='')
            print(produto_descricao, "\t|", end='')
            print(produto_preco_unitario, "\t\t\t|", end='')
            print(produto_quantidade, "\t\t|", end='')
            print(produto_desconto, "\t\t|", end='')
            print(round(((produto_preco_unitario * produto_quantidade) - produto_desconto), 2))
            
        print("---------------------------------------------------------")

        print("---------------------- ENDERECO -------------------------")
        print("LOGRADOURO: ", endereco_logradouro)
        print("NUMERO: ", endereco_numero)
        print("BAIRRO: ", endereco_bairro)
        print("CIDADE: ", endereco_cidade)
        print("ESTADO: ", endereco_estado)
        print("---------------------------------------------------------")

        print("--------------------- PAGAMENTO -------------------------")
        print("NUMERO DO CARTÃO: ", pagamento_numero_cartao)
        print("BANDEIRA: ", pagamento_bandeira)
        print("PARCELAS: ", parcelas)
        print("---------------------------------------------------------\n\n\n")

        cursor_itens.close()

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
