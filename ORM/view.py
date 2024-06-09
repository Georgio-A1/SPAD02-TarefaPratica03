# view.py
from controller import Controller

class View:
    def __init__(self):
        self.controller = Controller()

    def inserir_pedido(self):
        # Receber as informações do novo pedido do usuário
        order_data = {}
        order_data['customer_id'] = input("Digite o ID do cliente: ")
        order_data['employee_id'] = input("Digite o ID do vendedor: ")
        order_data['order_date'] = input("Digite a data do pedido (AAAA-MM-DD) ou pressione Enter para ignorar: ") or None
        order_data['required_date'] = input("Digite a data requerida (AAAA-MM-DD) ou pressione Enter para ignorar: ") or None
        order_data['shipped_date'] = input("Digite a data de envio (AAAA-MM-DD) ou pressione Enter para ignorar: ") or None
        order_data['freight'] = input("Digite o valor do frete ou pressione Enter para ignorar: ") or None
        order_data['ship_name'] = input("Digite o nome do destinatário ou pressione Enter para ignorar: ") or None
        order_data['ship_address'] = input("Digite o endereço de envio ou pressione Enter para ignorar: ") or None
        order_data['ship_city'] = input("Digite a cidade de envio ou pressione Enter para ignorar: ") or None
        order_data['ship_region'] = input("Digite a região de envio ou pressione Enter para ignorar: ") or None
        order_data['ship_postal_code'] = input("Digite o código postal de envio ou pressione Enter para ignorar: ") or None
        order_data['ship_country'] = input("Digite o país de envio ou pressione Enter para ignorar: ") or None

        order_data['order_details'] = []
        while True:
            detail = {}
            detail['productid'] = input("Digite o ID do produto: ")
            detail['unitprice'] = float(input("Digite o preço unitário: "))
            detail['quantity'] = int(input("Digite a quantidade: "))
            detail['discount'] = input("Digite o desconto (ou pressione Enter para ignorar): ") or None
            if detail['discount'] is not None:
                detail['discount'] = float(detail['discount'])
            order_data['order_details'].append(detail)
            more = input("Deseja adicionar mais itens ao pedido? (s/n): ")
            if more.lower() != 's':
                break

        # Chamar o método correspondente do controller para inserir o pedido
        if self.controller.inserir_pedido(order_data):
            print("Pedido inserido com sucesso!")
        else:
            print("Erro ao inserir o pedido!")

    def obter_info_pedido(self):
        order_id = input("Digite o ID do pedido: ")
        order_info = self.controller.obter_info_pedido(order_id)
        if order_info:
            print("Informações do Pedido:")
            print(f"Numero do pedido: {order_info['Numero do pedido']}")
            print(f"Data do pedido: {order_info['Data do pedido']}")
            print(f"Nome do cliente: {order_info['Nome do cliente']}")
            print(f"Nome do vendedor: {order_info['Nome do vendedor']}")
            print("Itens do pedido:")
            for item in order_info['Itens do pedido']:
                print(f"Produto: {item['Produto']}, Quantidade: {item['Quantidade']}, Preço: {item['Preço']}")
        else:
            print("Pedido não encontrado!")

    def gerar_ranking_funcionarios(self):
        start_date = input("Digite a data de início (AAAA-MM-DD): ")
        end_date = input("Digite a data de fim (AAAA-MM-DD): ")
        ranking = self.controller.gerar_ranking_funcionarios(start_date, end_date)
        if ranking:
            print("Ranking de Funcionários:")
            for i, (lastname, firstname, total_pedidos, soma_valores_vendidos) in enumerate(ranking, start=1):
                print(f"{i}. {firstname} {lastname} - Total de Pedidos: {total_pedidos}, Soma dos Valores Vendidos: {soma_valores_vendidos}")
        else:
            print("Não foi possível gerar o ranking!")
