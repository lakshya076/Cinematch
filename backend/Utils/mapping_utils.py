import pymysql.cursors


def mapping_status(username: str, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select email from mapping where username="{username}"')
    x = cursor.fetchall()

    cursor.execute(f'select email from deleted_mapping where username="{username}"')
    y = cursor.fetchall()

    if x:
        return 1

    elif y:
        return 2

    else:
        return 0


def get_mapping_data(username: str, cursor: pymysql.cursors.Cursor):

    cursor.execute(f'select * from mapping where username = "{username}"')
    data = cursor.fetchall()

    if data:
        data = data[0]
        result = [data[0]]

        for i in data[1:4]:
            if i:
                result.append(list(map(int, i.split('-'))))
            else:
                result.append([])

        for i in data[4:6]:
            if i:
                result.append(i.split())
            else:
                result.append([])
        
        if data[6]:
            result.append(list(map(int, data[6].split('-'))))
        else:
            result.append([])

        return result
    
    else:
        return []
    

def get_language_movies(username: str, limit: int, cursor: pymysql.cursors.Cursor):


    cursor.execute(f'select id from main where release_date <= curdate() and (select languages from mapping where mapping.username = "{username}") like concat("%", main.language, "%") order by release_date desc limit {limit}')
    data = cursor.fetchall()

    return [int(i[0]) for i in data]
