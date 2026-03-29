'''
-- Autor: Rodrigo Santos
-- Linkedin: https://www.linkedin.com/in/rodrigo-santos-22390056/
-- E-mail: rodrigoinfo30@gmail.com
-- Data de criação: 20/12/2025  
-- Descrição: código criado para criar a linha digitável para boletos do banco Bradesco (237)
'''

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

#Informações Itaú banco 341
#informar a conta sem o dígito caso tenha 5 caractéres o número da conta
#informar o dígito do número bancário

#banco = '237'
#print(f"A linha digitável é: {func_cod_barra('237', '9', '26/04/2019', '40.00', '2370', '09', '00030052604', '0029998')}")

#banco = '237'
#print(f"A linha digitável é: {func_cod_barra('237', '9', '21/01/2026', '20000.00', '0096', '09', '01000035722', '00788030')}")

import LinhaDigitavel_237_341 as ln
import BoletoCodBarra as bl

banco = '341'
digitavel_final, digitavel = ln.func_cod_barra('341', '9', '20/05/2026', '15516.74', '7779', '112', '029732214', '05263')

cod_barra = bl.GeraCodBarraBoleto(digitavel)

with open("barcode" + banco + ".html", "w", encoding="utf-8") as f:
    f.write("<html><body>")
    f.write(f"{digitavel_final}<br>")
    f.write(cod_barra)
    f.write("</body></html>")
