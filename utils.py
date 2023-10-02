import pymysql
import pymysql.cursors

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


    cursor.execute(f'select recommended from recommendations where id={id}')
    x = cursor.fetchall()

    if x:    
        return cursor.fetchall()[0][0].split('-')
    else:
        return []


def get_genz(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return genres of a movie in a list, given its `id`
    
    '''

    cursor.execute(f'select genres from recommendations where id={id}')
    x = cursor.fetchall()

    if x:
        return cursor.fetchall()[0][0].split('-')
    else:
        return []


def get_keyz(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return keywords of a movie in a list, given its `id`
    
    '''

    cursor.execute(f'select keywords from recommendations where id={id}')
    x = cursor.fetchall()

    if x:
        return cursor.fetchall()[0][0].split('-')
    else:
        return []


def get_pop(id: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Return popularity of a movie, given its `id`
    
    '''


    cursor.execute(f'select popularity from recommendations where id={id}')
    x = cursor.fetchall()

    if x:
        return float(cursor.fetchall()[0][0])
    else:
        return 1.86 # Avg


def recommend_direct(id: int, depth: int, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Searches for recommendations of a movie using the given recommendations till `depth`
    
    '''

    og_recs = get_recs(id, connection, cursor)

    popsorted = pop_sort(og_recs, connection, cursor)

    recommendations = popsorted

    if depth == 1:
        return recommendations

    for i in popsorted[:]:
        recommendations += recommend_direct(i, depth-1, connection, cursor)

    return list(set(recommendations))


def pop_sort(ids: list, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Sort given movies by popularity
    
    '''

    pop_dict = {}

    for i in ids:

        popularity = get_pop(i, connection, cursor)
        pop_dict[popularity] = i

    pop_list = list(pop_dict.keys())
    pop_list.sort(reverse=True)
    ids_sorted = []

    for i in pop_list:
        ids_sorted.append(pop_dict[i])

    return ids_sorted


def search(phrase: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    
    '''
    
    search for movies using `phrase`
    
    '''

    title_search = []
    keyword_search = []
    overview_search = []

    cursor.execute(f'select id from main where overview like "%{phrase}%"')
    overview_search.extend([int(i[0]) for i in cursor.fetchall()])

    cursor.execute(f'select id from main where title like "%{phrase}%" or genres like "%{phrase}%"')
    title_search.extend([int(i[0]) for i in cursor.fetchall()])

    cursor.execute(f'select id from recommendations where keywords like "%{phrase}%"')
    keyword_search.extend([int(i[0]) for i in cursor.fetchall()])

    combined_search = title_search + overview_search + keyword_search
    combined_search = set(combined_search)
    combined_search = pop_sort(list(combined_search), connection, cursor)

    return combined_search
