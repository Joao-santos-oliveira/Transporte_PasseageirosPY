import design_estrutura as d 
from datetime import datetime, timedelta
import numpy as np

linhas = []               # lista de linhas cadastradas
onibus_por_linha = {}     # dicionário: id da linha → lista de ônibus



# FUNÇAO PARA GERAR ASSENTOS (1 a 20, todos livres = True)

def gerar_assentos():
    """Retorna uma lista com 20 assentos livres (True = livre)."""
    return [True for _ in range(20)]


#FUNÇAO PARA INSERIR LINHA DE ONIBUS
 
def inserir_linha():
    """Insere uma nova linha no sistema."""

    print("\n=== CADASTRO DE NOVA LINHA ===")
    
    origem = input("Cidade de origem: ")
    destino = input("Cidade de destino: ")
    horario = input("Horário (hh:mm): ")
    valor = float(input("Valor da passagem: "))

    linha_id = len(linhas)  # ID automático baseado na quantidade de linhas já cadastradas

    nova_linha = {
        "id": linha_id,
        "origem": origem,
        "destino": destino,
        "horario": horario,
        "valor": valor
    }

    linhas.append(nova_linha)
    onibus_por_linha[linha_id] = []   # cria lista vazia para os ônibus desta linha
    d.exibir_linha(linha_id, nova_linha)

# FUNÇAO PARA GERAR ÔNIBUS DIÁRIOS PARA OS PROXIMOS 30 DIAS
 
def gerar_onibus_diarios(linha_id):
    """
    Cria um ônibus para cada dia dos próximos 30 dias.
    Cada ônibus tem:
      - data (dd/mm/aaaa)
      - lista de 20 assentos
    """

    hoje = datetime.now()
    lista_onibus = []

    for i in range(30):
        data = hoje + timedelta(days=i)
        data_str = data.strftime("%d/%m/%Y")

        onibus = {
            "data": data_str,
            "assentos": gerar_assentos()
        }

        lista_onibus.append(onibus)

    # salva no dicionário principal
    onibus_por_linha[linha_id] = lista_onibus

def cadastrar_linha_completa():
    """Cadastra a linha e cria seus ônibus dos próximos 30 dias."""
    
    inserir_linha()  # cria a linha normal
    linha_id = len(linhas) - 1
    gerar_onibus_diarios(linha_id)


# REMOVER LINHA

def remover_linha():
    """Remove uma linha pelo ID e apaga seus ônibus."""
    print("\n=== REMOVER LINHA ===")

    if not linhas:
        print("Nenhuma linha cadastrada.")
        return

    try:
        linha_id = int(input("Digite o ID da linha que deseja remover: "))
    except:
        print("ID inválido!")
        return

    # Verifica se o ID existe
    if linha_id < 0 or linha_id >= len(linhas) or linhas[linha_id] is None:
        print("Linha não encontrada.")
        return

    print(f"Linha removida: {linhas[linha_id]['origem']} → {linhas[linha_id]['destino']}")

    # Remove a linha substituindo por None (não quebra os IDs anteriores)
    linhas[linha_id] = None
    onibus_por_linha.pop(linha_id, None)

    print("Remoção concluída com sucesso.\n")

#ALTERAR LINHA

def alterar_linha():
    """Permite editar origem, destino, horário e valor de uma linha já cadastrada."""
    print("\n=== ALTERAR LINHA ===")

    if not linhas:
        print("Nenhuma linha cadastrada.")
        return

    try:
        linha_id = int(input("Digite o ID da linha que deseja alterar: "))
    except:
        print("ID inválido!")
        return

    if linha_id < 0 or linha_id >= len(linhas) or linhas[linha_id] is None:
        print("Linha não encontrada.")
        return

    linha = linhas[linha_id]

    d.exibir_linha_formatada(linha_id, linha)

    print("\nO que deseja alterar?")
    print("1 - Origem")
    print("2 - Destino")
    print("3 - Horário")
    print("4 - Valor")
    print("0 - Cancelar")

    op = input("Escolha: ")

    if op == "1":
        linha["origem"] = input("Nova cidade de origem: ")

    elif op == "2":
        linha["destino"] = input("Nova cidade de destino: ")

    elif op == "3":
        linha["horario"] = input("Novo horário (hh:mm): ")

    elif op == "4":
        try:
            linha["valor"] = float(input("Novo valor da passagem: "))
        except:
            print("Valor inválido.")
            return

    elif op == "0":
        print("Edição cancelada.")
        return

    else:
        print("Opção inválida.")
        return

    print("\nAlteração realizada com sucesso!\n")

#   CONSULTAR HORÁRIOS POR CIDADE

def consultar_horarios_por_cidade():
    """Mostra todas as linhas que partem ou chegam em determinada cidade."""
    print("\n=== CONSULTAR HORÁRIOS POR CIDADE ===")

    cidade = input("Digite o nome da cidade: ").strip()

    encontrou = False
    print("\nLinhas encontradas:\n")

    for linha in linhas:
        if linha is None:
            continue

        if cidade.lower() in (linha["origem"].lower(), linha["destino"].lower()):
            encontrou = True
            d.exibir_linha_formatada(linha["id"], linha)

    if not encontrou:
        print("Nenhuma linha encontrada para essa cidade.\n")
    else:
        print()

#   VALIDAR ÔNIBUS BASEADO NA HORÁRIO E DATA

