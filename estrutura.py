import design_estrutura as d 
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from desing_terminal import Cores as C


linhas = []               # lista de linhas cadastradas
onibus_por_linha = {}     # dicionário: id da linha → lista de ônibus
erros_ocorridos = []   # lista para guardar erros ocorridos em tempo real




# FUNÇAO PARA GERAR ASSENTOS (1 a 20, todos livres = True)

def gerar_assentos():
    """Retorna uma lista com 20 assentos livres (True = livre)."""
    return [True for _ in range(20)]


#FUNÇAO PARA INSERIR LINHA DE ONIBUS ********************************************************************************************
 
def inserir_linha():
    """Insere uma nova linha no sistema."""
    
    print("\n=== CADASTRO DE NOVA LINHA ===")

    while True:

        origem = input("Cidade de origem: ").strip()
        if not origem:
            print(f"{C.VERMELHO}Origem inválida, favor inserir um local.{C.RESET}\n")
            continue
        break

    while True:
        destino = input("Cidade de destino: ").strip()
        if not destino:
            print(f"{C.VERMELHO}Destino inválido, favor inserir um local.{C.RESET}\n")
            continue
        break

    while True:
        horario = input("Horário (hh:mm): ").strip()

        if not horario or ":" not in horario:
            print(f"{C.VERMELHO}Horário inválido, digite hh:mm.{C.RESET}\n")
            continue

        horario_separado = horario.split(":")

        if len(horario_separado) != 2:
            print(f"{C.VERMELHO}Hora inválida, digite no formato hh:mm.{C.RESET}\n")
            continue

        try:
            hora = int(horario_separado[0])
            minuto = int(horario_separado[1])

            if hora < 0 or hora > 23:
                print(f"{C.VERMELHO}Hora inválida, digite um número entre 0 e 23.{C.RESET}\n")
                continue

            if minuto < 0 or minuto > 59:
                print(f"{C.VERMELHO}Minuto inválido, digite um número entre 0 e 59.{C.RESET}\n")
                continue

        except ValueError:
            print(f"{C.VERMELHO}Valor inválido, digite apenas números.{C.RESET}\n")
            continue

        break
        
    while True:
        try:
            valor = input("Valor da passagem: ").strip().replace(",", ".")
           
            if valor == "":
                print(f"{C.VERMELHO}Valor inválido, não pode ser vazio.{C.RESET}\n")
                continue

            valor = float(valor)

            if valor <= 0:
                print(f"{C.VERMELHO}Valor inválido, não permitido números negativos.{C.RESET}\n")
                continue

        except Exception:
            print(f"{C.VERMELHO}Valor inválido, digite apenas números.{C.RESET}\n")
            continue

        break
        

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
    """Verifica se o ônibus está na rota atual"""

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
    
