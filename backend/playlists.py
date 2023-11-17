import backend.Utils.playlist_utils as playlist_utils
import backend.encryption as encryption
import pymysql, pymysql.cursors


def create_playlist(username: str, name: str, movies: str, password: str, connection: pymysql.Connection,
                    cursor: pymysql.cursors.Cursor) -> int:
    """
    Creates a playlist in the MySQL Database, if it doesn't already exist
    """
    status = playlist_utils.playlist_status(username, name, cursor)
    if not status:

        req_pass = int(bool(password))
        hashed_pass = ''
        if req_pass:
            hashed_pass = encryption.sha256(password)
            del password

        cursor.execute(
            f'insert into playlists values("{username}", "user", "{name}", "{movies}", {req_pass}, "{hashed_pass}", curdate())')
        connection.commit()

    return status


def update_password(username: str, name: str, new_pass: str, connection: pymysql.Connection,
                    cursor: pymysql.cursors.Cursor) -> int:
    """
    Updates the password of a playlist in the MySQL database, if it exists
    """
    hashed_password = encryption.sha256(new_pass)
    del new_pass

    status = playlist_utils.playlist_status(username, name, cursor) == 1

    if status == 1:
        cursor.execute(
            f'update playlists set password = "{hashed_password}" where username = "{username}" and name = "{name}"')
        connection.commit()

    return status


def add_movies(movies: list, username: str, name: str, connection: pymysql.Connection,
               cursor: pymysql.cursors.Cursor) -> int:
    """
    Adds movies to a playlist in the MySQL database, if it exists
    """
    status = playlist_utils.playlist_status(username, name, cursor)
    if status == 1:
        prev_movies = list(map(str, playlist_utils.get_movies(username, name, cursor)))
        final_movies = list(set(prev_movies + list(map(str, movies))))

        cursor.execute(
            f'update playlists set movies = "{"-".join(final_movies)}" where username = "{username}" and name = "{name}"')
        connection.commit()

    return status


def remove_movies(movies: list, username: str, name: str, connection: pymysql.Connection,
                  cursor: pymysql.cursors.Cursor) -> list | bool:
    """
    Removes movies from the MySQL database

    Returns the list of movies left in the playlist
    """
    prev_movies = playlist_utils.get_movies(username, name, cursor)
    movies = list(map(int, movies))

    if prev_movies:

        final_movies = [str(i) for i in prev_movies if i not in movies]

        cursor.execute(
            f'update playlists set movies = "{"-".join(final_movies)}" where username = "{username}" and name = "{name}"')
        connection.commit()

        return final_movies

    else:
        return False


def delete_playlist(username: str, name: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> bool:
    """
    Sends a playlist into its deletion period
    """
    cursor.execute(f'select * from playlists where username = "{username}" and name = "{name}"')
    data = cursor.fetchone()

    if data:

        cursor.execute(
            f'insert into deleted_playlists values("{data[0]}", "{data[2]}", "{data[3]}", "{data[4]}", "{data[5]}", curdate(), date_add(curdate(), interval 30 day))')
        cursor.execute(f'delete from playlists where username = "{username}" and name = "{name}"')

        connection.commit()

        return True

    else:
        return False


def remove_playlists(connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> tuple[tuple]:
    """
    Removes a playlist completely from the database

    Returns the data of the deleted playlists
    """
    cursor.execute(f'select username, name from deleted_playlists where curdate() > removal_date')
    data = cursor.fetchall()

    for i in data:
        cursor.execute(f'delete from deleted_playlists where username = "{i[0]}" and name = "{i[1]}"')
    connection.commit()

    return data


def recover_playlist(username: str, name: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> int:
    """
    Recovers a playlist in its deletion period
    """
    status = playlist_utils.playlist_status(username, name, cursor)
    if status == 2:
        cursor.execute(
            f'insert into playlists (select username, "user", name, movies, requires_password, password from deleted_playlists where username = "{username}" and name = "{name}")')
        cursor.execute(f'delete from deleted_playlists where username = "{username}" and name = "{name}"')
        connection.commit()

    return status
