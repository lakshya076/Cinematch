import pymysql
import pymysql.cursors
from validate_email import validate_email


def movie_exists(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select * from main where id={id}')

    if cursor.fetchall():
        return True
    else:
        return False


def get_title(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return `title` of a movie, given its `id`

    Returns `False` if movie not found
    
    '''

    cursor.execute(f'select title from main where id={id}')

    x = cursor.fetchall()

    if x:
        return x[0][0]
    else:
        return False


def get_recs(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Returns recommended movies of a movie in a list, given its `id`
    
    '''

    if movie_exists(id, connection, cursor):
        cursor.execute(f'select recommended from recommendation where id={id}')
        return cursor.fetchall()[0][0].split('-')
    else:
        return []


def get_genz(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return genres of a movie in a list, given its `id`
    
    '''

    cursor.execute(f'select genres from recommendation where id={id}')
    x = cursor.fetchall()

    if x:
        return x[0][0].split('-')
    else:
        return []


def get_keyz(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return keywords of a movie in a list, given its `id`
    
    '''

    cursor.execute(f'select keywords from recommendation where id={id}')

    if movie_exists(id, connection, cursor):
        return cursor.fetchall()[0][0].split('-')
    else:
        return []


def get_popularity(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return popularity of a movie, given its `id`
    
    '''


    if movie_exists(id, connection, cursor):
        cursor.execute(f'select popularity from recommendation where id={id}')
        return cursor.fetchall()[0][0]
    else:
        return 1.86 # Avg


def get_overview(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if movie_exists(id, connection, cursor):
        cursor.execute(f'select overview from main where id="{id}"')
        return cursor.fetchall()[0][0]
    else:
        return False


def get_release_date(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if movie_exists(id, connection, cursor):
        
        cursor.execute(f'get release_date from main where id={id}')
        return cursor.fetchall()[0][0]
    
    else:

        return False


def recommend_direct(id: int, depth: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Searches for recommendation of a movie using the given recommendation till `depth`
    
    '''

    if movie_exists(id, connection, cursor):

        og_recs = get_recs(id, connection, cursor)

        popsorted = pop_sort(og_recs, connection, cursor)

        recommendation = popsorted

        if depth == 1:
            return recommendation

        for i in popsorted[:]:
            recommendation += recommend_direct(i, depth-1, connection, cursor)

        return list(set(recommendation))
    
    else:

        return []


def pop_sort(ids: list, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Sort given movies by popularity
    
    '''

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


def valid_email(email: str):

    return validate_email(email)


def user_exists(user: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select email from users where email="{user}" or username="{user}"')

    x = cursor.fetchall()

    return bool(len(x))


def get_email(uname: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select email from users where username="{uname}"')
    x = cursor.fetchall()

    if x:
        return x[0][0]
    else:
        return False
    

def get_username(email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select email from users where email="{email}"')
    x = cursor.fetchall()

    if x:
        return x[0][0]
    else:
        return False

    
def get_password(user: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select password from users where email="{user}" or username="{user}"')
    x = cursor.fetchall()

    if x:
        return x[0][0]
    else:
        return False
    

def is_premium(user: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if user_exists(user, connection, cursor):

        cursor.execute(f'select * from users where username="{user}" or email="{user}"')
        return bool(cursor.fetchall()[0][0])

    else:
        return False