#   CONSULTAR ASSENTOS ***************************************************************************************

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
        gravar_reserva_invalida("1", cidade)
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
        gravar_reserva_invalida("2", cidade)
        print("ID inválido!")
        return
    
    data_escolhida = input("Digite a data escolhida (dd/mm): ")

    try:
        dia, mes = data_escolhida.split("/")
        data_escolhida = f"{int(dia):02d}/{int(mes):02d}"
    except:
        print("Formato de data inválido!")
        gravar_reserva_invalida("5", cidade, data=data_original)
        return

    onibus_escolhido = None

    for onibus in onibus_por_linha[id_linha_escolhido]:
        data_formatada = onibus['data'][:5]
        if data_escolhida == data_formatada: # verifica se tem ônibus disponível nessa data
            onibus_escolhido = onibus
            data_original = onibus['data']
            break

    if onibus_escolhido is None:
        gravar_reserva_invalida("3", cidade, data=data_escolhida)
        print("Nenhum ônibus disponível! Data inválida!\n")
        return

    d.mostrar_horario_onibus(id_linha_escolhido, onibus_escolhido) # mostra o horário já escolhido
    horario_str = linhas[id_linha_escolhido]['horario']
    if ":" not in horario_str:
        horario_str = horario_str + ":00"
    print(f"Horário disponível para essa linha: {horario_str}h\n")

    disponivel= validar_onibus_data_hora(data_escolhida, horario_str) # verifica se o ônibus já passou
    if not disponivel:
        gravar_reserva_invalida("4", cidade, horario_str, data_original)
        print("Este ônibus já passou!")
        return
    elif disponivel == None:
        gravar_reserva_invalida("5", cidade, horario_str, data_original)
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
                        gravar_reserva_invalida("10",  cidade, horario_str, data_original, assento)
                        break
                    else:
                        posicao_assento = assento - 1
                        if onibus['assentos'][posicao_assento] == False:
                            gravar_reserva_invalida("7", cidade, horario_str, data_original, assento)
                            print("Este assento já está reservado!")
                            break
                        elif onibus['assentos'][posicao_assento] == True:

                            # faz a reserva do assento
                            onibus['assentos'][posicao_assento] = False
                            linha_controle = posicao_assento // 10
                            coluna_controle = posicao_assento % 10
                            matriz_controle[linha_controle][coluna_controle] = False
                            print(f"\nAssento {assento} reservado com sucesso!")
                            #gravar_reservas_corretas(cidade, horario_str, data_original, assento)
                            #d.exibir_assentos(matriz_controle)
                            break

                elif assento_disponivel is False:
                    assento = "??" 
                    gravar_reserva_invalida("6", cidade, horario_str, data_original, assento)
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
                        gravar_reserva_invalida("10",  cidade, horario_str, data_original, assento)
                        break
                    else:
                        posicao_assento = assento - 1
                        if onibus['assentos'][posicao_assento] == True:
                            gravar_reserva_invalida("8", cidade, horario_str, data_original, assento)
                            print("Este assento não está reservado!")
                            break
                        elif onibus['assentos'][posicao_assento] == False:

                            # libera o assento
                            onibus['assentos'][posicao_assento] = True
                            linha_controle = posicao_assento // 10
                            coluna_controle = posicao_assento % 10
                            matriz_controle[linha_controle][coluna_controle] = True
                            print(f"\nAssento {assento} liberado com sucesso!\n")
                            #excluir_reserva_arquivo(cidade, horario_str, data_original, assento)
                            #d.exibir_assentos(matriz_controle)
                            break

                elif assento_disponivel is True:
                    assento = "??" 
                    gravar_reserva_invalida("9", cidade, horario_str, data_original, assento)
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


#   ARQUIVO RESERVAS INVÁLIDAS *********************************************************************************

def gravar_reserva_invalida(erro='Erro inesperado ao realizar reserva!', cidade="Não encontrada", hora='??:??', data='??/??/????', assento='??'):
    """Gravar as reservas inválidas no arquivo .txt"""

    global erros_ocorridos

    nome_arquivo = "relatorioErros.txt"

    # Mapeamento de erros
    erros_map = {
        "1": "Nenhuma linha encontrada para essa cidade.",
        "2": "ID inválido para escolher a linha!",
        "3": "Nenhum ônibus disponível! Data inválida!",
        "4": "Este ônibus já passou!",
        "5": "Formato da data ou hora inválida!",
        "6": "Nenhum assento disponível para esta data!",
        "7": "Este assento já está reservado!",
        "8": "Este assento não está reservado, impossível desfazer reserva!",
        "9": "Nenhum assento reservado para esta data!",
        "10": "Número do assento inválido!"
    }

    cidade = cidade.strip() or "Não encontrada"
    erro_msg = erros_map.get(str(erro), erro)

    registro = {
        "cidade": cidade.title(),
        "hora": hora,
        "data": data,
        "assento": assento,
        "erro": erro_msg
    }

    # 1) salva em memória
    erros_ocorridos.append(registro)

    # 2) salva no arquivo
    try:
        with open(nome_arquivo, "a", encoding='utf-8') as arq:
            linha = f"{registro['cidade']}, {hora}, {data}, {assento}, {erro_msg}\n"
            arq.write(linha)
    except:
        print("Erro ao gravar erro no arquivo.")
        
#   MOSTRAR ERROS

