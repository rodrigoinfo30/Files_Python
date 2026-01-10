'''
-- Autor: Rodrigo Santos
-- Linkedin: https://www.linkedin.com/in/rodrigo-santos-22390056/
-- E-mail: rodrigoinfo30@gmail.com
-- Data de criação: 20/12/2025  
-- Descrição: código criado para criar a linha digitável para boletos do banco Bradesco (237)
'''

#próximo dia útil quando vencimento cair no sábado ou domingo
from datetime import datetime, timedelta

def proximo_dia_util(data_inicial):
    dia_seguinte = data_inicial #+ timedelta(days=1)
    # weekday(): 0=Segunda, 1=Terça, 2=Quarte, 3=Quinta, 4=Sexta, 5=Sábado, 6=Domingo
    while dia_seguinte.weekday() >= 5: # Se for Sábado ou Domingo
        if dia_seguinte.weekday() >= 5:
            dia_seguinte += timedelta(days=1)
        else:
            dia_seguinte
    return dia_seguinte


#gerar o dígito verificador do código de barras seguindo a regra do banco
def func_digitavel_cod_dig(banco= '', digitavel = ''):
    digitavel = digitavel.rjust(43, "0")
    mutiplicaindice = "4329876543298765432987654329876543298765432"
    total = 0
    contador = 1
    while contador <= 43:
        num1 = mutiplicaindice[contador-1:contador]
        num2 = digitavel[contador-1:contador]

        inum1 = int(num1)
        inum2 = int(num2)

        total = total + (inum1 * inum2)
        contador = contador + 1

    resto = total % 11

    resultado = 11 - resto
    if resultado == 0:
        resultado = 1
    elif resultado == 1:
        resultado = 1
    elif resultado > 9:
        resultado = 1
    return resultado

#Calcular o digito Dac dos campos 1, 2 e 3
def func_digitavel_dig(banco = '', digitavel = ''):
    qtd_dig = len(digitavel)
    
    if qtd_dig not in(9, 10, 11, 13, 20):
        return digitavel
    if qtd_dig == 9:
        multiplica = "212121212"
    elif qtd_dig == 10:
        multiplica = "1212121212"
    elif qtd_dig == 11:
        multiplica = "21212121212"
    elif qtd_dig == 13:
        multiplica = "2121212121212"
    elif qtd_dig == 20:
        multiplica = "12121212121212121212"
    else:
        return digitavel

    total_geral = 0

    contador = 1
    
    while contador <= qtd_dig:
        num1 = multiplica[contador-1:contador]
        num2 = digitavel[contador-1:contador]
        
        inum1 = int(num1)
        inum2 = int(num2)

        total = (inum1 * inum2)
        if total <= 9:
            total_geral = total_geral + total
        else:
            stotal = str(total)

            num1 = stotal[0:1]
            num2 = stotal[1:]

            inum1 = int(num1)
            inum2 = int(num2)
            
            total_geral = total_geral + inum1 + inum2
        contador += 1
           
    if banco == "237":                    #Bradesco
        stotal = total_geral
        num1 = str(stotal)[-1]
        inum1 = int(num1)
        if inum1 == 0:
            inum2 = 0
        else:
            inum2 = 10 - inum1
        digitavel += str(inum2)
    elif banco == "341":                    #Itaú
        if qtd_dig == 20 or qtd_dig == 11:
            resto = total_geral % 10
            if resto == 0:
                inum1 = 0
            else:
                inum1 = 10 - resto
            digitavel += str(inum2)
        else:
            stotal = total_geral
            num1 = str(stotal)[-1]
            inum1 = int(num1)
            if inum1 == 0:
                inum2 = 0
            else:
                inum2 = 10 - inum1
            digitavel += str(inum2)        
    else:
        nome = "Banco não cadastrado"

    return digitavel

#Montar a linha digitável
def func_digitavel(banco = '', digitavel = ''):
    barra_dig = ""
    barra_dig1 = ""
    barra_dig2 = ""
    barra_dig3 = ""
    barra_dig4 = ""
    barra_dig5 = ""

    contador = 1
    
    if (banco == "1" or banco == "001"):
        nome = "Brasil"
    elif banco == "237":            #Bradesco
        barra_dig1 = digitavel
        barra_dig1 = digitavel[:4]
        barra_dig1 = barra_dig1 + digitavel[19:24]

        barra_dig2 = digitavel[24:34]

        barra_dig3 = digitavel[34:44]

        barra_dig4 = digitavel[4:5]

        barra_dig5 = digitavel[5:9] + digitavel[9:19]

    elif banco == "341":            #Itaú
        barra_dig1 = digitavel
        barra_dig1 = digitavel[:4]
        barra_dig1 = barra_dig1 + digitavel[19:24]

        barra_dig2 = digitavel[24:34]

        barra_dig3 = digitavel[34:44]

        barra_dig4 = digitavel[4:5]

        barra_dig5 = digitavel[5:9] + digitavel[9:19]        
        
    else:
        barra_dig = "Banco não cadastrado"

    #calcular o dígito das 3 primeiras partes
    barra_dig1 = func_digitavel_dig(banco, barra_dig1)
    barra_dig2 = func_digitavel_dig(banco, barra_dig2)
    barra_dig3 = func_digitavel_dig(banco, barra_dig3)

    #Juntar todas as partes
    barra_dig += barra_dig1[:5] + "." + barra_dig1[5:11] + " "
    barra_dig += barra_dig2[:5] + "." + barra_dig2[5:11] + " "
    barra_dig += barra_dig3[:5] + "." + barra_dig3[5:11] + " "
    barra_dig += barra_dig4 + " "
    barra_dig += barra_dig5
    return barra_dig   

