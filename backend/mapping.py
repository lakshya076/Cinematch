import pymysql, pymysql.cursors
from backend.Utils.mapping_utils import get_mapping_data, mapping_status


def add_liked_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[1]
    movies = list(map(int, movies))

    if og_data:

        og_movies.extend(movies)
        og_movies = list(set(map(str, og_movies)))

        cursor.execute(f'update mapping set liked_movies = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def add_disliked_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[2]
    movies = list(map(int, movies))

    if og_data:

        og_movies.extend(movies)
        og_movies = list(set(map(str, og_movies)))

        cursor.execute(f'update mapping set disliked_movies = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def add_watched_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[3]
    movies = list(map(int, movies))

    if og_data:

        og_movies.extend(movies)
        og_movies = list(set(map(str, og_movies)))

        cursor.execute(f'update mapping set watched_movies = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def add_recommended_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)

    if og_data:

        og_movies = og_data[6]
        movies = list(map(int, movies))

        og_movies.extend(movies)
        og_movies = list(set(map(str, og_movies)))

        cursor.execute(f'update mapping set recommendations = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def add_languages(langs: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_langs = og_data[5]

    if og_data:

        og_langs.extend(langs)
        og_langs = list(set(og_langs))

        cursor.execute(f'update mapping set languages = "{"-".join(og_langs)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def add_liked_genres(genres: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_genres = og_data[4]

    if og_data:

        og_genres.extend(genres)
        og_genres = list(set(og_genres))

        cursor.execute(f'update mapping set disliked_movies = "{"-".join(og_genres)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_liked_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[1]
    movies = list(map(int, movies))

    if og_data:

        og_movies = [str(i) for i in og_movies if i not in movies]

        cursor.execute(f'update mapping set liked_movies = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_disliked_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[2]
    movies = list(map(int, movies))

    if og_data:

        og_movies = [str(i) for i in og_movies if i not in movies]

        cursor.execute(f'update mapping set disliked_movies = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_watched_movies(movies: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[3]
    movies = list(map(int, movies))

    if og_data:

        og_movies = [str(i) for i in og_movies if i not in movies]

        cursor.execute(f'update mapping set watched_movies = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_recommended_movies(movies: list, username: str, connection: pymysql.Connection,
                              cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_movies = og_data[6]
    movies = list(map(int, movies))

    if og_data:

        og_movies = [str(i) for i in og_movies if i not in movies]

        cursor.execute(f'update mapping set recommendations = "{"-".join(og_movies)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_languages(langs: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_langs = og_data[5]

    if og_data:

        og_langs = [i for i in og_langs if i not in langs]

        cursor.execute(f'update mapping set languages = "{"-".join(og_langs)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_liked_genres(genres: list, username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    og_data = get_mapping_data(username, cursor)
    og_genres = og_data[4]

    if og_data:

        og_genres = [i for i in og_genres if i not in genres]

        cursor.execute(f'update mapping set disliked_movies = "{"-".join(og_genres)}" where username = "{username}"')
        connection.commit()

        return True

    else:
        return False


def delete_mapping(username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    status = mapping_status(username, cursor)

    if status == 1:

        cursor.execute(f'delete from mapping where username = "{username}"')
        connection.commit()

        return True

    else:
        return status


def remove_mapping(connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    cursor.execute('delete from deleted_mapping where removal_date < curdate()')
    connection.commit()