def mostrar_erros():
    """Exibir as reservas inválidas gravadas no arquivo .txt"""

    global erros_ocorridos

    if not erros_ocorridos:
        print("\nNenhum erro registrado ainda.\n")
        return

    print("\nComo deseja visualizar os erros?")
    print("1 - Exibir no terminal")
    print("2 - Exportar para arquivo texto")
    opc = input("Escolha: ")

    if opc == "1":

        # Mostra todos os erros no terminal
        print("\n=== ERROS REGISTRADOS ===\n")
        for e in erros_ocorridos:
            print(f"{e['cidade']}, {e['hora']}, {e['data']}, {e['assento']}, {e['erro']}")
        print()

    elif opc == "2":

        # Salva erros em arquivo .txt
        nome = "relatorioErros.txt"
        try:
            with open(nome, "w", encoding="utf-8") as file:
                for e in erros_ocorridos:
                    file.write(f"{e['cidade']}, {e['hora']}, {e['data']}, {e['assento']}, {e['erro']}\n")
            print(f"\nArquivo '{nome}' gerado com sucesso!\n")
        except:
            print("Erro ao gerar arquivo!")

    else:
        print("Opção inválida.")


#   IMPORTAR RESERVAS DO ARQUIVO ************************************************************************************

def importar_reservas_arquivo():
    """Importar as reservas de um arquivo .txt"""

    print("\n=== IMPORTAR RESERVAS DE ARQUIVO ===")
    nome_arquivo = input("Digite o nome do arquivo (ex: reservas.txt): ").strip()

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arq:
            linhas_arquivo = arq.readlines()
    except:
        print(f"\nArquivo '{nome_arquivo}' não encontrado!\n")
        return

    print(f"\nLendo arquivo '{nome_arquivo}'...\n")

    for linha in linhas_arquivo:
        try:
            partes = linha.split(",")

            if len(partes) != 4:
                print(f"Linha inválida (formato errado): {linha.strip()}")
                gravar_reserva_invalida("5", cidade="??", hora="??", data="??/??/????", assento="??")
                continue

            # Remove espaços extras
            cidade, hora, data, assento = [p.strip() for p in partes]

            # Validar assento
            try:
                assento = int(assento)
            except:
                gravar_reserva_invalida("10", cidade, hora, data, assento="??")
                print(f"Erro: Assento inválido → {linha.strip()}")
                continue

             # Procura linha de ônibus correspondente
            linha_encontrada = None
            for ln in linhas:
                if ln and cidade.lower() in ln["destino"].lower():
                    linha_encontrada = ln
                    break

            if not linha_encontrada:
                gravar_reserva_invalida("1", cidade, hora, data, assento)
                print(f"Erro: Nenhuma linha para → {cidade}")
                continue

            linha_id = linha_encontrada["id"]

            # Procura ônibus com a mesma data
            onibus_escolhido = None
            for onibus in onibus_por_linha[linha_id]:
                if onibus["data"] == data:
                    onibus_escolhido = onibus
                    break

            if onibus_escolhido is None:
                gravar_reserva_invalida("3", cidade, hora, data, assento)
                print(f"Erro: Data sem ônibus → {data}")
                continue

            # Confere se a viagem já passou
            valido = validar_onibus_data_hora(data[:5], hora)
            if valido is False:
                gravar_reserva_invalida("4", cidade, hora, data, assento)
                print(f"Erro: Ônibus já passou → {data} {hora}")
                continue

            # Checa validade do número do assento
            if not (1 <= assento <= 20):
                gravar_reserva_invalida("10", cidade, hora, data, assento)
                print(f"Erro: Número do assento inválido → {assento}")
                continue

            # Verifica se o assento já está ocupado
            pos = assento - 1
            if onibus_escolhido["assentos"][pos] is False:
                gravar_reserva_invalida("7", cidade, hora, data, assento)
                print(f"Erro: Assento já reservado → {assento}")
                continue

            # Reserva o assento
            onibus_escolhido["assentos"][pos] = False
            #gravar_reservas_corretas(cidade, hora, data, assento)
            print(f"Reserva OK: {cidade}, {hora}, {data}, assento {assento}")

        except Exception as e:
            print(f"Erro inesperado ao processar linha: {linha.strip()}")
            gravar_reserva_invalida("Erro inesperado", cidade="??", data="??/??/????")
            continue

    print("\nImportação concluída!\n")

