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

        # verifica se a data/hora do ônibus já passou do dia atual
        if onibus_dt < hora_atual and (mes, dia) < (hora_atual.month, hora_atual.day):
            # se a data ainda vai acontecer no ano seguinte (ex: escolheu 05/01 e hoje é 20/12),
            # muda o ano do ônibus para o ano seguinte
            onibus_dt = datetime(year=hora_atual.year + 1, month=mes, day=dia,hour=hora_onibus.hour, minute=hora_onibus.minute)

        # depois de ajustar o ano, verifica novamente se o ônibus já passou
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
        gravar_reserva_invalida("1")
        print("Nenhuma linha encontrada para essa cidade.\n")
        return
    else:
        print()

    # escolher qual a linha do ônibus, pelo id, e automaticamente escolhe o horário
    while True:
        try:
            id_linha_escolhido = int(input("Digite o id da linha escolhida: "))
            break
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.\n")
 
    if id_linha_escolhido in ids_linha:
        d.mostrar_onibus_da_linha(id_linha_escolhido) # exibe as datas de funcionamento da linha
    else:
        gravar_reserva_invalida("2")
        print("ID inválido!")
        return
    
    data_escolhida = input("Digite a data escolhida (dd/mm): ")

    onibus_escolhido = None

    for onibus in onibus_por_linha[id_linha_escolhido]:
        data_formatada = onibus['data'][:5]
        if data_escolhida == data_formatada: # verifica se tem ônibus disponível nessa data
            onibus_escolhido = onibus
            data_original = onibus['data']
            break

    if onibus_escolhido is None:
        gravar_reserva_invalida("3")
        print("Nenhum ônibus disponível! Data inválida!\n")
        return

    d.mostrar_horario_onibus(id_linha_escolhido, onibus_escolhido) # mostra o horário já escolhido
    horario_str = linhas[id_linha_escolhido]['horario']
    if ":" not in horario_str:
        horario_str = horario_str + ":00"
    print(f"Horário disponível para essa linha: {horario_str}h\n")

    disponivel= validar_onibus_data_hora(data_escolhida, horario_str) # verifica se o ônibus já passou
    if not disponivel:
        gravar_reserva_invalida("4")
        print("Este ônibus já passou!")
        return
    elif disponivel == None:
        gravar_reserva_invalida("5")
        print("Formato da data ou hora inválida!")
        return
    
    # cria matriz para gerenciar os assentos
    matriz_controle = np.array(onibus_escolhido['assentos']).reshape((2, 10))

    # exibe os assentos
    d.exibir_assentos(matriz_controle)

    print("O que deseja escolher? ")
    print("1 - Reservar assento")
    print("2 - Excluir a reserva do assento")
    print("0 - Cancelar")
     
    op = input("Escolha: ")

    if op == "1":
        assento_disponivel = False
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
                            gravar_reserva_invalida("7")
                            print("Este assento já está reservado!")
                            break
                        elif onibus['assentos'][posicao_assento] == True:

                            # faz a reserva do assento
                            onibus['assentos'][posicao_assento] = False
                            linha_controle = posicao_assento // 10
                            coluna_controle = posicao_assento % 10
                            matriz_controle[linha_controle][coluna_controle] = False
                            print(f"\nAssento {assento} reservado com sucesso!")
                            gravar_reservas_corretas(cidade, horario_str, data_original, assento)
                            #d.exibir_assentos(matriz_controle)
                            break

                elif assento_disponivel is False:
                    gravar_reserva_invalida("6")
                    print("Nenhum assento disponível para está data!\n")
                    return
            except ValueError as e:
                print(f"Erro ao digitar o número do assento! Por favor, insira apenas números inteiros.")

    elif op == "2":
        assento_disponivel = True
        while True:
            try:
                if False in onibus_escolhido['assentos']:
                    assento_disponivel = False
                    assento = int(input("\nInforme o número do assento: "))

                    if assento < 1 or assento > 20:
                        print("Número do assento inválido!")
                    else:
                        posicao_assento = assento - 1
                        if onibus['assentos'][posicao_assento] == True:
                            gravar_reserva_invalida("8")
                            print("Este assento não está reservado!")
                            break
                        elif onibus['assentos'][posicao_assento] == False:

                            # libera o assento
                            onibus['assentos'][posicao_assento] = True
                            linha_controle = posicao_assento // 10
                            coluna_controle = posicao_assento % 10
                            matriz_controle[linha_controle][coluna_controle] = True
                            print(f"\nAssento {assento} liberado com sucesso!\n")
                            excluir_reserva_arquivo(cidade, horario_str, data_original, assento)
                            #d.exibir_assentos(matriz_controle)
                            break

                elif assento_disponivel is True:
                    gravar_reserva_invalida("9")
                    print("\nNenhum assento reservado para está data!\n")
                    return
            except ValueError as e:
                print(f"Erro ao digitar o número do assento! Por favor, insira apenas números inteiros.")

    elif op == "0":
        print("Edição cancelada.")
        return
    else:
        print("Opção inválida.")
        return

