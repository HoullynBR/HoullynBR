import time
import getpass

lista = []

while True:
        user = "Matheus"
        key = 12345
        licensa = 30
        login = str(input("\n !#!#!#!    Digite seu usuario: "))
        senha = float(input("\n !#!#!#!    Digite sua senha: "))
        print("\n       ### Aguarde... ### ")
        time.sleep(3)
        if login == user and senha == key:
            print(f"\n !#!#!#! Login efetuado com sucesso! !#!#!#!\n  !#!#! sua licensa expira em {licensa} dias !#!#!")
        else:
            print(f"\n !#!#!#! Senha e/ou Usuario incorretos\n !#!#!#! Deseja tentar acessar novamente?  !#!#!#!\n\n")
        break
while True:
    if login == user and senha == key:
        print(f"\n       !#!#!#! Menu Inicial !#!#!#!\n\n  !#!#!#! [1]  Adicionar item     !#!#!#!\n  !#!#!#! [2]  Mostar item      !#!#!#!  \n  !#!#!#! [3]  Editar item        !#!#!#!\n  !#!#!#! [4]  Remover item       !#!#!#!\n  !#!#!#! [5]  Exibir todos itens !#!#!#!\n")
    opcao = int(input("Selecione a opção: "))
    if opcao == 1:
        adicionar = input("Adicionar item: ")
        lista.append(adicionar)	
    elif opcao == 2:
        for item in lista:
            print (f"\n item: {item}")
    elif opcao == 3:
        break
    else:
            print("Opção Inválida!")
