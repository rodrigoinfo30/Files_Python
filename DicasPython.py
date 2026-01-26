#Dica de como ler um arquivo .csv e degar cada campo de forma dinâmica
 
#modelo de arquivo
with open("C:/Users/Rodrigo Santos/Documents/Python/arquivo_csv.csv", "w") as arquivo_cvs:
    arquivo_cvs.write("nome;rg;cpf;endereco;celular;telefone;empresa\n")
    arquivo_cvs.write("rodrigo;112223334;55566677788;rua teste 123;119222223333;1122334455;Teste LTDA\n")
    arquivo_cvs.write("Joao;444444444;55555555555;rua sem número 456;11988888888;1166667777;Infor Teste LTDA\n")

with open('C:/Users/Rodrigo Santos/Documents/Python/arquivo_csv.csv', 'r') as file:
    #contador para linhas do arquivo
    linhas = 1
    for line in file:
        #verificar quando ; tem na linha
        contador = line.count(';')
        #Pegando somente as informações da segunda linha em diante
        if linhas >= 2:
            values_insert = ""
            #for para saber quantas informações estão separadas por ;
            for i in range(contador):
                #pegar a posição final que contem ;
                final = line.index(";")
                #pegar a informação e armazenar em uma variável para fazer um insert por exemplo
                informacao = line[:final]
                #informações para o insert por exemplo
                if i <= 4:
                    values_insert += (informacao + ",")
                else:
                    values_insert += informacao
                #mostrando a informação
                print(f"informacao {i}", informacao)
                #retirando a primeira informação da linhas para pegar as próximas
                line = line[(final + 1):]
            #Informação completa para o insert
            print("values_insert", values_insert)
        linhas = linhas + 1

print()
print("------uso de variável global------")        
print()
#uso de variável global
from datetime import datetime

def cadastro():
    global gIdade #variável global
    nome = input('Entre com o seu nome: ')
    dt_nascimento = input('Digite sua data de nascimento: ')
    prof = input('Qual sua profissão? ')

    data_atual = datetime.now()
    formato_1 = "%d/%m/%Y"
    data_em_texto = data_atual.strftime(formato_1)
    dt_nascimento = datetime.strptime(dt_nascimento, formato_1)
    data_em_texto = datetime.strptime(data_em_texto, formato_1)
    diferenca = abs((dt_nascimento - data_em_texto).days)

    idade = int((diferenca / 365))
    gIdade = idade

    if idade < 18:
        msg = "Sua idade não permite a criação de uma habilitação para dirigir!"
        return msg
    else:
        return {"nome": nome, "nascimento": dt_nascimento, "profissao": prof}

# Dicionário para armazenar os cadastros
cadastros = {}

# Contador para indexar os cadastros
contador = 1

print('Vamos renovas sua habilitação ou fazer uma nova!')
# Loop para permitir múltiplos cadastros
while True:
    novo_cadastro = cadastro() # Chama a função de cadastro   
    if gIdade < 18:
        print(novo_cadastro)
    else:
        # Adiciona o novo cadastro no dicionário com um identificador
        cadastros[contador] = novo_cadastro
        contador += 1
    # Pergunta se o usuário deseja fazer outro cadastro
    resposta = input("\nDeseja fazer outro cadastro? (s/n): ").uper()
    # Verifica se o usuário deseja sair
    if resposta != 'S':
        break

#mostra o cadastro se tiver informação no dicionário
if cadastros:
    # Imprimir os cadastros de forma organizada
    print("\nObrigado pelas informações!")
    print("Aqui estão os cadastros realizados:")    
    for idx, dados in cadastros.items():
        print(f"\nCadastro {idx}:")
        print(f"Nome: {dados['nome']}")
        print(f"Endereço: {dados['nascimento']}")
        print(f"Profissão: {dados['profissao']}")

        
