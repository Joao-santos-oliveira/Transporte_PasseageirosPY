import estrutura as e
from datetime import datetime, timedelta
from desing_terminal import Cores as C
import numpy as np


def exibir_linha(linha_id, linha):
    print("\n" + "="*50)
    print("✔️  Linha cadastrada com sucesso!")
    print("="*50)

    print(f"🆔  ID da linha: {linha_id}")
    print(f"📍 Origem: {linha['origem']}")
    print(f"🏁 Destino: {linha['destino']}")
    print(f"⏰ Horário: {linha['horario']}")
    print(f"💰 Valor da passagem: R$ {linha['valor']:.2f}")

    print("-"*50)
    print("🗓️  Ônibus gerados para os próximos 30 dias.")
    print("="*50 + "\n")


def exibir_linha_formatada(linha_id, linha):
    print("\n" + "="*50)
    print("🚌  Detalhes da Linha")
    print("\n" + "="*50)

    print(f"🆔  ID da linha: {linha_id}")
    print(f"📍 Origem: {linha['origem']}")
    print(f"🏁 Destino: {linha['destino']}")
    print(f"⏰ Horário: {linha['horario']}")
    print(f"💰 Valor da passagem: R$ {linha['valor']:.2f}")

    print("="*50 + "\n")


def mostrar_linhas():
    """Exibe todas as linhas cadastradas, pulando as removidas."""
    print("\n" + "="*60)
    print("🚍  LINHAS CADASTRADAS")
    print("="*60)

    encontrou = False

    for linha in e.linhas:
        if linha is None:   # linha removida
            continue

        encontrou = True

        print(f"""
        🆔  ID da Linha: {linha['id']}
        📍 Origem:       {linha['origem']}
        🏁 Destino:      {linha['destino']}
        ⏰ Horário:      {linha['horario']}
        💰 Valor:        R$ {linha['valor']:.2f}
                """)
        print("-"*60)

    if not encontrou:
        print("Nenhuma linha cadastrada ainda.\n")


def mostrar_horario_onibus(linha_id, onibus_escolhido):
    """Exibe o horário do ônibus da linha escolhida em formato de calendário, mostrando assentos livres."""
    if linha_id < 0 or linha_id >= len(e.linhas):
        print(f"{C.VERMELHO}ID inexistente!{C.RESET}\n")
        return

    linha = e.linhas[linha_id]

    if linha is None:
        print(f"{C.VERMELHO}Esta linha foi removida e não possui ônibus cadastrados.{C.RESET}\n")
        return

    onibus_lista = e.onibus_por_linha.get(linha_id, [])

    print("\n" + "="*60)
    print(f"{C.AZUL}{C.NEGRITO}🗓️  ÔNIBUS DA LINHA {linha_id}{C.RESET}")
    print("="*60)

    if not onibus_lista:
        print(f"{C.VERMELHO}Nenhum ônibus encontrado para essa linha.{C.RESET}\n")
        return

    print(f"\n{C.AMARELO}{C.NEGRITO}📅 Calendário de Horários:{C.RESET}")
    print("-"*60)

    linha_impressao = ""
    count = 0

    horario = linha['horario'][:5]  # hh/mm
    livres = sum(onibus_escolhido["assentos"])

        # Escolhendo cor com base no número de assentos livres
    if livres == 20:
        cor = C.VERDE
    elif livres >= 10:
        cor = C.AMARELO
    else:
        cor = C.VERMELHO

    # Ex.: 12h (20)
    linha_impressao += f"{cor}{horario}h ({livres}){C.RESET}".ljust(14)
    count += 1

    if count == 6:   # 6 datas por linha
        print(linha_impressao)
        linha = ""
        count = 0

    if linha:
        print(linha_impressao)

    print("-"*60)
    print(f"{C.CIANO}Legenda:{C.RESET}")
    print(f"{C.VERDE}(20){C.RESET} = todos os assentos livres")
    print(f"{C.AMARELO}(10-19){C.RESET} = disponibilidade moderada")
    print(f"{C.VERMELHO}(0-9){C.RESET} = poucos assentos\n")



