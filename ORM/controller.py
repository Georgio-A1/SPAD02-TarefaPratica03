# controller.py
from dao import DAO

class Controller:
    def __init__(self):
        self.dao = DAO()

    def inserir_pedido(self, order_data):
        return self.dao.inserir_pedido(order_data)

    def obter_info_pedido(self, order_id):
        return self.dao.obter_info_pedido(order_id)

    def gerar_ranking_funcionarios(self, start_date, end_date):
        return self.dao.gerar_ranking_funcionarios(start_date, end_date)
