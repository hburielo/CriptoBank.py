import random
from datetime import datetime

#====================|| LISTAS E DICIONÁRIOS ||====================# 
cpf = []
cpf_formatado = []
nome = []
senha = []
extrato = []  
valor_cripto = {
    
    'BTC': 338034.0,
    'ETH': 19350.0,
    'XRP': 3.0,
}
cripto_codigos = {
    'Real':'REAL',
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Ripple': 'XRP'
}
saldo = {
    'Real': 0.0,
    'Bitcoin': 0.0,
    'Ethereum': 0.0,
    'Ripple': 0.0,
}
saldo_cripto = []
#======================================================================#
#====================|| FUN. SALVAR USUARIO  ||====================#
def salvar_usuarios(cpf,nome,senha):
    with open('usuario.txt', 'a') as arquivo:
        for dados in range(len(cpf)):
            arquivo.write(f"CPF:{cpf[dados]}\nNome:{nome[dados]}\nSenha:{senha[dados]}\n\n")
#====================|| FUN. CADASTRAR ||====================#
def cadastro_usuario():
    while True:
        CPF = input("CPF: ")
        if not CPF.isdigit() or (len(CPF) != 11):
            print("CPF inválido. Digite um CPF válido!")
            print("Tente novamente!")
        else:
            cpf.append(CPF)
            break
    NOME = input('Nome: ')
    nome.append(NOME)
    while True:
        SENHA = input('Senha: ')
        if not SENHA.isdigit() or len(SENHA) != 6:
            print("Senha inválida. Digite uma senha válida!")
            print("Tente novamente!")
        else:
            senha.append(SENHA)
            break
    
    extrato.append([])
    salvar_usuarios(cpf,nome,senha)  
    print("Usuário cadastrado com sucesso!")
    print("=============================================================")
#====================================================================#

#====================|| FUN. FORMAT CADASTRAR ||====================#

def formatar_cpf(cpf):
    cpf_formatado = "{:03d}.{:03d}.{:03d}-{:02d}".format(
        int(cpf[:3]), int(cpf[3:6]), int(cpf[6:9]), int(cpf[9:])
    )
    return cpf_formatado
#===================================================================#

#====================|| FUN. LOGIN  ||====================#

def fazer_login():
    print("=============================================================")
    login_cpf = input("CPF: ")
    login_senha = input("Senha: ")

    if login_cpf in cpf:
        index = cpf.index(login_cpf)
        if login_senha == senha[index]:
            print("Acesso realizado com sucesso!")
            print(f"Seja Bem-Vindo, {nome[index]}")
            return index
        else:
            print("Senha incorreta!")
            return None
    else:
        print("Usuário não encontrado!")
        print()
        return None
#======================================================================#

#====================|| FUN. MENU  ||====================#

def mostrar_menu():
    print("=============================================================")
    menu = {
        1: '1. Consultar saldo',
        2: '2. Consultar extrato',
        3: '3. Depositar',
        4: '4. Sacar',
        5: '5. Comprar criptomoedas',
        6: '6. Vender criptomoedas',
        7: '7. Atualizar cotação',
        8: '8. Sair'
    }
    print(" ")

    for valor in menu.values():
        print(valor)

#====================|| FUN. CONSULTAR SALDO ||====================#

def consultar_saldo(index):
    print("=============================================================")
    print("")
    print("------------SALDO------------")
    print("Por gentileza, informe a senha cadastrada: ")
    saldo_senha = input("Senha: ")
    if saldo_senha == senha[index]:
        print('Nome:', nome[index])
        print('CPF:', formatar_cpf(cpf[index]))
        for moeda, valor in saldo.items():
            print(moeda + ":", f"{valor:.4f}")
    else:
        print("Senha incorreta!")

#====================|| FUN. CONSULTAR EXTRATO ||====================#

def consultar_extrato(index):
    print("=============================================================")
    print("")
    print("------------EXTRATO------------")
    print("Por gentileza, informe a senha cadastrada: ")
    extrato_senha = input("Senha: ")
    if extrato_senha == senha[index]:
        print('Nome:', nome[index])
        print('CPF:', formatar_cpf(cpf[index]))
        for valor in extrato[index]:
            print(valor)
    else:
        print("Senha incorreta!")

#=====================================================================#
def salvar_extrato(index):
    with open('extrato.txt', 'w') as file:
        for index, registros in enumerate(extrato):
            for registro in registros:
                file.write(f"{registro}\n")
            file.write("\n")
            file.close()

#====================|| FUN. REGISTRAR EXTRATO ||====================#

