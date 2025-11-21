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
        linha += f"{cor}{data} ({livres}){C.RESET}".ljust(14)
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
    """Exibe os assentos do ônibus escolhido, mostrando a disponibilidade de acordo com as cores."""

    matriz_assentos = np.arange(1, 21).reshape((2, 10)) # matriz para mostrar o número do assento

    # usa a matriz de controle para verificar se está disponível ou não
    print(f"\n{C.AMARELO}{C.NEGRITO}📅 Visualização dos Assentos:{C.RESET}")
    print("-"*60)
    for linha in range(matriz_assentos.shape[0]):
        for coluna in range(matriz_assentos.shape[1]):
            if matriz_controle[linha][coluna] == True:
                print(f"[{C.VERDE}{matriz_assentos[linha][coluna]:02d}{C.RESET}]", end=" ") 
            elif matriz_controle[linha][coluna] == False:
                print(f"[{C.VERMELHO}{matriz_assentos[linha][coluna]:02d}{C.RESET}]", end=" ")
        print()
        if linha == 0:
            print()
    print("-"*60)
    print(f"{C.CIANO}Legenda:{C.RESET}")
    print(f"[ {C.VERDE}🟩{C.RESET} ] = assento disponível")
    print(f"[ {C.VERMELHO}🟥{C.RESET} ] = assento indisponível")
    print(f"Assentos ímpares têm vista para janela.\n")


def exibir_arquivo(nome_arquivo, arquivo):
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
        print("Erro ao exibir arquivo: ", e)
