def menu():
    # Define o menu de opções e solicita a escolha do usuário
    menu = """\n
    ================ MENU ================
    [d] Depositar\n
    [s] Sacar\n
    [e] Extrato\n
    [nc] Nova conta\n
    [lc] Listar contas\n
    [nu] Novo usuário\n
    [q] Sair\n
    => """
    return input(menu.strip())  # Remove espaços extras e solicita a entrada do usuário

def depositar(saldo, valor, extrato, /):
    # Função para realizar depósito
    if valor > 0:  # Verifica se o valor do depósito é positivo
        saldo += valor  # Adiciona o valor ao saldo
        extrato += f"Depósito:\tR$ {valor:.2f}\n"  # Adiciona a transação ao extrato
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato  # Retorna o saldo e o extrato atualizados

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Função para realizar saque
    excedeu_saldo = valor > saldo  # Verifica se o valor do saque é maior que o saldo
    excedeu_limite = valor > limite  # Verifica se o valor do saque excede o limite
    excedeu_saques = numero_saques >= limite_saques  # Verifica se o número de saques excedeu o limite

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor  # Subtrai o valor do saque do saldo
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"  # Adiciona a transação ao extrato
        numero_saques += 1  # Incrementa o número de saques
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato  # Retorna o saldo e o extrato atualizados

def exibir_extrato(saldo, /, *, extrato):
    # Função para exibir o extrato
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)  # Exibe o extrato
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")  # Exibe o saldo atual
    print("==========================================")

def criar_usuario(usuarios):
    # Função para criar um novo usuário
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)  # Verifica se o usuário já existe

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    # Função para filtrar usuário pelo CPF
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    # Função para criar uma nova conta
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    # Função para listar todas as contas
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha.strip())  # Remove espaços extras e exibe os detalhes da conta

def main():
    # Função principal do programa
    LIMITE_SAQUES = 3  # Define o limite diário de saques
    AGENCIA = "0001"  # Define a agência padrão

    saldo = 0  # Inicializa o saldo
    limite = 500  # Define o limite máximo de saque
    extrato = ""  # Inicializa o extrato
    numero_saques = 0  # Inicializa o contador de saques
    usuarios = []  # Inicializa a lista de usuários
    contas = []  # Inicializa a lista de contas

    while True:
        opcao = menu()  # Exibe o menu e captura a opção escolhida pelo usuário

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)  # Realiza o depósito

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )  # Realiza o saque

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)  # Exibe o extrato

        elif opcao == "nu":
            criar_usuario(usuarios)  # Cria um novo usuário

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)  # Adiciona a nova conta à lista

        elif opcao == "lc":
            listar_contas(contas)  # Lista todas as contas

        elif opcao == "q":
            break  # Sai do programa

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
