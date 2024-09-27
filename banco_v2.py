import textwrap
from typing import List, Dict, Tuple, Optional

def menu() -> str:
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))

def atualizar_saldo_e_extrato(saldo: float, extrato: str, valor: float, tipo: str) -> Tuple[float, str]:
    saldo += valor
    extrato += f"{tipo}:\tR$ {valor:.2f}\n"
    return saldo, extrato

def depositar(saldo: float, valor: float, extrato: str) -> Tuple[float, str]:
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        saldo, extrato = atualizar_saldo_e_extrato(saldo, extrato, valor, "Depósito")
        print("\n=== Depósito realizado com sucesso! ===")
    return saldo, extrato

def sacar(saldo: float, valor: float, extrato: str, limite: float, numero_saques: int, limite_saques: int) -> Tuple[float, str, int]:
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    else:
        saldo, extrato = atualizar_saldo_e_extrato(saldo, extrato, -valor, "Saque")
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo: float, extrato: str) -> None:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios: List[Dict[str, str]]) -> None:
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf: str, usuarios: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia: str, numero_conta: int, usuarios: List[Dict[str, str]]) -> Optional[Dict[str, any]]:
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

def listar_contas(contas: List[Dict[str, any]]) -> None:
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """))

def main() -> None:
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0.0
    limite = 500.0
    extrato = ""
    numero_saques = 0
    usuarios: List[Dict[str, str]] = []
    contas: List[Dict[str, any]] = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo do sistema...")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
