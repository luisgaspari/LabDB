import pymongo

print("Biblioteca pymongo importada com sucesso!")

# Parâmetros de conexão
conexao_uri = "mongodb://localhost:27017/"
nome_banco_dados = "blog"

try:
    # Conectar ao MongoBD
    conexao_mongo = pymongo.MongoClient(conexao_uri)
    # Selecionar o banco de dados e a coleção
    banco_dados_mongo = conexao_mongo[nome_banco_dados]
    # Selecionar a coleção
    colecao = banco_dados_mongo["post"]
    # Realizando a consulta
    # resultado = colecao.find({"titulo": "Segundo Post"})
    resultado = colecao.find()
    # iterando sobre o resultado
    for documento in resultado:
        print(documento)
except Exception as e:
    print("Erro ao acessar o banco de dados: ", e)
