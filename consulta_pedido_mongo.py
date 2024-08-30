import pymongo
import time

# Parâmetros de conexão
conexao_uri = "mongodb://localhost:27017/"
nome_banco_dados = "desnormalizacao"

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

    # Conectar ao MongoDB
    conexao_mongo = pymongo.MongoClient(conexao_uri)
    # Selecionar o banco de dados e a coleção
    banco_dado_mongo = conexao_mongo[nome_banco_dados]
    # Selecionar a coleção
    colecao = banco_dado_mongo["pedido"]

    # Consultando o documento na coleção
    resultado = colecao.find({"_id": numero_pedido})
    # Iterar sobre os resultados
    for documento in resultado:
        # print(documento)
        print("--------------------- INFORMACOES -----------------------")
        print("PEDIDO: ", documento["_id"])
        print("DATA: ", documento["data"].strftime('%d/%m/%Y %H:%M:%S'))
        print("CLIENTE: ", documento["cliente_nome"])
        print("CPF: ", documento["cliente_cpf"])
        print("---------------------------------------------------------")

        print("------------------------ ITENS --------------------------")
        print("ID \t|Descrição \t\t\t\t|Preço unitário \t|Quantidade \t|Desconto \t|Subtotal")
        for linha_item in documento["itens"]:
            produto_id = linha_item["codigo"]
            produto_descricao = completar_com_espacos(linha_item["descricao"], 35)
            produto_preco_unitario = linha_item["preco_unitario"]
            produto_quantidade = linha_item["quantidade"]
            produto_desconto = linha_item["desconto"]
            subtotal = linha_item["subtotal"]

            print(produto_id, "\t|", end='')
            print(produto_descricao, "\t|", end='')
            print(produto_preco_unitario, "\t\t\t|", end='')
            print(produto_quantidade, "\t\t|", end='')
            print(produto_desconto, "\t\t|", end='')
            print(subtotal)
            
        print("---------------------------------------------------------")

        print("---------------------- ENDERECO -------------------------")
        print("LOGRADOURO: ", documento["endereco"]["logradouro"])
        print("NUMERO: ", documento["endereco"]["numero"])
        print("BAIRRO: ", documento["endereco"]["bairro"])
        print("CIDADE: ", documento["endereco"]["cidade"])
        print("ESTADO: ", documento["endereco"]["estado"])
        print("---------------------------------------------------------")

        print("--------------------- PAGAMENTO -------------------------")
        print("NUMERO DO CARTÃO: ", documento["pagamento"]["numero_cartao"])
        print("BANDEIRA: ", documento["pagamento"]["bandeira_cartao"])
        print("PARCELAS: ", documento["pagamento"]["parcelas"])
        print("---------------------------------------------------------\n\n\n")

    # Registrar o tempo de término
    fim = time.time()
    # Calcular o tempo decorrido
    tempo_decorrido = fim - inicio
    print("Tempo decorrido:", tempo_decorrido, "segundos")
except Exception as e:
    print("Ocorreu um erro:", e)