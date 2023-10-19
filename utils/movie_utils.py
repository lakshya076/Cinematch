import pymysql
import pymysql.cursors


def movie_exists(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Returns `True` if movie exists in the database, else returns `False`
    """

    cursor.execute(f'select * from main where id={id}')

    if cursor.fetchall():
        return True
    else:
        return False


def get_title(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return `title` of a movie, given its `id`
    Returns `False` if movie not found
    """

    if movie_exists(id, connection, cursor):
        cursor.execute(f'select title from main where id={id}')
        return cursor.fetchall()[0][0]
    else:
        return False


def get_poster(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return `poster path` of a movie, given its `id`
    Returns `False` if movie not found
    """

    if movie_exists(id, connection, cursor):
        cursor.execute(f'select poster from main where id={id}')
        return cursor.fetchall()[0][0]
    else:
        return False


def get_lang(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return `language` of a movie, given its `id`
    Returns `False` if movie not found
    """

    if movie_exists(id, connection, cursor):
        cursor.execute(f'select language from main where id={id}')
        return cursor.fetchall()[0][0]
    else:
        return False


def get_pop(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return `popularity` of a movie, given its `id`
    Returns `False` if movie not found
    """

    if movie_exists(id, connection, cursor):
        cursor.execute(f'select popularity from main where id={id}')
        return cursor.fetchall()[0][0]
    else:
        return False


def get_recs(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Returns recommended movies of a movie in a list, given its `id`
    """

    if movie_exists(id, connection, cursor):

        cursor.execute(f'select recommended from recommendation where id={id} order by popularity desc')
        return cursor.fetchall()[0][0].split('-')

    else:

        return []


def get_genz(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return genres of a movie in a list, given its `id`
    """

    if movie_exists(id, connection, cursor):

        cursor.execute(f'select genres from main where id={id}')
        return cursor.fetchall()[0][0].split('-')

    else:

        return []


def get_keyz(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return keywords of a movie in a list, given its `id`
    """

    if movie_exists(id, connection, cursor):

        cursor.execute(f'select keywords from recommendation where id={id}')
        return cursor.fetchall()[0][0].split('-')

    else:

        return []


def get_popularity(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Return popularity of a movie, given its `id`
    """

    if movie_exists(id, connection, cursor):

        cursor.execute(f'select popularity from recommendation where id={id}')
        return cursor.fetchall()[0][0]

    else:

        return 1.86  # Avg


def get_overview(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Returns the overview/description of a movie using its `id`
    """

    if movie_exists(id, connection, cursor):

        cursor.execute(f'select overview from main where id="{id}"')
        return cursor.fetchall()[0][0]

    else:

        return False


def get_release_date(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Returns the release date of the movie using its `id`

    Date is in format `YYYY-MM-DD`
    """

    if movie_exists(id, connection, cursor):

        cursor.execute(f'get release_date from main where id={id}')
        return cursor.fetchall()[0][0]

    else:

        return False


def recommend_direct(id: int, depth: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Searches for recommendation of a movie using the given recommendation till `depth`

    Returns `[]` if movie doesn't exist
    """

    if movie_exists(id, connection, cursor):

        og_recs = get_recs(id, connection, cursor)
        recommendation = og_recs

        if depth == 1:
            return recommendation

        for i in og_recs[:]:
            recommendation += recommend_direct(i, depth - 1, connection, cursor)

        return list(set(recommendation))

    else:

        return []


def pop_sort(ids: list, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    """
    Sort given movies by popularity
    """

    pop_dict = {}

    for i in ids:

        if movie_exists(i, connection, cursor):
            popularity = get_popularity(i, connection, cursor)
            pop_dict[popularity] = i

    pop_list = list(pop_dict.keys())
    pop_list.sort(reverse=True)
    ids_sorted = []

    for i in pop_list:
        ids_sorted.append(pop_dict[i])

    return ids_sorted
