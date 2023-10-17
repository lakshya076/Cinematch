import pymysql, pymysql.cursors
import encryption
import utils.user_utils as user_utils


def register(username: str, passwd: str, email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):


    '''
    
    Registers user in the database

    Returns `True` if successful

    Returns `False` if user already exists
    
    '''

    cursor.execute(f'select username from users where username="{username}"')
    data = cursor.fetchall()

    cursor.execute(f'select * from users where email="{email}"')
    data2 = cursor.fetchall()

    if data == () and data2 == ():

        hashed_pass = encryption.sha256(passwd)
        cursor.execute(f'insert into users values("{username}", "{hashed_pass}", "{email}", 0, null, null)')
        del passwd

        cursor.execute(f'insert into playlists values("{username}", "default", "Watching", "", 0, null)')
        cursor.execute(f'insert into playlists values("{username}", "default", "Watched", "", 0, null)')
        cursor.execute(f'insert into playlists values("{username}", "default", "Plan to Watch", "", 0, null)')

        connection.commit()

        return True

    else:

        return False


def login(username: str, passwd: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):


    '''
    
    Checks login credentials from the database

    Returns `True` only if credentials are correct
    
    '''


    if not user_utils.user_exists(username, connection, cursor) == ():

        return False

    else:

        cursor.execute(f'select username, password from users where username="{username}"')
        data = cursor.fetchall()[0]

        if username == data[0] and encryption.sha256(passwd) == data[1]:
            del passwd
            return True
        
        else:
            return False


def forgot_passwd(email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    '''
    
    Sends `otp` to `email` for password recovery

    returns `otp` if `email` exists in DB and can be sent to.

    else returns `-1`
    
    '''

    cursor.execute(f'select * from users where email="{email}"')
    data = cursor.fetchall()

    if data == ():
        return -1
    
    else:

        return email.send_otp(data[0][4])


def update_passwd(email: str, new_pass: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if user_utils.user_exists(email, connection, cursor):
    
        cursor.execute(f'update users set password="{encryption.sha256(new_pass)}" where email="{email}"')
        del new_pass
        connection.commit()

        return True
    
    else:

        return True


def delete_user(username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):

    if user_utils.user_exists(username, connection, cursor):
        
        cursor.execute(f'delete from users where username="{username}"')
        connection.commit()

        return True
    
    else:

        return False
