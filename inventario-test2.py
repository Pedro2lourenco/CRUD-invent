#!/usr/bin/env python3

import sqlite3 as sq3
import csv
from datetime import datetime

agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

conn = sq3.connect('invent-test1.db')
cursor = conn.cursor()

cursor.execute('''create table if not exists invent1(id integer primary key autoincrement,tipo text not null,marca text not null, process text not null,storage integer,ram integer not null,num_up integer,last_up_data text,update_type text,sector text)''')

conn.commit()

def menu():

    update_csv = False

    print('''████████╗ █████╗ ███████╗ ██████╗ ██████╗ ███╗   ███╗\n ╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗ ████║\n   ██║   ███████║███████╗██║     ██║   ██║██╔████╔██║\n    ██║   ██╔══██║╚════██║██║     ██║   ██║██║╚██╔╝██║\n    ██║   ██║  ██║███████║╚██████╗╚██████╔╝██║ ╚═╝ ██║\n     ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝''')
    
    try:
        option = int(input(
            'Digite o comando desejado:\n'
            '1 - Adicionar\n'
            '2 - Deletar\n'
            '3 - Fazer modificação\n'
            '4 - Ler dados\n'
            '0 - Fechar\n'
        ))
    except ValueError:
        print("Digite um número válido.")
        return

    if option == 1:

        tipo = input("Tipo: ")
        marca = input("Marca: ")
        process = input("Processador: ")
        storage = int(input("Storage: "))
        ram = int(input("RAM: "))
        num_up = int(input("Número de upgrades: "))
        last_up_data = input("Data último upgrade: ")
        update_type = input("Tipo de upgrade: ")
        sector = input("Setor: ")

        create(tipo, marca, process, storage, ram, num_up, last_up_data, update_type, sector)

        update_csv = True

        print("Inventário atualizado.")

    elif option == 2:
        id = int(input("Selecione o ID para deletar: "))
        delete(id)

        update_csv = True

    elif option == 3:
        id = int(input("Selecione o ID para modificar: "))
        print("Digite os campos (ex: ram=16). Digite 'fim' para terminar:")

        valid_columns = {"tipo","marca","process","storage","ram","sector"}
        campos = {}

        while True:
            entrada = input(">> ")

            if entrada.lower() == "fim":
                break

            if "=" in entrada:
                chave, valor = entrada.split("=")

                chave = chave.strip()
                valor = valor.strip()

                
                if chave not in valid_columns:
                    print("Campo inválido!")
                    continue

                if valor.isdigit():
                    valor = int(valor)

                campos[chave] = valor
            else:
                print("Formato inválido. Use campo=valor")

        if campos:

            update(id, campos)
            update_csv = True

        else:
            print("Nenhuma alteração feita.")

    elif option == 4:
        read()

    elif option == 0:

        print('Salvando inventário...')

        cursor.execute('select * from invent1')
        data = cursor.fetchall()
        col = [desc[0] for desc in cursor.description]

        with open('inventario.csv','w',newline='',encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerow(col)
            write.writerows(data)

        conn.close()
        print('Fim do programa.')
        exit()

    else:
        print("Opção inválida.")

    if update_csv:
        cursor.execute('select * from invent1')
        data = cursor.fetchall()
        col = [desc[0] for desc in cursor.description]

        with open('inventario.csv','w',newline='',encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerow(col)
            write.writerows(data)

        print("Inventário atualizado.")
    

def create(tipo,marca,process,storage,ram,num_up,last_up_data,update_type,sector):

    cursor.execute('insert into invent1(tipo,marca,process,storage,ram,num_up,last_up_data,update_type,sector) values (?,?,?,?,?,?,?,?,?)',(tipo,marca,process,storage,ram,num_up,last_up_data,update_type,sector))
    conn.commit()

def read():
    cursor.execute('select * from invent1')
    data = cursor.fetchall()

    for line in data:
        print(line)

def update(id,field):

    valid_columns = {"tipo","marca","process","storage","ram","num_up","last_up_data","update_type","sector"}
    
    cursor.execute("SELECT * FROM invent1 WHERE id=?", (id,))
    if not cursor.fetchone():
        print("ID não encontrado.")
        return
    
    busca = 'UPDATE invent1 SET '
    values = []

    for chave, value in field.items():
        if chave in valid_columns:
            busca += f'{chave}=?, '
            values.append(value)
    

    if not values:
        print("Nenhum campo válido para atualizar.")
        return
    
    busca += "num_up = num_up + 1, "
    busca += "last_up_data = ?, "
    busca += "update_type = ?, "

    data_atual = datetime.now().strftime("%Y-%m-%d")

    tipo_update = ", ".join(field.keys())

    values.append(data_atual)
    values.append(tipo_update)
    
    busca = busca.rstrip(', ')
    busca += ' WHERE id=?'
    values.append(id)

    cursor.execute(busca, values)
    conn.commit()

    print(f"Computador {id} foi modificado.")


def delete(id):

    cursor.execute("SELECT * FROM invent1 WHERE id=?", (id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM invent1 WHERE id=?", (id,))
        conn.commit()
        print("Computador deletado com sucesso.")
    else:
        print("ID não encontrado.")


if __name__ == "__main__":
    while True:
        menu()

