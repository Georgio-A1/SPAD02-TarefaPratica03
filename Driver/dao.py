import psycopg2
from datetime import datetime

class DAO:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port="5432",
                database="northwind",
                user="postgres",
                password="postgres"
            )
            self.conn.autocommit = True
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados:", e)

    def get_next_orderid(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT MAX(orderid) FROM northwind.orders")
            max_orderid = cur.fetchone()[0]
            return max_orderid + 1 if max_orderid else 1
        except Exception as e:
            print("Erro ao obter o próximo ID do pedido:", e)
            return None

    def inserir_pedido(self, order_data):
        try:
            next_orderid = self.get_next_orderid()

            cur = self.conn.cursor()

            # Inserir dados na tabela de pedidos
            cur.execute("""
                INSERT INTO northwind.orders 
                (orderid, customerid, employeeid, orderdate, requireddate, shippeddate, freight, shipname, shipaddress, shipcity, shipregion, shippostalcode, shipcountry)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                next_orderid,
                order_data['customer_id'],
                order_data['employee_id'],
                order_data.get('order_date'),
                order_data.get('required_date'),
                order_data.get('shipped_date'),
                order_data.get('freight'),
                order_data.get('ship_name'),
                order_data.get('ship_address'),
                order_data.get('ship_city'),
                order_data.get('ship_region'),
                order_data.get('ship_postal_code'),
                order_data.get('ship_country')
            ))

            # Inserir detalhes do pedido
            for detail in order_data['order_details']:
                cur.execute("""
                    INSERT INTO northwind.order_details 
                    (orderid, productid, unitprice, quantity, discount)
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    next_orderid,
                    detail['productid'],
                    detail['unitprice'],
                    detail['quantity'],
                    detail.get('discount')
                ))

            return True
        except Exception as e:
            print("Erro ao inserir novo pedido:", e)
            return False

    def obter_info_pedido(self, order_id):
        try:
            cur = self.conn.cursor()

            # Consultar informações do pedido
            cur.execute("""
                SELECT o.orderid, o.orderdate, c.companyname AS customer_name, e.lastname || ', ' || e.firstname AS employee_name
                FROM northwind.orders o
                INNER JOIN northwind.customers c ON o.customerid = c.customerid
                INNER JOIN northwind.employees e ON o.employeeid = e.employeeid
                WHERE o.orderid = %s;
            """, (order_id,))
            order_info = cur.fetchone()

            if order_info:
                # Consultar os itens do pedido
                cur.execute("""
                    SELECT p.productname, od.quantity, od.unitprice
                    FROM northwind.order_details od
                    INNER JOIN northwind.products p ON od.productid = p.productid
                    WHERE od.orderid = %s;
                """, (order_id,))
                order_details = cur.fetchall()

                # Montar o dicionário com as informações do pedido
                result = {
                    'Numero do pedido': order_info[0],
                    'Data do pedido': order_info[1],
                    'Nome do cliente': order_info[2],
                    'Nome do vendedor': order_info[3],
                    'Itens do pedido': [{'Produto': item[0], 'Quantidade': item[1], 'Preço': item[2]} for item in order_details]
                }
                return result
            else:
                return None
        except Exception as e:
            print("Erro ao obter informações do pedido:", e)
            return None

    def gerar_ranking_funcionarios(self, start_date, end_date):
        try:
            cur = self.conn.cursor()

            # Consultar o ranking dos funcionários
            cur.execute("""
                SELECT e.lastname, e.firstname, COUNT(o.orderid) AS total_pedidos, SUM(od.quantity * od.unitprice) AS soma_valores_vendidos
                FROM northwind.orders o
                INNER JOIN northwind.employees e ON o.employeeid = e.employeeid
                INNER JOIN northwind.order_details od ON o.orderid = od.orderid
                WHERE o.orderdate >= %s AND o.orderdate <= %s
                GROUP BY e.lastname, e.firstname
                ORDER BY total_pedidos DESC;
            """, (start_date, end_date))
            ranking = cur.fetchall()
            return ranking
        except Exception as e:
            print("Erro ao gerar ranking de funcionários:", e)
            return None