def validar_onibus_data_hora(data, hora):
    try:
        dia, mes = map(int, data.split("/"))
        hora_atual = datetime.now()
        hora_onibus = datetime.strptime(hora, "%H:%M").time()

        onibus_dt = datetime(year=hora_atual.year, month=mes, day=dia,hour=hora_onibus.hour, minute=hora_onibus.minute)

        if onibus_dt < hora_atual and (mes, dia) < (hora_atual.month, hora_atual.day):
            onibus_dt = datetime(year=hora_atual.year + 1, month=mes, day=dia,hour=hora_onibus.hour, minute=hora_onibus.minute)

        if onibus_dt < hora_atual:
            return False
        else:
            return True
    except ValueError:
        return None
    
#   CONSULTAR ASSENTOS

def consultar_assentos():
    """Mostra todos os assentos disponpiveis para reserva ou para cancelamento"""
    print("\n=== CONSULTAR ASSENTOS ===")

    cidade = input("Digite o nome da cidade de destino: ").strip()

    encontrou = False
    ids_linha = []
    print("\nLinhas encontradas:\n")

    for linha in linhas:
        if linha is None:
            continue

        if cidade.lower() in linha["destino"].lower():
            encontrou = True
            ids_linha.append(linha["id"])
            d.exibir_linha_formatada(linha["id"], linha)

    if not encontrou:
        print("Nenhuma linha encontrada para essa cidade.\n")
        return
    else:
        print()

    op = -2
    while op != -1:
        try:
            id_linha_escolhido = int(input("Digite o id da linha escolhida: "))
            op = -1
            break
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.")
 
    if id_linha_escolhido in ids_linha:
        d.mostrar_onibus_da_linha(id_linha_escolhido)
    else:
        print("ID inválido!")
        return
    
    data_escolhida = input("Digite a data escolhida (dd/mm): ")

    onibus_escolhido = None

    for onibus in onibus_por_linha[id_linha_escolhido]:
        data_formatada = onibus['data'][:5]
        if data_escolhida == data_formatada:
            onibus_escolhido = onibus
            break

    if onibus_escolhido is None:
        print("Nenhum ônibus disponível! Data inválida!\n")
        return

    d.mostrar_horario_onibus(id_linha_escolhido, onibus_escolhido)
    horario_str = linhas[id_linha_escolhido]['horario']
    if ":" not in horario_str:
        horario_str = horario_str + ":00"
    print(f"Horário disponível para essa linha: {horario_str}h\n")

    disponivel= validar_onibus_data_hora(data_escolhida, horario_str)
    if not disponivel:
        print("Este ônibus já passou!")
        return
    elif disponivel == None:
        print("Data ou hora inválida!")
    
    #criar matriz para gerenciar os assentos
    matriz_controle = np.array(onibus_escolhido['assentos']).reshape((2, 10))
    d.exibir_assentos(matriz_controle)

    print("O que deseja escolher? ")
    print("1 - Reservar assento")
    print("2 - Excluir a reserva do assento")
    print("0 - Cancelar")
     
    op = input("Escolha: ")

    assento_disponivel = False
    if op == "1":

        while True:
            try:
                if True in onibus_escolhido['assentos']:
                    assento_disponivel = True
                    assento = int(input("\nInforme o número do assento: "))
                    if assento < 1 or assento > 20:
                        print("Número do assento inválido!")
                    else:
                        posicao_assento = assento - 1
                        if onibus['assentos'][posicao_assento] == False:
                            print("Este assento já está reservado!")
                        elif onibus['assentos'][posicao_assento] == True:
                            onibus['assentos'][posicao_assento] = False
                            linha_controle = posicao_assento // 10
                            coluna_controle = posicao_assento % 10
                            matriz_controle[linha_controle][coluna_controle] = False
                            print(f"\nAssento {assento} reservado com sucesso!")
                            d.exibir_assentos(matriz_controle)
                            break
                elif assento_disponivel is False:
                    print("Nenhum assento disponível para está data!\n")
                    return
            except ValueError as e:
                print(f"Erro ao digitar o número do assento! Por favor, insira apenas números inteiros.")

    elif op == "2":
        while True:
            try:
                if False in onibus_escolhido['assentos']:
                    assento_disponivel = True
                    assento = int(input("\nInforme o número do assento: "))
                    if assento < 1 or assento > 20:
                        print("Número do assento inválido!")
                    else:
                        posicao_assento = assento - 1
                        if onibus['assentos'][posicao_assento] == False:
                            print("Este assento já está reservado!")
                        elif onibus['assentos'][posicao_assento] == True:
                            onibus['assentos'][posicao_assento] = False
                            linha_controle = posicao_assento // 10
                            coluna_controle = posicao_assento % 10
                            matriz_controle[linha_controle][coluna_controle] = False
                            print(f"\nAssento {assento} reservado com sucesso!")
                            d.exibir_assentos(matriz_controle)
                            break
                elif assento_disponivel is False:
                    print("Nenhum assento disponível para está data!\n")
                    return
            except ValueError as e:
                print(f"Erro ao digitar o número do assento! Por favor, insira apenas números inteiros.")

        print("\nAlteração realizada com sucesso!\n")
    elif op == "0":
        print("Edição cancelada.")
        return
    else:
        print("Opção inválida.")
        return

    


