import os

#       LIMPAR A TELA

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
