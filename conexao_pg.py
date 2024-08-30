import psycopg2
print("Importou a biblioteca!")

# Parâmetros da conexao
dbmane = 'desnormalizacao'
user = 'postgres'
password = 'Lipisa99@@'
host = 'localhost'
port = '5432'

try: 
    # Conectando ao banco de dados
    con = psycopg2.connect(dbname=dbmane, user=user, password=password, host=host, port=port)
    print("Conectou ao banco de dados")
    # Criar um cursor
    cursor = con.cursor()
    # Query que lista os produtos
    sql = "SELECT p.id, p.descricao, p.preco_unitario FROM produto p LIMIT 1"
    # Executar o SELECT
    cursor.execute(sql)
    # Recuperar os resultados
    resultados = cursor.fetchall()
    # Exibir os resultados
    for linha in resultados:
        print(linha)
except Exception as e:
    print("Ocorreu um erro: ", e)
    print("Não foi possível conectar ao banco de dados")