def registrar_extrato(index, operacao, valor, moeda, taxa=0.0, quantidade=0.0):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    saldo_formatado = f"REAL: {saldo['Real']:.2f} BTC: {saldo['Bitcoin']:.5f} ETH: {saldo['Ethereum']:.5f} XRP: {saldo['Ripple']:.5f}"

    if moeda == 'REAL':
        valor_cotacao_moeda = 0.00
    else:
        valor_cotacao_moeda = valor_cripto[cripto_codigos[moeda]]

    sinal = '+' if operacao in ['Depósito', 'Compra de Criptomoeda'] else '-'
    valor_formatado = f"{sinal} {valor:.2f} {moeda}".center(20)
    cotacao_formatada = f"{valor_cotacao_moeda:.2f}".center(10)
    taxa_formatada = f"{taxa:.2f}".center(10)
    saldo_formatado_centered = saldo_formatado.center(40)

    registro = f"{timestamp} | {valor_formatado} | CT: {cotacao_formatada} | TX: {taxa_formatada} | {saldo_formatado_centered}"
    extrato[index].append(registro)

    salvar_extrato(index)


#======================================================================#


#====================|| FUN. DEPOSITAR CORRETORA ||====================#

def depositar(index):
    print("=============================================================")
    print("")
    print("------------DEPÓSITO------------")
    print("Qual a quantia deseja depositar? ")
    deposito = float(input("R$: "))
    saldo['Real'] += deposito
    registrar_extrato(index, 'Depósito', deposito, 'REAL')
    print(f"Valor depositado: + {deposito:.2f} REAL")
    print(f"Saldo atual: {saldo['Real']:.2f} REAL")



#======================================================================#

#====================|| FUN. SACAR CORRETORA ||====================#

def sacar(index):
    print("=============================================================")
    print("")
    print("------------SAQUE------------")
    print("Qual o valor deseja sacar? ")
    saque = float(input("R$: "))
    if saque <= saldo['Real']:
        saldo['Real'] -= saque
        registrar_extrato(index, 'Saque', saque, 'REAL')
        print(f"Valor retirado: - {saque:.2f} REAL")
        print(f"Saldo atual: {saldo['Real']:.2f} REAL")
    else:
        print("Saldo insuficiente!")


#=======================================================================#

#====================|| FUN. ATT COTAÇÃO ||====================#

def atualizar_cotacao():
    print("=============================================================")
    print("")
    print("------------COTAÇÃO------------")
    for cripto in valor_cripto:
        num_aleatorio = random.randint(-5, 5)
        variacao = (num_aleatorio / 100) * valor_cripto[cripto]
        valor_atualizado = valor_cripto[cripto] + variacao
        valor_cripto[cripto] = valor_atualizado
        print(f"{cripto}: {valor_cripto[cripto]:.2f}")

#======================================================================#

#====================|| FUN. COMPRAR CRIPTO ||====================#
def comprar_cripto(index):
    total_compra = 0
    print("=============================================================")
    print("")
    print("------------COMPRAR CRIPTO------------")
    print("Por gentileza, informe a senha cadastrada: ")
    compra_senha = input("Senha: ")
    if compra_senha == senha[index]:
        cripto_menu = {
            1: 'Bitcoin',
            2: 'Ethereum',
            3: 'Ripple',
        }

        for chave, moeda in cripto_menu.items():
            print(f'{chave}. {moeda}')

        escolha_cripto = int(input("Qual moeda deseja comprar? "))
        print("")

        if escolha_cripto in cripto_menu:
            nome_moeda = cripto_menu[escolha_cripto]
            codigo_moeda = cripto_codigos[nome_moeda]
            valor_moeda = valor_cripto[codigo_moeda]
            print(f"Qual o valor em R$ que deseja comprar de {nome_moeda}? ")
            valor_em_real = float(input("R$: "))

            quantidade_moeda = valor_em_real / valor_moeda
            taxa = 0
            if nome_moeda == 'Bitcoin':
                taxa = 0.02
            elif nome_moeda in ['Ethereum', 'Ripple']:
                taxa = 0.01

            print("=============================================================")
            for chave, valor in valor_cripto.items():
                print(f"A cotação atualizada da {chave}: R${valor:.2f}")

            print("Deseja atualizar a cotação? (SIM ou NÃO)")   
            escolha_att = input("")    
            if escolha_att == "SIM":
                atualizar_cotacao()
                print("")
            elif escolha_att == "NÃO":
                pass  # Continue without updating the quote

            print("Deseja continuar com a transação? (SIM ou NÃO)")
            compra_senha_confirm = input("")
            if compra_senha_confirm == "SIM":
                total_compra = valor_em_real * (1 + taxa)

                if saldo['Real'] >= total_compra:
                    saldo['Real'] -= total_compra
                    saldo[nome_moeda] += quantidade_moeda

                    registrar_extrato(index, 'Compra de Criptomoeda', valor_em_real, nome_moeda, taxa, quantidade_moeda)
                    print(f"Compra realizada com sucesso: R${valor_em_real:.2f} em {nome_moeda}")
                    print(f"Saldo atual em {nome_moeda}: {saldo[nome_moeda]:.8f}")
                else:
                    print("Saldo em REAL insuficiente para realizar compra")
            else:
                print("Transação suspensa!")
        else:
            print("Opção inválida")
    else:
        print("Senha incorreta")