def mostrar_onibus_da_linha(linha_id):
    """Exibe os ônibus da linha em formato de calendário, mostrando assentos livres."""
    if linha_id < 0 or linha_id >= len(e.linhas):
        print(f"{C.VERMELHO}ID inexistente!{C.RESET}\n")
        return

    linha = e.linhas[linha_id]

    if linha is None:
        print(f"{C.VERMELHO}Esta linha foi removida e não possui ônibus cadastrados.{C.RESET}\n")
        return

    onibus_lista = e.onibus_por_linha.get(linha_id, [])

    print("\n" + "="*60)
    print(f"{C.AZUL}{C.NEGRITO}🗓️  ÔNIBUS DA LINHA {linha_id}{C.RESET}")
    print("="*60)

    if not onibus_lista:
        print(f"{C.VERMELHO}Nenhum ônibus encontrado para essa linha.{C.RESET}\n")
        return

    print(f"\n{C.AMARELO}{C.NEGRITO}📅 Calendário de Assentos:{C.RESET}")
    print("-"*60)

    linha = ""
    count = 0

    for onibus in onibus_lista:
        data = onibus['data'][:5]  # dd/mm
        livres = sum(onibus["assentos"])

        # Escolhendo cor com base no número de assentos livres
        if livres == 20:
            cor = C.VERDE
        elif livres >= 10:
            cor = C.AMARELO
        else:
            cor = C.VERMELHO

        # Ex.: 16/11 (20)
        linha += f"{cor}{data}({livres}){C.RESET} ".ljust(14)
        count += 1

        if count == 6:   # 6 datas por linha
            print(linha)
            linha = ""
            count = 0

    if linha:
        print(linha)

    print("-"*60)
    print(f"{C.CIANO}Legenda:{C.RESET}")
    print(f"{C.VERDE}(20){C.RESET} = todos os assentos livres")
    print(f"{C.AMARELO}(10-19){C.RESET} = disponibilidade moderada")
    print(f"{C.VERMELHO}(0-9){C.RESET} = poucos assentos\n")



def exibir_assentos(matriz_controle):
    """Exibe assentos no formato:
       01 02    04 03
       05 06    08 07
       ...
    """

    print(f"\n{C.AMARELO}{C.NEGRITO}📅 Visualização dos Assentos:{C.RESET}")
    print("-"*60)

    for i in range(1, 20, 4):  
        # esquerda
        a1 = i
        a2 = i+1

        # direita (invertido)
        a3 = i+3
        a4 = i+2

        # Função auxiliar para pegar cor conforme disponível
        def cor_assento(num):
            linha = (num - 1) // 10
            col = (num - 1) % 10
            return C.VERDE if matriz_controle[linha][col] else C.VERMELHO

        c1 = cor_assento(a1)
        c2 = cor_assento(a2)

        if a3 <= 20:
            c3 = cor_assento(a3)
        else:
            c3 = ""

        if a4 <= 20:
            c4 = cor_assento(a4)
        else:
            c4 = ""

        # Monta a linha com espaçamento do corredor
        linha_texto = (
            f"{c1}{a1:02d}{C.RESET} "
            f"{c2}{a2:02d}{C.RESET}    "
        )

        if a3 <= 20:
            linha_texto += f"{c3}{a3:02d}{C.RESET} "
        if a4 <= 20:
            linha_texto += f"{c4}{a4:02d}{C.RESET}"

        print(linha_texto)

    print("-"*60)
    print(f"{C.CIANO}Legenda:{C.RESET}")
    print(f"[ {C.VERDE}🟩{C.RESET} ] = Assento disponível") 
    print(f"[ {C.VERMELHO}🟥{C.RESET} ] = Assento indisponível")
    print("Ímpares = Janela esquerda | Pares = Corredor \n")


