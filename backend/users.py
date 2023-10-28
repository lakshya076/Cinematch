import pymysql, pymysql.cursors
import backend.encryption as encryption
import backend.Utils.user_utils as user_utils
import backend.mailing as mailing
import backend.playlists as playlists
import backend.Utils.playlist_utils as playlist_utils


def register(username: str, password: str, email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    '''
    
    Registers user in the database

    Returns `True` if successful

    Returns `False` if user already exists
    
    '''

    hashed_password = encryption.sha256(password)
    del password

    cursor.execute(f'select username from users where username="{username}"')
    data = cursor.fetchall()

    cursor.execute(f'select * from users where email="{email}"')
    data2 = cursor.fetchall()

    if data == () and data2 == ():

        cursor.execute('update users set logged_in = 0')

        cursor.execute(f'insert into users values("{username}", "{hashed_password}", "{email}", 1, 0, null, null)')
        cursor.execute(f'insert into playlists values("{username}", "default", "Watching", "", 0, null, curdate())')
        cursor.execute(f'insert into playlists values("{username}", "default", "Watched", "", 0, null, curdate())')
        cursor.execute(f'insert into playlists values("{username}", "default", "Plan to Watch", "", 0, null, curdate())')
        cursor.execute(f'insert into playlists values("{username}", "default", "Shortlist", "", 0, null, curdate())')
        # cursor.execute(f'insert into mapping values("{username}", "", "", "", "", "", "")')


        connection.commit()

        return True

    else:

        return False


def login(username: str, password: str, cursor: pymysql.cursors.Cursor, connection: pymysql.Connection):
    '''
    
    Checks login credentials from the database

    Returns `True` only if credentials are correct
    
    '''

    hashed_password = encryption.sha256(password)
    del password

    cursor.execute(f'select username, password from users where username="{username}"')
    data = cursor.fetchall()

    if data:

        if username == data[0][0] and hashed_password == data[0][1]:

            cursor.execute(f'update users set logged_in = 0')
            cursor.execute(f'update users set logged_in = 1 where username = "{username}"')
            connection.commit()

            return True

        else:
            return False

    else:
        return False


def logout(cursor: pymysql.cursors.Cursor, connection: pymysql.Connection):
    cursor.execute('update users set logged_in = 0')
    connection.commit()


def forgot_password(email: str, cursor: pymysql.cursors.Cursor):
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


def update_password(email: str, new_pass: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    hashed_password = encryption.sha256(new_pass)
    del new_pass

    if user_utils.user_status(email, cursor) == 1:

        cursor.execute(f'update users set password = "{hashed_password}" where email = "{email}"')
        connection.commit()

        return True

    else:

        return True


def delete_user(username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    cursor.execute(f'select * from users where username = "{username}"')
    data = cursor.fetchone()

    if data:

        cursor.execute(
            f'insert into deleted_users values("{data[0]}", "{data[1]}", "{data[2]}", {int(data[3])}, "{data[4]}", "{data[5]}", curdate(), date_add(curdate(), interval 30 day))')
        cursor.execute(f'delete from users where username = "{username}"')
        connection.commit()

        for i in playlist_utils.get_playlists(username, cursor):
            playlists.delete_playlist(username, i, connection, cursor)

        mailing.send_deletion_mail(data[2], cursor)

        return True

    else:

        return False


def remove_users(connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    cursor.execute(f'select username, email from deleted_users where curdate() > removal_date')

    for i in cursor.fetchall():
        cursor.execute(f'delete from deleted_users where username = "{i[0]}"')
        mailing.send_removal_mail(i[1], cursor)

    connection.commit()


def recover_user(email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    if user_utils.user_status(email, cursor) == 2:

        cursor.execute(f'insert into users (select username, password, email, premium, premium_start, premium_end from deleted_users where email="{email}")')
        cursor.execute(f'delete from deleted_users where email="{email}"')
        connection.commit()

        return True

    else:
        return False
