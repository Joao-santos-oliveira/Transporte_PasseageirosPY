import estrutura as e
import design_estrutura as d
import auxilares as a
from desing_terminal import Cores as C

def menu():
    while True:
        print("\n" + C.AZUL_CLARO + C.NEGRITO + "="*60 + C.RESET)
        print(f"{C.VERDE_CLARO}{C.NEGRITO}     SISTEMA DE VENDA DE PASSAGENS – MENU PRINCIPAL{C.RESET}")
        print(C.AZUL + C.NEGRITO + "="*60 + C.RESET)

        print(f"{C.AMARELO_CLARO}1 - Cadastrar nova linha{C.RESET}")
        print(f"{C.AMARELO_CLARO}2 - Remover linha{C.RESET}")
        print(f"{C.AMARELO_CLARO}3 - Editar linha{C.RESET}")
        print(f"{C.AMARELO_CLARO}4 - Mostrar todas as linhas cadastradas{C.RESET}")
        print(f"{C.AMARELO_CLARO}5 - Consultar horários por cidade{C.RESET}")
        print(f"{C.AMARELO_CLARO}6 - Mostrar ônibus de uma linha específica{C.RESET}")
        print(f"{C.AMARELO_CLARO}7 - Consultar assentos{C.RESET}")
        print(f"{C.AMARELO_CLARO}8 - Ler Reservas a Partir de Arquivo de texto{C.RESET}")
        print(f"{C.AMARELO_CLARO}9 - Gravar Reservas Inválidas em arquivo de texto {C.CIANO}(A IMPLEMENTAR){C.RESET}")
        print(f"{C.AMARELO_CLARO}10 - Relatórios / Estatísticas  {C.CIANO}(A IMPLEMENTAR){C.RESET}")
        print(f"{C.AZUL}{C.NEGRITO}0 - Sair{C.RESET}")
        print(C.AZUL + C.NEGRITO + "="*60 + C.RESET)

        opc = input(f"{C.BRANCO_CLARO}Escolha uma opção: {C.RESET}")

        #OPÇÕES JÁ EXISTENTES 
       
        if opc == "1":
            e.cadastrar_linha_completa()

        elif opc == "2":
            e.remover_linha()

        elif opc == "3":
            e.alterar_linha()

        elif opc == "4":
            d.mostrar_linhas()
            
        elif opc == "5":
            e.consultar_horarios_por_cidade()

        elif opc == "6":
            try:
                linha_id = int(input(f"{C.BRANCO}Digite o ID da linha: {C.RESET}"))
                d.mostrar_onibus_da_linha(linha_id)
            except:
                print(f"{C.VERMELHO}ID inválido!{C.RESET}")   

        elif opc == "7":
            e.consultar_assentos()

#       OPÇÕES A IMPLEMENTAR 

        elif opc == "8":
            #print("\n Função 'Ler Reservas a Partir de Arquivo de texto' ainda não implementada.\n")
            arquivo = e.ler_arquivo("reservarCorretas.txt")
            d.exibir_arquivo("reservarCorretas.txt", arquivo)

        elif opc == "9":
            print("\n Função 'Gravar Reservas Inválidas em arquivo de texto' ainda não implementada.\n")    

        elif opc == "10":
            print("\n Função 'Relatórios' ainda não implementada.\n")

        elif opc == "0":
            print(f"\n{C.VERDE}Saindo do sistema...{C.RESET}")
            break

        else:
            print(f"\n{C.VERMELHO}Opção inválida! Tente novamente.{C.RESET}")

        input(f"\n{C.AMARELO_CLARO}Pressione ENTER para voltar ao menu...{C.RESET}")
        a.limpar_tela()
