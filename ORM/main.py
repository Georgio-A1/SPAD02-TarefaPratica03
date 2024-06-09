from view import View

def main():
    view = View()
    while True:
        print("1. Inserir novo pedido")
        print("2. Obter informações de um pedido")
        print("3. Gerar ranking de funcionários")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            view.inserir_pedido()
        elif opcao == '2':
            view.obter_info_pedido()
        elif opcao == '3':
            view.gerar_ranking_funcionarios()
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
