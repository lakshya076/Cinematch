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
    data = cursor.fetchall()

    if data:

        if data[0][0] == '':
            return []
        else:
            return list(map(int, data[0][0].split('-')))

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


def get_type(username: str, name: str, cursor: pymysql.cursors.Cursor):
    
    cursor.execute(f'select type from playlists where username = "{username}" and name = "{name}"')
    data = cursor.fetchall()

    if data:
        return data[0][0]

    else:
        return False


def get_type(username: str, name: str, cursor: pymysql.cursors.Cursor):
    
    cursor.execute(f'select date from playlists where username = "{username}" and name = "{name}"')
    data = cursor.fetchall()

    if data:
        return '-'.join(data[0][0].split('-')[::-1])

    else:
        return False


def get_playlists(username: str, cursor: pymysql.cursors.Cursor):
    
    cursor.execute(f'select name from playlists where username = "{username}"')
    data = cursor.fetchall()

    return [i[0] for i in data]


def get_playlists_info(username: str, cursor: pymysql.cursors.Cursor):

    '''
    
    (username, type, name, movies, requires_password, password, date_created)

    '''

    cursor.execute(f'select * from playlists where username = "{username}"')
    data = cursor.fetchall()

    if data:

        result = []
        for i in data:
            
            if i[3] == '':
                result.append([i[0], i[1], i[2], [], bool(int(i[4])), i[5], str(i[6])])
            
            else:
                result.append([i[0], i[1], i[2], list(map(int, i[3].split('-'))), bool(int(i[4])), i[5], str(i[6])])

        return result

    else:
        return False


def playlist_info(username: str, name: str, cursor: pymysql.cursors.Cursor):
    
    '''
    
    0 username
    1 type
    2 name 
    3 movies
    4 requires_password 
    5 password 

    '''

    cursor.execute(f'select * from playlists where name = "{name}" and username = "{username}"')
    data = cursor.fetchall()

    if data:

        final_list = [data[0][0], data[0][1], data[0][2], data[0][3], bool(int(data[0][4])), data[0][5],
                      str(data[0][6])]

        if final_list[3] == '':
            final_list[3] = []

        else:
            final_list[3] = list(map(int, final_list[3].split('-')))

        return final_list

    else:
        return None
