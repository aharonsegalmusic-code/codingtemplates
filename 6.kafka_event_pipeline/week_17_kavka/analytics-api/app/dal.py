from .connection import db  # FIX: relative import


def top_customers():
    sql = """
    SELECT customers.customerNumber, customers.customerName, COUNT(orders.orderNumber)
    FROM customers
    LEFT JOIN orders ON orders.customerNumber = customers.customerNumber
    GROUP BY customers.customerNumber, customers.customerName
    ORDER BY COUNT(orders.orderNumber) DESC
    LIMIT 10;
    """.strip()
    return db.query(sql)


def customers_without_orders():
    sql = """
    SELECT c.customerNumber, c.customerName
    FROM customers c
    WHERE NOT EXISTS (
      SELECT 1 FROM orders o WHERE o.customerNumber = c.customerNumber
    )
    ORDER BY c.customerNumber;
    """.strip()
    return db.query(sql)


def zero_credit_active_customers():
    sql = """
    SELECT customers.customerNumber, customers.customerName, customers.creditLimit, COUNT(orders.orderNumber)
    FROM customers
    JOIN orders ON orders.customerNumber = customers.customerNumber
    WHERE customers.creditLimit = 0
    GROUP BY customers.customerNumber, customers.customerName, customers.creditLimit
    ORDER BY COUNT(orders.orderNumber) DESC;
    """.strip()
    return db.query(sql)