#======================================================================#


#======================================================================#

#====================|| FUN. VENDER CRIPTO ||====================#

def vender_cripto(index):
    print("============================================================")
    print("")
    print("------------VENDER CRIPTO------------")
    print("Por gentileza, informe a senha cadastrada: ")
    venda_senha = input("Senha: ")
    if venda_senha == senha[index]:
        cripto_menu = {
            1: 'Bitcoin',
            2: 'Ethereum',
            3: 'Ripple',
        }

        for chave, moeda in cripto_menu.items():
            print(f'{chave}. {moeda}')

        escolha_cripto = int(input("Qual moeda deseja vender? "))
        print("")

        if escolha_cripto in cripto_menu:
            nome_moeda = cripto_menu[escolha_cripto]
            codigo_moeda = cripto_codigos[nome_moeda]
            valor_moeda = valor_cripto[codigo_moeda]
            print(f"Qual o valor em {nome_moeda} que deseja vender? ")
            venda = float(input("Valor: "))
            print("=============================================================")

            taxa = 0
            if nome_moeda == 'Bitcoin':
                taxa = 0.03
            elif nome_moeda == 'Ethereum':
                taxa = 0.02
            elif nome_moeda == 'Ripple':
                taxa = 0.01
            print("=============================================================")
            for chave, valor in valor_cripto.items():
                print(f"A cotação atualizada da {chave}: R${valor:.2f}")

            print("Deseja atualizar a cotação? (SIM ou NÃO)")   
            escolha_att = input("")    
            if escolha_att == "SIM":
                atualizar_cotacao()
                print("")
            elif escolha_att == "NÃO":
                pass  # Continue without updating the quote
                
            print("Deseja continuar com a transação? (SIM ou NÃO)")
            
            venda_senha_confirm = input("")
            if venda_senha_confirm == "SIM":
                total_venda = venda * valor_moeda * (1 - taxa)

                if saldo[nome_moeda] >= venda:
                    saldo['Real'] += total_venda
                    saldo[nome_moeda] -= venda
                    registrar_extrato(index, 'Venda de Criptomoeda', total_venda, nome_moeda, taxa, venda)
                    print(f"Venda realizada com sucesso: {venda:.8f} {nome_moeda}")
                    print(f"Valor recebido em REAL: R${total_venda:.2f}")
                else:
                    print("Saldo insuficiente na criptomoeda para realizar a venda")
            else:
                print("Transação suspensa!")
        else:
            print("Opção inválida")
    else:
        print("Senha incorreta")


#======================================================================#

#====================|| CÓDIGO PRINCIPAL ||====================#
def principal():
    while True:
        print("=============================================================")
        print("Bem-vindo(a) à Camporese Exchange!")
        print("Ser um parceiro tem seus privilégios.")
        print("")
        print("Selecione uma opção abaixo:")
        print("1. Cadastro")
        print("2. Login")
        print("3. Sair")
        print("=============================================================")
        escolha = int(input("Escolha: "))

        if escolha == 1:
            cadastro_usuario()
        elif escolha == 2:
            usuario_logado = fazer_login()
            if usuario_logado is not None:
                while True:
                    mostrar_menu()
                    opcao = int(input("Digite o número da opção desejada: "))

                    if opcao == 1:
                        consultar_saldo(usuario_logado)
                    elif opcao == 2:
                        consultar_extrato(usuario_logado)
                    elif opcao == 3:
                        depositar(usuario_logado)
                    elif opcao == 4:
                        sacar(usuario_logado)
                    elif opcao == 5:
                        comprar_cripto(usuario_logado)
                    elif opcao == 6:
                        vender_cripto(usuario_logado)
                    elif opcao == 7:
                        atualizar_cotacao()
                    elif opcao == 8:
                        break
                    else:
                        print("Opção inválida!")
            else:
                continue
        elif escolha == 3:
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

#==============================================================#
principal()