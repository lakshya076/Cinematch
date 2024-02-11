import pymysql.cursors


def movie_exists(id: int, cursor: pymysql.cursors.Cursor) -> bool:
    """
    Returns `True` if movie exists in the database, else returns `False`
    """

    cursor.execute(f'select * from main where id={id}')

    if cursor.fetchall():
        return True

    else:
        return False


def get_recs(id: int, cursor: pymysql.cursors.Cursor) -> list[int]:
    """
    Returns recommended movies of a movie in a list, given its `id`
    """

    cursor.execute(f'select recommended from recommendation where id={id} order by popularity desc')
    data = cursor.fetchone()

    if data:

        if data[0]:
            return list(map(int, data[0].split('-')))
        else:
            return []

    else:
        return []


def get_pop(id: int, cursor: pymysql.cursors.Cursor) -> float:
    """
    Return popularity of a movie, given its `id`
    """

    cursor.execute(f'select popularity from recommendation where id={id}')
    data = cursor.fetchone()

    if data:
        return float(data[0])

    else:
        return 1.86  # Avg


def get_movie_info(id: int, cursor: pymysql.cursors.Cursor) -> list:
    """
    (id, title, overview, release_date, genres, language, popularity, cast, poster)
    """

    cursor.execute(f'select * from main where id = {id}')
    data = cursor.fetchall()

    if data:
        data = data[0]
        result = [int(data[0]), data[1], data[2], str(data[3]), data[4].split('-'), data[5], float(data[6]),
                  data[7].split('-'), data[8], data[9].split('-')]
        return result

    else:
        return False


def get_movies_info(ids: list, cursor: pymysql.cursors.Cursor) -> list[list]:
    """
    (id, title, overview, release_date, genres, language, popularity, cast, poster)
    """

    if ids == []:
        return []

    query = 'select * from main where '
    for i in ids:
        query += f'id = {i} or '

    query = query[:len(query) - 4]
    cursor.execute(f'{query} order by popularity desc')
    data = cursor.fetchall()

    if data:
        result = []

        for i in data:
            movie_info = [int(i[0]), i[1], i[2], str(i[3]), i[4].split('-'), i[5], float(i[6]), i[7].split('-'), i[8],
                          i[9].split('-')]
            result.append(movie_info)

        return result

    else:
        return False


def recommend_direct(id: int, depth: int, cursor: pymysql.cursors.Cursor) -> list[int]:
    """
    Searches for recommendation of a movie using the given recommendation till `depth`
    Returns `[]` if movie doesn't exist
    """

    og_recs = get_recs(id, cursor)

    if og_recs:
        recommendation = og_recs

        if depth == 1:
            return recommendation

        for i in og_recs[:]:
            recommendation += recommend_direct(i, depth - 1, cursor)

        return list(set(recommendation))

    else:
        return []


def pop_sort(ids: list[int], cursor: pymysql.cursors.Cursor) -> list[int]:
    """
    Sort given movies by popularity
    """

    pop_dict = {}
    for i in ids:
        popularity = get_pop(i, cursor)
        pop_dict[popularity] = i

    pop_list = list(pop_dict.keys())
    pop_list.sort(reverse=True)
    ids_sorted = []

    for i in pop_list:
        ids_sorted.append(pop_dict[i])

    return ids_sorted


def get_random(cursor: pymysql.cursors.Cursor, limit: int) -> list[int]:
    """
    Returns IDs of `limit` random movies whose popularity is above 50
    """

    cursor.execute(f'select id from main where popularity >= 50 order by rand() limit {limit}')

    return [int(i[0]) for i in cursor.fetchall()]