'''def exibir_arquivo(nome_arquivo, arquivo):
    try:
        if nome_arquivo == "reservarCorretas.txt":

            if not arquivo:
                print("Nenhuma reserva encontrada.")
                return
            
            print()
            print("="*60)
            print(f"{C.CIANO}{C.NEGRITO} LISTA DE RESERVAS {C.RESET}")
            print("="*60)
            print()

            for i, reserva in enumerate(arquivo):
                cidade = reserva.get('cidade', '???')
                data = reserva.get('data', '??/??/????')
                hora = reserva.get('hora', '??:??')
                assento = reserva.get('assento', '??')

                print(f"Reserva {i+1}) {cidade}")
                print(f"Data: {data}")
                print(f"Hora: {hora}")
                print(f"Assento: {assento}")
                print("-" * 60)
            

    except Exception as e:
        print("Erro ao exibir arquivo: ", e)'''

def relatorio_ocupacao_terminal(ocupacao):
    print("\n=== OCUPAÇÃO MÉDIA POR DIA DA SEMANA ===\n")
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    for linha in e.linhas:
        if linha is None:
            continue

        linha_id = linha["id"]
        print(f"Linha {linha_id} - {linha['origem']} → {linha['destino']}")

        valores = ocupacao.get(linha_id, [])

        for i, v in enumerate(valores):
            print(f"{dias[i]}: {v:.2f}%")

        print()


def relatorio_ocupacao_arquivo(ocupacao):
    nome = "relatorio_ocupacao.txt"
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    with open(nome, "w", encoding="utf-8") as arq:
        arq.write("=== OCUPAÇÃO MÉDIA POR DIA DA SEMANA ===\n\n")

        for linha in e.linhas:
            if linha is None:
                continue

            linha_id = linha["id"]
            arq.write(f"Linha {linha_id} - {linha['origem']} → {linha['destino']}\n")

            valores = ocupacao.get(linha_id, [])
            for i, v in enumerate(valores):
                arq.write(f"{dias[i]}: {v:.2f}%\n")

            arq.write("\n")

    print(f"\nArquivo '{nome}' gerado com sucesso!\n")

def relatorio_total_arrecadado_terminal(resultados):
    print("\n=== TOTAL ARRECADADO NO MÊS ATUAL ===\n")

    for r in resultados:
        print(f"Linha {r['linha_id']} - {r['origem']} → {r['destino']}")
        print(f"Total arrecadado: R$ {r['total']:.2f}\n")

def menu_relatorios():
    print("\n=== RELATÓRIOS DO SISTEMA ===")
    print("1 - Total arrecadado no mês atual")
    print("2 - Ocupação percentual média por dia da semana")
    print("0 - Voltar\n")

    op = input("Escolha: ")

    if op == "0":
        return

    print("\nComo deseja visualizar o relatório?")
    print("1 - Terminal")
    print("2 - Arquivo texto")
    print("3 - Gráfico")
    exibir = input("Escolha: ")


    if op == "1":

        resultados = e.calcular_total_arrecadado()
        if resultados is None:
            print("Nenhum dado de arrecadação disponível.")
            return

        if exibir == "1":
            relatorio_total_arrecadado_terminal(resultados)

        elif exibir == "2":
            e.relatorio_total_arrecadado_arquivo(resultados)

        elif exibir == "3":
            e.grafico_total_arrecadado()

        else:
            print("Opção inválida!")

        return  # ← evita cair no relatório 2

    elif op == "2":

        ocupacao = e.calcular_ocupacao_media()
        if ocupacao is None:
            print("Nenhum dado de ocupação disponível.")
            return

        if exibir == "1":
            relatorio_ocupacao_terminal(ocupacao)

        elif exibir == "2":
            relatorio_ocupacao_arquivo(ocupacao)

        elif exibir == "3":
            e.grafico_ocupacao_media()

        else:
            print("Opção inválida!")

        return

    else:
        print("Opção inválida!")


