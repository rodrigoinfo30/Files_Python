#recebe a linhda digitável e o nome da pasta onde estão as barras
def GeraCodBarraBoleto (valor, images_folder="images"):
    fino = 1
    largo = 4
    altura = 55

    # Inicializa a lista de códigos
    barcodes = [""] * 100
    barcodes[0] = "00110"
    barcodes[1] = "10001"
    barcodes[2] = "01001"
    barcodes[3] = "11000"
    barcodes[4] = "00101"
    barcodes[5] = "10100"
    barcodes[6] = "01100"
    barcodes[7] = "00011"
    barcodes[8] = "10010"
    barcodes[9] = "01010"

    # Geração dos códigos combinados
    for f1 in range(9, -1, -1):
        for f2 in range(9, -1, -1):
            f = f1 * 10 + f2
            texto = ""
            for i in range(5):
                texto += barcodes[f1][i:i+1] + barcodes[f2][i:i+1]
            barcodes[f] = texto

    # Ajusta o valor para ter comprimento par
    texto = valor
    if len(texto) % 2 != 0:
        texto = "0" + texto

    # StringBuilder equivalente
    codbarras = []

    # Guarda inicial
    codbarras.append(f'<img src="{images_folder}/p.gif" width="{fino}" height="{altura}" border=0>')
    codbarras.append(f'<img src="{images_folder}/b.gif" width="{fino}" height="{altura}" border=0>')
    codbarras.append(f'<img src="{images_folder}/p.gif" width="{fino}" height="{altura}" border=0>')
    codbarras.append(f'<img src="{images_folder}/b.gif" width="{fino}" height="{altura}" border=0>')

    # Dados
    while len(texto) > 0:
        i = int(texto[:2])
        texto = texto[2:]
        s = barcodes[i]

        for j in range(0, 10, 2):
            f1 = fino if s[j] == '0' else largo
            codbarras.append(f'<img src="{images_folder}/p.gif" width="{f1}" height="{altura}" border=0>')

            f2 = fino if s[j+1] == '0' else largo
            codbarras.append(f'<img src="{images_folder}/b.gif" width="{f2}" height="{altura}" border=0>')

    # Guarda final
    codbarras.append(f'<img src="{images_folder}/p.gif" width="{largo}" height="{altura}" border=0>')
    codbarras.append(f'<img src="{images_folder}/b.gif" width="{fino}" height="{altura}" border=0>')
    codbarras.append(f'<img src="{images_folder}/p.gif" width="{fino}" height="{altura}" border=0>')

    return "".join(codbarras)


# Exemplo de uso
# html = GeraCodBarraBoleto("34192145200015516741120297322147779052633000")
# with open("barcode.html", "w", encoding="utf-8") as f:
#     f.write("<html><body>")
#     f.write(html)
#     f.write("</body></html>")     