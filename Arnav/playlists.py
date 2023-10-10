import Utils.playlist_utils as playlist_utils
import encryption
import pymysql, pymysql.cursors

def create_playlist(username: str, name: str, movies: str, password: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if not playlist_utils.playlist_status(username, name, connection, cursor):

        req_pass = int(bool(password))
        hashed_pass = ''
        if req_pass:
            hashed_pass = encryption.sha256(password)
            del password

        cursor.execute(f'insert into playlists values("{username}", "user", "{name}", "{movies}", {req_pass}, {hashed_pass})')

        return True
    
    else:

        return False