#       CALCULAR O TOTAL ARRECADADO *****************************************

def calcular_total_arrecadado():
    """
    Calcula o total arrecadado no mês atual para cada linha.
    Considera que cada assento reservado (False) representa uma passagem vendida.
    """

    hoje = datetime.now()
    mes_atual = hoje.month

    resultados = []

    for linha in linhas:
        if linha is None:
            continue

        linha_id = linha["id"]
        total = 0

        for onibus in onibus_por_linha.get(linha_id, []):
            data = datetime.strptime(onibus["data"], "%d/%m/%Y")

            # só conta o mês atual
            if data.month == mes_atual:
                assentos_reservados = sum(1 for a in onibus["assentos"] if a is False)
                total += assentos_reservados * linha["valor"]

        resultados.append({
            "linha_id": linha_id,
            "origem": linha["origem"],
            "destino": linha["destino"],
            "total": total
        })

    return resultados

#       CALCULAR A OCUPAÇÃO MÉDIA DE CADA LINHA ********************************************************

def calcular_ocupacao_media():
    """
    Calcula a ocupação percentual média de cada linha por dia da semana.
    
    Retorna um dicionário:
    { linha_id : [seg, ter, qua, qui, sex, sab, dom] }
    """

    ocupacao = {}

    for linha in linhas:
        if linha is None:
            continue

        linha_id = linha["id"]
        matriz = [ [] for _ in range(7) ]  # 7 dias da semana

        for onibus in onibus_por_linha.get(linha_id, []):
            data = datetime.strptime(onibus["data"], "%d/%m/%Y")
            dia_semana = data.weekday()  # 0=Seg ... 6=Dom

            total_assentos = 20
            reservados = sum(1 for a in onibus["assentos"] if a is False)

            porcentagem = (reservados / total_assentos) * 100
            matriz[dia_semana].append(porcentagem) # Guarda percentuais para cada dia

        medias = [] # média de ocupação para cada dia
        for lista in matriz:
            if lista:
                medias.append(sum(lista) / len(lista))
            else:
                medias.append(0)

        ocupacao[linha_id] = medias

    return ocupacao

#       GERAR ARQUIVO PARA RELATÓRIO DO TOTAL ARRECADADO

def relatorio_total_arrecadado_arquivo(resultados):
    """Gera arquivo com os totais arrecadados"""

    nome = "relatorio_total_arrecadado.txt"

    with open(nome, "w", encoding="utf-8") as arq:
        arq.write("=== TOTAL ARRECADADO NO MÊS ATUAL ===\n\n")
        for r in resultados:
            arq.write(f"Linha {r['linha_id']} - {r['origem']} → {r['destino']}\n")
            arq.write(f"Total arrecadado: R$ {r['total']:.2f}\n\n")

    print(f"\nArquivo '{nome}' gerado com sucesso!\n")

#       GERAR GRÁFICO DO TOTAL ARRECADADO

def grafico_total_arrecadado():
    """Gera um gráfico de barras para o total arrecadado por linha."""

    dados = calcular_total_arrecadado()

    linhas_x = [f"L{d['linha_id']}" for d in dados]
    valores_y = [d["total"] for d in dados]

    plt.figure()
    plt.bar(linhas_x, valores_y)
    plt.title("Total Arrecadado por Linha (Mês Atual)")
    plt.xlabel("Linha")
    plt.ylabel("Total (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#       GERAR GRÁFICO DA OCUPAÇÃO MÉDIA

def grafico_ocupacao_media():
    """Gera um gráfico de linhas com a ocupação média por dia da semana."""
    dados = calcular_ocupacao_media()

    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    plt.figure()
    for linha in linhas:
        if linha is None:
            continue

        linha_id = linha["id"]
        valores = dados.get(linha_id, [0]*7)

        plt.plot(dias, valores, label=f"Linha {linha_id}")

    plt.title("Ocupação Percentual Média por Linha e Dia da Semana")
    plt.xlabel("Dia da Semana")
    plt.ylabel("Ocupação (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


