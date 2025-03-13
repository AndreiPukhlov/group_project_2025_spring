from database.connection import get_db_connection_film2


def get_all_data():
    """Get the vendor with the highest total orders."""
    query = """
    select * from film2.film_locations_in_san_francisco
    limit 10;
    """
    with get_db_connection_film2() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def count_all_rows():
    """Get the vendor with the highest total orders."""
    query = """
        select count(*) from film2.film_locations_in_san_francisco;
        """
    with get_db_connection_film2() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
    return result
