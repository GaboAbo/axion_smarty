import pdfplumber
import re


def extract_table_data():
    with pdfplumber.open("App/Misc/Protocolo_vacio.pdf") as pdf:
        first_page = pdf.pages[0]
        table = first_page.extract_table()
        
    t = [[j if j != None else '' for j in i] for i in table]

    s = []
    for i in t[2:]:
        s.append([i[1], i[6] + ' ' + i[7]])

    table = [[re.sub(r'[^a-zA-Z0-9\s□áéíóúÁÉÍÓÚ%]', '', text[0]), re.sub(r'[^a-zA-Z0-9\s□áéíóúÁÉÍÓÚ%]', '', text[1])] for text in s]
    s = table

    c = []

    for i in range(len(s)-1, -1, -1):
        if s[i][0] == '':
            c.insert(0, s[i][1])
            s.pop(i)
        else:
            s[i][1] += ''.join(c)
            c = []

    for i in s:
        i[1] = i[1].split('□')

    for i in range(len(s)):
        for j in range(len(s[i][1])):
            s[i][1][j] = s[i][1][j].strip().replace("\n", "")
        s[i][0] = s[i][0].strip().replace("\n", " ")

    for i in s:
        if i[1][0] == '':
            i[1].pop(0)

    s[0][1] = ['Sin data', 'Data errónea', 'Sin trasmisión de ID', 'Usos', 'Minutos']
    s[-6][1] = ['Movimientos del control de angulación', 'Juego', 'Dirección del movimiento', 'Posición neutral Angulación', 'U', 'D', 'R', 'L']
    s[-11][1] = ['Tubo guía de luz cable OSF', 'Plegado', 'Percudido', 'Pinchado', 'Cortado']

    for i in s:
        i.extend(i[1])
        i.append("Comentarios")
        i.pop(1)

    pdf.close()
    return s
