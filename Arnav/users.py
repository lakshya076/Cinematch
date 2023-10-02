import pymysql, pymysql.cursors
import encryption
import otp


def register(uname: str, passwd: str, email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):


    '''
    
    Registers user in the database

    Returns `True` if successful

    Returns `False` if user already exists
    
    '''

    cursor.execute(f'select username from users where username="{uname}"')
    data = cursor.fetchall()

    cursor.execute(f'select * from users where email="{email}"')
    data2 = cursor.fetchall()

    if data == () and data2 == ():

        hashed_pass = encryption.sha256(passwd)
        cursor.execute(f'insert into users(username, password, email) values("{uname}", "{hashed_pass}", "{email}")')

        connection.commit()

        return True

    else:

        return False


def login(uname: str, passwd: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):


    '''
    
    Checks login credentials from the database

    Returns `True` only if credentials are correct
    
    '''

    cursor.execute(f'select * from users where username="{uname}"')

    if cursor.fetchall() == ():

        return False

    else:

        data = cursor.fetchall()[0]

        if uname == data[0] and encryption.sha256(passwd) == data[1]:
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

        return otp.send_otp(data[0][4])
