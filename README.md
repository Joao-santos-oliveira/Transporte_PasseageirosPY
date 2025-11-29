# 🟢 Sistema de Transporte de Passageiros

Trabalho desenvolvido por **João Gabriel Santos Oliveira** e por **Rita Mariê Amaral Siqueira**, alunos do curso de **Engenharia de Computação (CEFET - Campus V)**, para a disciplina de **Programação em Python**, orientada pelo professor **Guido Pantuza**.

---

## 1) Como iniciar e terminar a execução do programa

### Para iniciar o sistema:
1. Abra o arquivo em uma IDE (como **VSCode**) ou terminal;
2. Verifique se o **Python** está instalado (versão **3.13.3** ou superior) e se o terminal é compatível com ANSI colors (para as cores apareçam corretamente);
3. Execute o programa:
   - Na IDE: clique em **Run** ou no botão **"Play"** no arquivo **main.py**;
   - No terminal: navegue até o diretório do arquivo com o comando  
     ```bash
     cd python "main".py
     ```
4. O sistema será exibido na tela principal com as instruções do sistema.

### Para sair do sistema:
1. Utilize a opção **"(0) - Sair"** no menu principal;
2. Ou feche a janela que contém o arquivo;
3. Ou pressione **Ctrl + C** no terminal.


## 2) Opções oferecidas pelo programa

### No início do programa:
- Escolher a **opção do menu**, digitando um valor entre **0 e 10**;

### O menu oferece:
| Opção | Ação |
|:------:|:-----|
| (1) | Cadastrar nova linha |
| (2) | Remover linha |
| (3) | Editar linha |
| (4) | Mostrar todas as linhas cadastradas |
| (5) | Consultar horários por cidade |
| (6) |  Mostrar ônibus de uma linha específica |
| (7) | Consultar assentos |
| (8) | Ler Reservas a Partir de Arquivo de texto |
| (9) |  Visualizar Reservas Inválidas |
| (10) | Relatórios / Estatísticas |
| (0) | Sair |

---

##  3) Principais telas

O programa é executado no **terminal**, logo tem apenas a interface da linha de comando:

### Tela inicial:
<img width="452" height="401" alt="image" src="https://github.com/user-attachments/assets/1e77d645-c574-4625-bd99-e41152ce89dc" />

### Cadastro de Linha (opção 01):
<img width="393" height="320" alt="image" src="https://github.com/user-attachments/assets/d2acf9f1-ef52-4d9e-b949-2c6085500c04" />

### Remover  Linha (opção 02):
<img width="339" height="106" alt="image" src="https://github.com/user-attachments/assets/75956ee2-6782-49e8-b28c-b1271f644b40" />;

### Editar Linha (opção 03):
<img width="426" height="447" alt="image" src="https://github.com/user-attachments/assets/73cbfa43-2669-4f6a-b8e4-149713ea9090" />

### Mostrar todas as linhas cadastradas (opção 04):
<img width="436" height="344" alt="image" src="https://github.com/user-attachments/assets/40b0a8ea-4f23-40f6-a95c-74b861e3e3e3" />

### Consultar horários por cidade (opção 05):
<img width="426" height="500" alt="image" src="https://github.com/user-attachments/assets/5f8ea157-53af-4461-af3d-ad86580d183a" />

### Mostrar ônibus de uma linha específica (opção 06):
<img width="445" height="295" alt="image" src="https://github.com/user-attachments/assets/25c22feb-f8dd-4234-b6a4-adad56f67ba2" />

### Consultar assentos (opção 07):
<img width="467" height="664" alt="image" src="https://github.com/user-attachments/assets/1f2d32a7-2b8b-401e-b866-254dfa53544c" />

<img width="450" height="644" alt="image" src="https://github.com/user-attachments/assets/587ca0be-962a-44b2-8683-061cbd30fe65" />

### Ler Reservas a Partir de Arquivo de texto  (opção 08):
<img width="426" height="236" alt="image" src="https://github.com/user-attachments/assets/05a33048-370d-4378-aac4-b550bcdbec2f" />

### Visualizar Reservas Inválidas (opção 09):
<img width="587" height="331" alt="image" src="https://github.com/user-attachments/assets/f343d485-2f2e-4612-a758-15ae9427289a" />

### Relatórios / Estatísticas (opção 10):
<img width="436" height="388" alt="image" src="https://github.com/user-attachments/assets/7ef3b44a-f8c8-4233-af24-1e344db49213" />


## 04) 🧾 Conclusões

- O sistema conseguiu atender aos requisitos principais, permitindo cadastrar linhas, gerenciar horários, reservar assentos e gerar relatórios.

- A prática permitiu consolidar conceitos como modularização, manipulação de arquivos, tratamento de erros e estruturação de dados.

- A leitura de arquivos externos e o registro automático de reservas inválidas aumentaram a complexidade e funcionalidade do sistema.

- A visualização dos assentos e o uso de cores melhoraram a experiência do usuário no terminal.

⚠️ Limitações

- O sistema não utiliza banco de dados, o que limita persistência e escalabilidade.

- Não há controle de múltiplos usuários ou concorrência de reservas simultâneas.

🛠️ Possíveis Melhorias Futuras

- Criar interface gráfica ou painel web.



