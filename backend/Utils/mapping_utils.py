import pymysql, pymysql.cursors


def get_liked_movies(username: str, cursor: pymysql.cursors.Cursor) -> list | bool:

    cursor.execute(f'select liked_movies from mapping where username = "{username}"')
    data = cursor.fetchall()

    if data:

        result = data[0][0]
        if result:
            return []
        else:
            return result.split('-')
    
    else:
        return False
    

