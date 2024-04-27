#biblioteca nativa do python
import os
import datetime

#biblioteca externa
from prettytable import PrettyTable

def imprimir_tabela(boletim, filtro_data=None, filtro_bairro=None, filtro_intervalo=None):
    tabela = PrettyTable()
    tabela.field_names = boletim[0].keys()

    if filtro_data:
        for item in boletim:
            if filtro_data in item['Data']:
                tabela.add_row(item.values())
    elif filtro_bairro:
        for item in boletim:
            if filtro_bairro in item['Bairros']:
                tabela.add_row(item.values())
    else:
        for registro in boletim:
            tabela.add_row(registro.values())
    
    limpar_terminal()
    print(tabela)
    input("\nClique [ENTER] para sair.")
    limpar_terminal()

def limpar_terminal():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')
    # Se for outro sistema operacional, usa o comando 'clear'
    else:
        os.system('clear')

def ler_boletim():
    cabecalho = []
    conjunto_valores = []

    with open("boletim.csv", "r") as arquivo:
        
        # Separação das linhas de texto do arquivo
        linhas_boletim = arquivo.read().split("\n")

        # Leitura e formatação do cabeçalho da tabela ('data', 'bairros', 'habitantes' etc)
        cabecalho = linhas_boletim[0].split(",")

        # Leitura e formataçãp das demais linhas da tabela
        for linha in linhas_boletim[1:]:
            valores = linha.strip().split(",")
            conjunto_valores.append(valores)

    return cabecalho, conjunto_valores
        
def formatar_boletim(cabecalho, conjunto_valores):
    boletim = []

    for valores in conjunto_valores:
        item_boletim = {}
        for i, valor in enumerate(valores):
            if valor.isdigit():
                item_boletim[cabecalho[i]] = int(valor)
            else:
                item_boletim[cabecalho[i]] = valor
        boletim.append(item_boletim)
    
    return boletim

def exibir_menu(titulo, opcoes):
    tabela_menu = PrettyTable()
    tabela_menu.field_names = ["Opção" ,titulo]

    for i, opcao in enumerate(opcoes):
        tabela_menu.add_row([i+1, opcao])
    
    print(tabela_menu)

def exibir_tela_dengue():
    limpar_terminal()

def exibir_tela_boletim():
    cabecalho, conjunto_valores = ler_boletim()
    boletim = formatar_boletim(cabecalho, conjunto_valores)

    exibir_menu("Análise do Boletim", ["Filtrar por data", "Filtrar por bairro", "Filtrar por intervalo", "<- Voltar"])

    opcao = input("Selecione uma opção acima: ").strip().lower()

    limpar_terminal()
    if opcao == "1":
        filtrar_data(boletim)
    elif opcao == "2":
        filtrar_bairro(boletim)
    elif opcao == "3":
        filtrar_intervalo(boletim)
    else:
        executar_tela_inicial()

#Função responsável filtrar o boletim a partir de uma data listada nele
def filtrar_data(boletim):
    datas_registradas = []
    data_selecionada = ''

    #Itera sobre os dicionários de boletim, verificando se a data se repete
    for item in boletim:
        if item['Data'] not in datas_registradas:
            datas_registradas.append(item['Data'])

    data_selecionada = selecionar_info_filtros(datas_registradas, "Datas")
    
    imprimir_tabela(boletim, filtro_data=data_selecionada)

def filtrar_bairro(boletim):
    bairros_registrados = []

    for item in boletim:
        if item['Bairros'] not in bairros_registrados:
            bairros_registrados.append(item['Bairros'])

    bairro_selecionado = selecionar_info_filtros(bairros_registrados, "Bairros")
    
    imprimir_tabela(boletim, filtro_bairro=bairro_selecionado)

def selecionar_info_filtros(items_registrados, tipo):
    opcao_valida = False
    item_selecionado = ''
    while not opcao_valida:
        exibir_menu(f"{tipo} Registrados", items_registrados)
        opcao = input("Selecione uma opção acima: ").strip().lower()

        if opcao.isdigit():
            if 0 < int(opcao) <= len(items_registrados):
                item_selecionado = items_registrados[int(opcao) - 1]
                opcao_valida = True
                
        limpar_terminal()
        print("[ERRO] Valor Inválido, por favor digite novamente")
    
    return item_selecionado


#Função responsável por exbir opções de ações e redirecionar o usuário para outras telas
def executar_tela_inicial():

    exibir_menu("DENGUE FREE FEIRA", ["Informações sobre Dengue", "Análise do Boletim", "Sair"])

    opcao = input("Selecione uma opção acima: ").strip().lower()

    limpar_terminal()
    if opcao == "1":
        exibir_tela_dengue()
    elif opcao == "2":
        exibir_tela_boletim()
    elif opcao == "3":
        return False
    else:
        print("[ERRO] Opção Inválida, por favor, digite novamente")

    #Tela inicial retorna um valor booleano verdadeira caso não haja seleção da opção 3
    return True
 
def main():
    continuar = True
    while continuar:
        continuar = executar_tela_inicial()    

if __name__ == "__main__":
    main()