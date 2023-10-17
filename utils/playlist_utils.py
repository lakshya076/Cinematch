import pymysql
import pymysql.cursors

def playlist_status(username: str, name: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select * from playlists where username="{username}" and name="{name}"')
    x = cursor.fetchall()

    cursor.execute(f'select * from deleted_playlists where username="{username}" and name="{name}"')
    y = cursor.fetchall()

    if x:
        return 1
    elif y:
        return 2
    else:
        return 0
    

def requires_password(username: str, name: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if playlist_status(username, name, connection, cursor) == 1:

        cursor.execute(f'select requires_password from playlists where username="{username}" and name="{name}"')
        return int(cursor.fetchone()[0])
    
    else:

        return -1
