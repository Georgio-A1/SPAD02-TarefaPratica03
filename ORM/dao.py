# dao.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc
from models import Base, Order, OrderDetail, Product, Customer, Employee
from datetime import datetime

class DAO:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/northwind')
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def get_next_orderid(self):
        max_orderid = self.session.query(func.max(Order.orderid)).scalar()
        return max_orderid + 1 if max_orderid else 1

    def inserir_pedido(self, order_data):
        try:
            next_orderid = self.get_next_orderid()

            # Cria um novo pedido
            novo_pedido = Order(
                orderid=next_orderid,
                customerid=order_data['customer_id'],
                employeeid=order_data['employee_id'],
                orderdate=datetime.strptime(order_data['order_date'], '%Y-%m-%d') if order_data['order_date'] else None,
                requireddate=datetime.strptime(order_data['required_date'], '%Y-%m-%d') if order_data['required_date'] else None,
                shippeddate=datetime.strptime(order_data['shipped_date'], '%Y-%m-%d') if order_data['shipped_date'] else None,
                freight=order_data['freight'] if order_data['freight'] else None,
                shipname=order_data['ship_name'] if order_data['ship_name'] else None,
                shipaddress=order_data['ship_address'] if order_data['ship_address'] else None,
                shipcity=order_data['ship_city'] if order_data['ship_city'] else None,
                shipregion=order_data['ship_region'] if order_data['ship_region'] else None,
                shippostalcode=order_data['ship_postal_code'] if order_data['ship_postal_code'] else None,
                shipcountry=order_data['ship_country'] if order_data['ship_country'] else None,
                shipperid=None
            )

            self.session.add(novo_pedido)
            self.session.flush()  # Para gerar o orderid

            # Cria os detalhes do pedido
            for detail in order_data['order_details']:
                novo_detalhe = OrderDetail(
                    orderid=novo_pedido.orderid,
                    productid=detail['productid'],
                    unitprice=detail['unitprice'],
                    quantity=detail['quantity'],
                    discount=detail['discount'] if detail['discount'] else 0
                )
                self.session.add(novo_detalhe)

            self.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir novo pedido: {e}")
            self.session.rollback()
            return False

    def obter_info_pedido(self, order_id):
        try:
            pedido = self.session.query(Order).filter_by(orderid=order_id).one()
            customer = self.session.query(Customer).filter_by(customerid=pedido.customerid).one()
            employee = self.session.query(Employee).filter_by(employeeid=pedido.employeeid).one()
            detalhes_pedido = self.session.query(OrderDetail).filter_by(orderid=order_id).all()

            itens_pedido = []
            for detalhe in detalhes_pedido:
                produto = self.session.query(Product).filter_by(productid=detalhe.productid).one()
                itens_pedido.append({
                    "Produto": produto.productname,
                    "Quantidade": detalhe.quantity,
                    "Preço": detalhe.unitprice
                })

            pedido_info = {
                "Numero do pedido": pedido.orderid,
                "Data do pedido": pedido.orderdate,
                "Nome do cliente": customer.companyname,
                "Nome do vendedor": f"{employee.firstname} {employee.lastname}",
                "Itens do pedido": itens_pedido
            }

            return pedido_info
        except Exception as e:
            print(f"Erro ao obter informações do pedido: {e}")
            return None

    def gerar_ranking_funcionarios(self, start_date, end_date):
        try:
            ranking = self.session.query(
                Employee.lastname,
                Employee.firstname,
                func.count(Order.orderid).label('total_pedidos'),
                func.sum(OrderDetail.unitprice * OrderDetail.quantity).label('soma_valores_vendidos')
            ).join(Order, Employee.employeeid == Order.employeeid
            ).join(OrderDetail, Order.orderid == OrderDetail.orderid
            ).filter(
                Order.orderdate >= start_date,
                Order.orderdate <= end_date
            ).group_by(
                Employee.lastname,
                Employee.firstname
            ).order_by(
                desc('soma_valores_vendidos')
            ).all()

            return ranking
        except Exception as e:
            print(f"Erro ao gerar ranking de funcionários: {e}")
            return None
