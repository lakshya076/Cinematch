import pymysql
import pymysql.cursors
from validate_email import validate_email



def user_status(user: str, cursor: pymysql.cursors.Cursor):
    '''
    
    Returns `True` if username/email exists in the database, else returns `False`
    
    '''

    cursor.execute(f'select email from users where email="{user}" or username="{user}"')
    x = cursor.fetchall()

    cursor.execute(f'select email from deleted_users where email="{user}" or username="{user}"')
    y = cursor.fetchall()

    if x:
        return 1

    elif y:
        return 2

    else:
        return 0


def valid_email(email: str):
    '''
    
    Return `True` or `False` depending if the email is valid.
    
    '''

    return validate_email(email, check_format=True, check_blacklist=False, check_dns=False, check_smtp=False,
                          dns_timeout=0, smtp_timeout=0)


def get_email(username: str, cursor: pymysql.cursors.Cursor):
    '''
    
    Returns the email of a user, given the username

    Returns `False` if user doesn't exist
    
    '''

    cursor.execute(f'select email from users where email="{username}"')
    data = cursor.fetchone()

    if data:
        return data[0]

    else:
        return False


def get_username(email: str, cursor: pymysql.cursors.Cursor):
    '''
    
    Returns the username of a user, given the email

    Returns `False` if user doesn't exist
    
    '''

    cursor.execute(f'select username from users where email="{email}"')
    data = cursor.fetchone()

    if data:
        return data[0]

    else:
        return False


def get_password(user: str, cursor: pymysql.cursors.Cursor):
    '''
    
    Returns the hashed password of a user, given its username or email

    Returns `False` if user doesn't exist
    
    '''

    cursor.execute(f'select password from users where email="{user}" or username="{user}"')
    data = cursor.fetchone()

    if data:
        return data[0]

    else:
        return False


def get_logged_user(cursor: pymysql.cursors.Cursor):
    cursor.execute('select username from users where logged_in = 1')
    data = cursor.fetchall()

    if data:
        return data[0][0]

    else:
        return False


def is_logged_in(user: str, cursor: pymysql.cursors.Cursor):
    cursor.execute(f'select logged_in from users where username="{user}" or email="{user}"')
    data = cursor.fetchone()

    if data:
        return bool(int(data[0]))

    else:
        return False


def is_premium(user: str, cursor: pymysql.cursors.Cursor):
    '''
    
    Returns `True` if user is premium, else returns `False`

    '''

    cursor.execute(f'select premium from users where username="{user}" or email="{user}"')
    data = cursor.fetchall()

    if data:
        return bool(int(data[0][0]))

    else:
        return None
