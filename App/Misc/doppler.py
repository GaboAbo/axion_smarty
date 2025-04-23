from extractor import extract_table_data


def doppler():
    data = '[\n'
    for item_index, item in enumerate(extract_table_data()):
        data += ' '*2 + '[\n'
        for elem_index, elem in enumerate(item):
            data += ' '*4 + '{\n'
            data += ' '*6 + f'"id": "{item_index}{elem_index+1}",\n'
            data += ' '*6 + f'"name": "{elem}",\n'
            if elem_index == 0:
                data += ' '*6 + f'"field": "picker",\n'
                data += ' '*6 + f'"value": "",\n'
            elif elem == "Comentarios":
                data += ' '*6 + f'"field": "area",\n'
                data += ' '*6 + f'"value": "",\n'
            else:
                data += ' '*6 + f'"field": "boolean",\n'
                data += ' '*6 + f'"value": False,\n'
            data += ' '*4 + '},\n'
        data += ' '*2 + '],\n'
    data += '];'

    with open("END.py", "w") as file:
        file.write(data)

doppler()