#   ARQUIVO COM RESERVAS CORRETAS

def gravar_reservas_corretas(cidade, hora, data, assento):
    nome_arquivo = "reservarCorretas.txt"
    try:
        with open(nome_arquivo, "a", encoding='utf-8') as arq:
            mensagem = f"{cidade.title()}, {hora}, {data}, {assento}\n"
            arq.write(mensagem)
    except Exception as e:
        print(f"Erro ao gravar reserva no arquivo: {e}")

def excluir_reserva_arquivo(cidade, hora, data, assento):
    nome_arquivo = "reservarCorretas.txt"
    mensagem = f"{cidade.title()}, {hora}, {data}, {assento}".lower().strip()

    try:
        with open(nome_arquivo, "r", encoding='utf-8') as arq:
            linhas = arq.readlines()

        with open(nome_arquivo, "w", encoding='utf-8') as arq:
            for linha in linhas:
                if linha.strip().lower() != mensagem:
                    arq.write(linha)

    except Exception as e:
        print(f"Erro ao apagar reserva no arquivo: {e}")

#   ARQUIVO RESERVAS INVÁLIDAS

def gravar_reserva_invalida(erro='Erro inesperado ao realizar reserva!', cidade="Não encontrada", hora='??:??', data='??/??/????', assento='??'):
    nome_arquivo = "reservasIncorretas.txt"

    erros_map = {
        "1": "Nenhuma linha encontrada para essa cidade.",
        "2": "ID inválido para escolher a linha!",
        "3": "Nenhum ônibus disponível! Data inválida!",
        "4": "Este ônibus já passou!",
        "5": "Formato da data ou hora inválida!",
        "6": "Nenhum assento disponível para esta data!",
        "7": "Este assento já está reservado!",
        "8": "Este assento não está reservado, impossível desfazer reserva!",
        "9": "Nenhum assento reservado para esta data!"
    }

    cidade= cidade.strip() or "Não encontrada"
    erro_msg = erros_map.get(str(erro), erro)

    try:
        with open(nome_arquivo, "a", encoding='utf-8') as arq:
            mensagem = f"[{hora} - {data}] | {cidade.title()} | Assento {assento} | Erro: {erro_msg}\n"
            arq.write(mensagem)
    except Exception as e:
        print(f"Erro ao gravar erro de reserva no arquivo: {e}")

def ler_arquivo(nome_arquivo):
    try:
        reservas = []
        if nome_arquivo == "reservarCorretas.txt":
            with open(nome_arquivo, "r", encoding='utf-8') as arq:
                for linha in arq:
                    cidade, hora, data, assento = [campo.strip() for campo in linha.split(",")]
                    nova_linha = {
                        'cidade': cidade.strip(),
                        'data': data.strip(),
                        'hora': hora.strip(),
                        'assento': assento.strip()
                    }
                    reservas.append(nova_linha)
        return reservas
    except Exception as e:
        print("Erro ao ler arquivo: ", e)
        return None



