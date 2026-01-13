#string de exemplo para encontrar a palavra que ficar depois do ponto e vírgula
#Lambrando que o Python a contagem inicia com zero (0)
string = "rodrigo;teste"

#Pegar posição do carácter ;
posicao = string.index(";")
print("posição é:", posicao)
print()

#Pegando a palavra que ficar depois do ponto ;
ini = int(posicao) + 1
fim = len(string)
resultado = string[ini:fim]

#segunda forma não precisa informar a posição final,
#porque deixando somente ":", já entende que vai pegar o final
resultado2 = string[ini:]

#Palavra no final
print("A palavra é:", resultado)
print("A palavra 2 é:", resultado2)
print()

#Para usar de forma dinâmica, pode seguir esse exemplo
posicao = string.index(";")

ini = int(posicao) + 1
fim = len(string)
resultado = string[ini:fim]
print("Resultado dinamico é: ", resultado)
print()

#Para trabalhar com string entrar a posição inicial e soma com a quantidade de caracteres que você precisa
#exemplo
#A palavra teste inicia na posição 8 e tem 5 caracteres
string = "rodrigo;teste"
posicao = string.index(";")
ini = int(posicao) + 1
fim = ini + len("teste")

resultado = string[8:13]
resultado2 = string[ini:fim]

print("final:", resultado)
print("final 2:", resultado2)
