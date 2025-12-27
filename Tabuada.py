'''
-- Autor: Rodrigo Santos
-- Linkedin: https://www.linkedin.com/in/rodrigo-santos-22390056/
-- E-mail: rodrigoinfo30@gmail.com
-- Data de criação: 27/12/2025  
'''
#Tabuada do 1 até o 10
contador = 1
while contador <= 10:
    contador2 = 1
    print("-" * 30)
    print("Tabuada do: ", contador)
    #print()
    while contador2 <= 10:        
        print(contador, " x ", contador2, " = ", (contador * contador2))
        contador2 += 1
    print("-" * 30)
    print()
    contador += 1
