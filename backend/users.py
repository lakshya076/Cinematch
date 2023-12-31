import pymysql
import pymysql.cursors
import pandas

import backend.encryption as encryption
import backend.Utils.user_utils as user_utils
import backend.mailing as mailing
import backend.playlists as playlists
import backend.Utils.playlist_utils as playlist_utils
import backend.mapping as mapping
import backend.collaborative_filtering as collab_filter


def register(username: str, password: str, email: str, liked: list, genres: list, langs: list,
             sim_table: pandas.DataFrame, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> bool:
    """
    Registers user in the database

    Returns `True` if successful
    Returns `False` if user already exists
    """

    hashed_password = encryption.sha256(password)
    del password

    name_status = user_utils.user_status(username, cursor)
    mail_status = user_utils.user_status(email, cursor)
    if name_status == mail_status == 0:

        liked = list(map(str, liked))
        recommended = list(map(str, collab_filter.recommend(liked, cursor, sim_table)))[:100]
        print(recommended)

        cursor.execute('update users set logged_in = 0')
        cursor.execute(f'insert into users values("{username}", "{hashed_password}", "{email}", 1, 0, null, null)')

        cursor.execute(f'insert into playlists values("{username}", "default", "Shortlist", "", 0, null, curdate())')
        cursor.execute(
            f'insert into mapping values("{username}", "{"-".join(liked)}", "", "{"-".join(liked)}", "{"-".join(genres)}", "{"-".join(langs)}", "{"-".join(recommended)}")')

        connection.commit()
        print("User Registered successfully")
        return True

    else:
        return name_status, mail_status


def login(username: str, password: str, cursor: pymysql.cursors.Cursor, connection: pymysql.Connection) -> bool:
    """
    Checks login credentials from the database
    Returns `True` only if credentials are correct
    """

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


def make_premium(username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> int:
    status = user_utils.user_status(username, cursor)

    if status == 1:
        cursor.execute(f'update users set premium = 1 where username = "{username}"')

    return status


def logout(cursor: pymysql.cursors.Cursor, connection: pymysql.Connection) -> None:
    cursor.execute('update users set logged_in = 0')
    connection.commit()


def update_password(email: str, new_pass: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> bool:
    hashed_password = encryption.sha256(new_pass)
    del new_pass

    if user_utils.user_status(email, cursor) == 1:

        cursor.execute(f'update users set password = "{hashed_password}" where email = "{email}"')
        connection.commit()
        return True

    else:
        return True


def delete_user(username: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> bool:
    cursor.execute(f'select * from users where username = "{username}"')
    data = cursor.fetchall()

    if data:

        data = data[0]
        if data[5] and data[6]:
            cursor.execute(
                f'insert into deleted_users values("{data[0]}", "{data[1]}", "{data[2]}", "{int(data[4])}", "{data[5]}, "{data[6]}",  curdate(), date_add(curdate(), interval 30 day))')
        else:
            cursor.execute(
                f'insert into deleted_users values("{data[0]}", "{data[1]}", "{data[2]}", "{int(data[4])}", null, null,  curdate(), date_add(curdate(), interval 30 day))')
        cursor.execute(f'delete from users where username = "{data[0]}"')
        connection.commit()

        for i in playlist_utils.get_playlists(username, cursor):
            playlists.delete_playlist(username, i, connection, cursor)

        mapping.delete_mapping(username, connection, cursor)

        mailing.send_deletion_mail(data[2], cursor)

        return True

    else:
        return False


def remove_users(connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> None:
    cursor.execute(f'select username, email from deleted_users where curdate() > removal_date')

    for i in cursor.fetchall():
        cursor.execute(f'delete from deleted_users where username = "{i[0]}"')
        mapping.remove_mapping(connection, cursor)
        playlists.remove_playlists(connection, cursor)
        mailing.send_removal_mail(i[0], i[1])
        print("User removed.")

    connection.commit()


def reminder_remove(connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    cursor.execute(f"select username, email from deleted_users where curdate() = removal_date")

    for i in cursor.fetchall():
        mailing.send_reminder_mail(i[0], i[1])
        print("Removal Reminder Email Sent.")

    connection.commit()


def recover_user(email: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor) -> bool:
    if user_utils.user_status(email, cursor) == 2:

        cursor.execute(
            f'insert into users (select username, password, email, premium, premium_start, premium_end from deleted_users where email="{email}")')
        cursor.execute(f'delete from deleted_users where email="{email}"')
        connection.commit()

        return True

    else:
        return False
