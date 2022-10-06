from asyncio import events
from PySimpleGUI import PySimpleGUI as sg
from tkinter import *
#janela-inicio. Da linha 3 a 12 está o código responsável pela criação da interface gráfica
def janela_inicial():    
    sg.theme('lightgreen')
    menu_def=['&Tools', ['&Detalhar','&Close']],['&Save',['&Save File', 'Save &As','Save &Copy'  ]]
    layout = [
        [sg.Menu(menu_def, background_color='darkgrey',text_color='black', disabled_text_color='yellow', font='Verdana', pad=(10,10))],
        [sg.Text('Data:  '), sg.Text(), sg.Text(), sg.Input(key='data', size=(28))],
        [sg.Text('Código:      '), sg.Input(key='codigo', size=(28))],
        [sg.Text('Quantidade:'), sg.Input(key='quantidade', size=(28))],
        [sg.Text('Tipo:'), sg.Radio('Compra', "Radio01", default=False), sg.Radio('Venda', "Radio01", default=True, key='tipo')],
        [sg.Text('Preço:'), sg.Input(key='preco', size=(32))],
        [sg.Text('Taxa: '), sg.Input(key='taxa', size=(32)) ],
        [sg.Text()],
        [sg.Output(size=(40, 10))],#Output me permite mostrar as coisa na tela,
        [sg.Button('Salvar'), sg.Button('Gerar IR')],

    ]
    return sg.Window('Calculadora de IR', layout=layout, finalize=True)
    #fim da janela1

def janela_detalhes():
    sg.theme('lightgreen')
    layout = [
        [sg.Text('Códigos das empresas')],
        [sg.Output(size=(40, 10)), sg.Image(r'/home/gabriel/Desktop/coin-flip-59(1).gif')],
        [sg.Input(key='codigo_escolhido', size=(42, 10)), sg.Button('Go'), sg.Button('Voltar')],
    ]
    return sg.Window('Detalhes', layout=layout, finalize=True)
    #fim da segunda janela

def janela_detalhes2():
    sg.theme('lightgreen')
    layout = [
        [sg.Output(size=(83, 10))],
        [sg.Button('Voltar')]
    ]
    return sg.Window('Detalhes da empresa escolhida', layout=layout, finalize=True)

#Essas variáveis armazenam dados das operações que serão usados no calculo do IR.
contador = 0
total_vendido = 0
total_investido = 0
impostoirrf = 0
quinze = 0
total_taxa_corretagem = 0
codigos = []

janela1, janela2, janela3 = janela_inicial(), None, None

while True:
    window, eventos, valores = sg.read_all_windows()
    #em cada linha  da 27 a 36 é lida da interface gráfica o dado digitado e armazenado em uma variável.
    if window == janela1:
        data = valores['data']
        codigo = valores['codigo']
        quantidade = valores['quantidade']
        if valores['tipo'] == True:
            tipo = 'venda'
        else:
            tipo = 'compra'
        preco = valores['preco']
        taxa = valores['taxa']

        if eventos == sg.WIN_CLOSED or eventos == 'Close': 
            break

        if eventos == 'Detalhar':
            janela1.hide()
            janela2 = janela_detalhes()
            for cod in codigos:
                print(cod)

        #da linha 47 a 55 está a parte que armazena os dados armazenados nas variáveis em um arquivo de texto.
        if eventos == 'Salvar' and window == janela1:
            if codigo not in codigos:
                codigos.append(codigo)
            arquivo = open(f'{codigo}.txt','a+')

            contador += 1  #Essa variável serve somente para contar o número de transações feitas.
            arq = open(f"{codigo}.txt")
            cont = arq.readlines()
            cont.append(f'Data: {data}, Código: {codigo}, Quantidade: {quantidade}, Tipo: {tipo}, Preço: {preco}, Taxa: {taxa}')#adiciona mais um elemento(linha) ao conteudo
            cont.append('\n')
            print(f'Transação {contador} salvada com sucesso!')
            arq = open(f'{codigo}.txt', 'w')
            arq.writelines(cont)
            arq.close()

            if tipo == 'compra':
                total_investido += int(quantidade) * float(preco)
                total_taxa_corretagem += float(taxa)

            else:
                total_vendido += int(quantidade) * float(preco)
                impostoirrf += 0.005/100 * total_vendido #calculo do importo irrf
                total_taxa_corretagem += float(taxa)

        lucro = total_vendido - total_investido
        quinze = 15/100 * lucro #15% é retirado do lucro no final do mês

        if eventos == 'Gerar IR':
            if total_vendido <= 20000:
                print('O total de vendas foi menos que R$20 mil, logo não é precisa pagar IR')
            else:
                #calculo do imposto de renda
                lucro_real = (lucro - quinze) - impostoirrf
                print(f'O valor do Imposto de Renda é de R${(lucro - lucro_real) - total_taxa_corretagem:.2f}')
    elif window == janela2:
        #Se não for a janela 1, então esse bloco será ativado para manibulação
        if eventos == sg.WIN_CLOSED:
            break

        if window == janela2 and eventos == 'Voltar':
            janela2.hide()
            janela1.un_hide()
            window = janela1
        
        if eventos == 'Go':#quando o botão Go for precionado...
            janela2.hide()
            janela3 = janela_detalhes2()

            file = valores['codigo_escolhido']
            file = open(f'{file}.txt')
            print(f'{file.readlines()}')

    else:
        if eventos == sg.WIN_CLOSED:
            break

        if eventos == 'Voltar':
            janela3.hide()
            janela2.un_hide()

