import design_estrutura as d 
from datetime import datetime, timedelta

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