#gerar linha digitável banco(237-Bradesco)
'''
Basta informar as seguintes informações
banco        = código do banco
moeda        = código da moeda
vencimento   = vecimento do boleto
valor        = valor do boleto
agencia      = agência da conta
carteira     = código da carteira, normalmente é 9
nosso_numero = nosso número
conta        = número da conta sem dígito
'''
def func_cod_barra(banco= '', moeda= '', vencimento= '', valor= '', agencia= '', carteira= '', nosso_numero= '', conta= ''):
    cod_barra_final = ''
    #verificar qual o próximo dia últil
    formato_1 = "%d/%m/%Y"
    vencimento_util = datetime.strptime(vencimento, formato_1)
    proximo_dia = proximo_dia_util(vencimento_util)
    proximo_dia = proximo_dia.strftime("%d/%m/%Y")

    fator_vencimento = '07/10/1997'
    fator_vencimento2 = '22/02/2025'

    d1 = datetime.strptime(proximo_dia, "%d/%m/%Y")
    d2 = datetime.strptime(fator_vencimento, "%d/%m/%Y")

    diferenca = abs((d2 - d1).days)
    #Boletos com vencimento apartir de 22/02/2025 tem que fazer a diferença de 9000 para o fator
    if diferenca > 10000:
        diferenca = diferenca -9000
    else:
        diferenca

    svalor = str(valor)
    svalor = svalor.replace(".", "")
    svalor = svalor.rjust(10, "0")
    diferenca = str(diferenca).rjust(4, "0")

    if banco == "237":                    #Bradesco
        carteira = carteira.rjust(2, "0")
        agencia = agencia.rjust(4, "0")
        #agencia = agencia.rjust(3, "0")
        nosso_numero = nosso_numero.rjust(11, "0")
        conta = conta.rjust(7, "0")
        
        cod_barra_final = banco
        cod_barra_final += moeda
        cod_barra_final += str(diferenca)
        cod_barra_final += svalor
        cod_barra_final += agencia
        cod_barra_final += carteira
        cod_barra_final += nosso_numero
        cod_barra_final += conta
        cod_barra_final += "0"

    elif banco == "341":
        ndig = nosso_numero[-1]
        nosso_numero = nosso_numero[:8]
        banco = banco.rjust(3, "0")
        carteira = carteira.rjust(3, "0")
        agencia = agencia.rjust(4, "0")
        nosso_numero = nosso_numero.rjust(8, "0")
        conta = conta.rjust(5, "0")
        
        conteudo = carteira + nosso_numero
        dac_agen = func_digitavel_dig(banco, conteudo)

        conteudo = agencia + "00" + conta
        dac_conta = func_digitavel_dig(banco, conteudo)         
        
        cod_barra_final = banco
        cod_barra_final += moeda
        cod_barra_final += str(diferenca)
        cod_barra_final += svalor        
        cod_barra_final += carteira
        cod_barra_final += nosso_numero
        cod_barra_final += ndig
        cod_barra_final += agencia
        cod_barra_final += conta
        cod_barra_final += dac_conta[-1]
        cod_barra_final += "000"        
    
    else:
        nome = "Banco não cadastrado"
    #Calcular o dígito verificador do código de barras
    digito = func_digitavel_cod_dig(banco, cod_barra_final)

    #Montar o código de barra com o dígito verificador
    cod_barra_final = cod_barra_final[:4] + str(digito) + cod_barra_final[4:44]

    #Montar a linha dígitável
    cod_barra_final = func_digitavel(banco, cod_barra_final)
    return cod_barra_final

#print(f"A linha digitável é: {func_cod_barra('237', '9', '26/04/2019', '40.00', '2370', '09', '00030052604', '0029998')}")
#print(f"A linha digitável é: {func_cod_barra('237', '9', '21/01/2026', '20000.00', '0096', '09', '01000035722', '00788030')}")

#Informações Itaú banco 341
#informar a conta sem o dígito caso tenha 5 caractéres o número da conta
#informar o dígito do número bancário
print(f"A linha digitável é: {func_cod_barra('341', '9', '20/05/2026', '15516.74', '7779', '112', '029732214', '05263')}") #itaú

