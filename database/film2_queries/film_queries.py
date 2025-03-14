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


def get_movies_1940_1970():
    query = """
            select distinct(Title), `Production Company`, Director, `Actor 1`, `Release Year`, `Fun Facts`
            from film_locations_in_san_francisco
            where `Release Year` between 1940 and 1970
            order by `Release Year` desc;
            """
    with get_db_connection_film2() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def movies_where_writer_is(writer):
    query = """
    SELECT distinct(Title), `Release Year`, Director, Writer, `Actor 1`
    FROM `film2`.`film_locations_in_san_francisco`
    where Writer = %s;
    """
    with get_db_connection_film2() as cnx:
        cursor = cnx.cursor()
        cursor.execute(query, (writer,))
        result = cursor.fetchall()
        return result
