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

'''
Função que gera um número CPF válido baseado em números
randômicos
'''
def gerar_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]  # Gera os 9 primeiros dígitos do CPF

    # Calcula o primeiro dígito verificador
    soma = 0
    for i, v in enumerate(cpf):
        soma += v * (10 - i)
    resto = soma % 11
    cpf.append(11 - resto if resto > 1 else 0)

    # Calcula o segundo dígito verificador
    soma = 0
    for i, v in enumerate(cpf):
        soma += v * (11 - i)
    resto = soma % 11
    cpf.append(11 - resto if resto > 1 else 0)

    # Formata o CPF com pontos e traços
    cpf_formatado = ''.join(map(str, cpf))
    cpf_formatado = f"{cpf_formatado[:3]}.{cpf_formatado[3:6]}.{cpf_formatado[6:9]}-{cpf_formatado[9:]}"

    return cpf_formatado

try:
    # Registrar o tempo de início
    inicio = time.time()

    # Conectar ao banco de dados
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Abre o arquivo CSV em modo de leitura
    with open('nomes.csv', 'r', newline='', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Lê os dados linha por linha
        for linha in leitor_csv:
            nome = linha[0].split(';')[1]
            cpf = gerar_cpf()
            print(nome, ' ', cpf)
            sql = "INSERT INTO cliente (nome, cpf) VALUES ('" + nome + "', '" + cpf + "')"
            
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