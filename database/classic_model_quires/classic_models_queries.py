from database.connection import get_db_connection_classic_model


def get_top_vendor():
    """Get the vendor with the highest total orders."""
    query = """
    SELECT pr.productVendor, SUM(od.quantityOrdered) AS total_orders
    FROM products pr
    JOIN orderdetails od ON pr.productCode = od.productCode
    GROUP BY pr.productVendor
    ORDER BY total_orders DESC
    LIMIT 1;
    """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def fetch_customers_by_country(country):
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        query = "SELECT customerName, city, country FROM customers WHERE country = %s"
        cursor.execute(query, (country,))
        results = cursor.fetchall()
    return results


def get_vendors_product_lines_products():
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        query = """
        select count(distinct productCode) as products_total, 
        count(distinct productLine) as prodlines_total, 
        count(distinct productVendor) as vendors_total
        from products
        """
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def get_avg_msrp_buy_price():
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        query = """
            select productVendor, avg(buyPrice) as avg_buy_price,
avg(MSRP) as avg_msrp
from products
group by productVendor
order by avg_buy_price desc
        """
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def number_of_vendors_product_lines_products():
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        query = """
        select count(distinct pr.productCode) as products_total, 
        count(distinct pl.productLine) as prodlines_total, 
        count(distinct pr.productVendor) as vendors_total
        from products pr
        left join productlines pl on pr.productLine=pl.productLine;
        """
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def max_sails_vendor():
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        query = """
            select pr.productVendor, sum(od.quantityOrdered) as total_orders
from products pr
join orderdetails od on pr.productCode=od.productCode
group by pr.productVendor
order by total_orders desc
limit 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result


def most_sold_product():
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        query = """
        select pr.productName, sum(od.quantityOrdered) as total_sold
from products as pr
join orderdetails as od
on pr.productCode=od.productCode
group by pr.productName
order by total_sold desc;
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result


def buyprice_msrp_difference():
    query = """
            select productName, buyPrice, MSRP, (buyPrice - MSRP) as marge
            from products
            order by productName;
            """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()

        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_union_buyprice():
    query = """
    select productName, buyPrice from products
        where buyPrice > 100
    union
        select productName, buyPrice from products
        where buyPrice < 200
        order by buyPrice desc;
    """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_all_canceled_orders():
    query = """
    select count(*)
from (select o.orderDate, o.shippedDate, o.comments, o.status
customerName
from orders as o
join customers as c on o.customerNumber=c.customerNumber
where status = 'Cancelled') as total_canceled;
    """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        return cursor.fetchone()


def all_orders_created():
    query = """
    select count(*)
from (select o.orderDate, o.shippedDate, o.comments, o.status
customerName
from customers as c
join orders as o on c.customerNumber=o.customerNumber) as all_orders;
    """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        return cursor.fetchone()


def number_of_products_per_product_line():
    query = """
    select productLine, count(distinct productName) as orig_products_per_product_line
        from products
    group by productLine;
    """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def number_of_no_customer_employees():
    query = """
    select count(*) from
(select concat(firstName, "", lastName) as saler_name,
count(distinct customerName) as customer
from employees as e
left join customers as c on e.employeeNumber=c.salesRepEmployeeNumber
group by saler_name
having customer = 0) as no_customer_emloyee;
    """
    with get_db_connection_classic_model() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        return cursor.fetchone()
