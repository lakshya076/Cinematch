import pymysql
import pymysql.cursors

def playlist_status(username: str, name: str, cursor: pymysql.cursors.Cursor):

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
    

def requires_password(username: str, name: str, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select requires_password from playlists where username="{username}" and name="{name}"')
    data = cursor.fetchone()

    if data:
        return bool(int(data[0]))
    
    else:
        return -1
    
def get_movies(username: str, name: str, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select movies from playlists where username="{username}" and name="{name}"')
    data = cursor.fetchall()[0]

    if data:
        return str(data[0]).split('-')
    
    else:
        return []
    

def get_password(username: str, name: str, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select password from playlists where username = "{username}" and name = "{name}"')
    from_normal = cursor.fetchone()

    cursor.execute(f'select password from deleted_playlists where username = "{username}" and name = "{name}"')
    from_deleted = cursor.fetchone()

    if from_normal:
        return from_normal[0]

    elif from_deleted:
        return from_deleted[0]

    else:
        return False