import pymysql
import pymysql.cursors
from validate_email import validate_email


def valid_email(email: str):

    '''
    
    Return `True` or `False` depending if the email address exists or/and can be delivered.

    Return `None` if the result is ambiguous.
    
    '''

    return validate_email(email)


def user_exists(user: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Returns `True` if username/email exists in the database, else returns `False`
    
    '''

    cursor.execute(f'select email from users where email="{user}" or username="{user}"')

    x = cursor.fetchall()

    return bool(len(x))


def get_email(uname: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Returns the email of a user, given the username

    Returns `False` if user doesn't exist
    
    '''

    cursor.execute(f'select email from users where username="{uname}"')
    x = cursor.fetchall()

    if x:
        return x[0][0]
    else:
        return False
    

def get_username(email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Returns the username of a user, given the email

    Returns `False` if user doesn't exist
    
    '''

    if user_exists(email, connection, cursor):

        cursor.execute(f'select email from users where email="{email}"')
        return cursor.fetchall()[0][0]
    
    else:

        return False

    
def get_password(user: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Returns the hashed password of a user, given its username or email

    Returns `False` if user doesn't exist
    
    '''

    if user_exists(user, connection, ):

        cursor.execute(f'select password from users where email="{user}" or username="{user}"')
        return cursor.fetchall()[0][0]
    
    else:

        return False
    

def is_premium(user: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Returns `True` if user is premium, else returns `False`

    '''

    if user_exists(user, connection, cursor):

        cursor.execute(f'select * from users where username="{user}" or email="{user}"')
        return bool(cursor.fetchall()[0][0])

    else:

        return False