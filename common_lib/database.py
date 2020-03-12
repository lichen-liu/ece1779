import mysql.connector
from mysql.connector import errorcode
import os
import pathlib


_MYSQL_HOST = 'ece1779-db.caxvvqofsqfz.us-east-1.rds.amazonaws.com'
_MYSQL_PORT = 3306
_MYSQL_USERNAME = 'admin'
_MYSQL_PASSWORD = 'ece1779ins!'
_MYSQL_SCHEMA_FILE = os.path.join(pathlib.Path(__file__).parent.absolute(), 'schema.sql')


# Decorator for connecting to and disconnecting from the database
def database_operation(func):
    def inner(*args, **kwargs):
        error_message = None
        try:
            cnx = mysql.connector.connect(
                user=_MYSQL_USERNAME,
                password=_MYSQL_PASSWORD,
                host=_MYSQL_HOST,
                port=_MYSQL_PORT)
            if cnx:
                error_message = func(cnx, *args, **kwargs)
        except mysql.connector.Error as err:
            print(err)
            error_message = str(err)
        except Exception as e:
            print('Unexpected exception: ' + str(e))
        finally:
            cnx.close()
            return error_message
    return inner


@database_operation
def create_new_account(cnx, username, password_hash, salt):
    '''
    salt must be a char[8]
    password_hash must be a char[64]
    Return error_message if errored; otherwise None
    '''
    error_message = None
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Check whether the username has already been registered
        check_sql = """
        SELECT COUNT(1)
        FROM ece1779.account
        WHERE username = %s;
        """
        check_val = (username,)
        cursor.execute(check_sql, check_val)
        check_results = cursor.fetchall()
        if check_results and check_results[0][0] == 1:
            error_message = 'Error! ' + username + ' is already registered!'
            cnx.rollback()

        if error_message is None:
            # Create the new account in the database
            insert_sql = """
            INSERT INTO ece1779.account
            (username, password_hash, salt)
            VALUES (%s, %s, %s);
            """
            insert_val = (username, password_hash, salt)
            cursor.execute(insert_sql, insert_val)
            cnx.commit()
    except mysql.connector.Error as err:
        # Handle duplicated inserts
        print(err)
        error_message = str(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))
    finally:
        return error_message


@database_operation
def get_account_credential(cnx, username):
    '''
    Return (account_id, password_hash, salt) if successful; otherwise None
    '''
    result = None
    try:
        cursor = cnx.cursor()

        # Check whether the username has already been registered
        get_sql = """
        SELECT id, password_hash, salt
        FROM ece1779.account
        WHERE username = %s;
        """
        get_val = (username,)
        cursor.execute(get_sql, get_val)
        get_results = cursor.fetchall()
        if get_results:
            result = (get_results[0][0], get_results[0][1], get_results[0][2])
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))
    finally:
        return result


@database_operation
def create_new_photo(cnx, account_id, filename):
    '''
    Return photo_id if successful; otherwise None
    '''
    result = None
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Create the new photo in the database
        insert_sql = """
        INSERT INTO ece1779.photo
        (account_id, name)
        VALUES (%s, %s);
        """
        insert_val = (account_id, filename)
        cursor.execute(insert_sql, insert_val)
        result = cursor.lastrowid
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))
    finally:
        return result


@database_operation
def get_account_photo(cnx, account_id):
    '''
    Return [(photo_id, photo_name)] if successful; otherwise None
    '''
    result = None
    try:
        cursor = cnx.cursor()

        # Check whether the username has already been registered
        get_sql = """
        SELECT id, name
        FROM ece1779.photo
        WHERE account_id = %s;
        """
        get_val = (account_id,)
        cursor.execute(get_sql, get_val)
        get_results = cursor.fetchall()
        if get_results:
            result = list()
        for get_result in get_results:
            result.append(get_result[0:2])
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))
    finally:
        return result


@database_operation
def get_photo(cnx, photo_id):
    '''
    Return (user_id, photo_name) if successful; otherwise None
    '''
    result = None
    try:
        cursor = cnx.cursor()

        # Check whether the username has already been registered
        get_sql = """
        SELECT account_id, name
        FROM ece1779.photo
        WHERE id = %s;
        """
        get_val = (photo_id,)
        cursor.execute(get_sql, get_val)
        get_results = cursor.fetchall()
        if get_results:
            result = get_results[0]
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))
    finally:
        return result


@database_operation
def delete_photo(cnx, photo_id):
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Remove photo from table photo
        delete_sql = """
        DELETE
        FROM ece1779.photo
        WHERE id = %s;
        """
        delete_val = (photo_id,)
        cursor.execute(delete_sql, delete_val)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def delete_account_table(cnx):
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Remove all accounts from table account
        delete_sql = """
        DELETE
        FROM ece1779.account
        WHERE id <> '-1';
        """
        cursor.execute(delete_sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def get_account_table(cnx):
    try:
        cursor = cnx.cursor()

        # Get all accounts from table account
        get_sql = """
        SELECT *
        FROM ece1779.account;
        """
        cursor.execute(get_sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def delete_photo_table(cnx):
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Remove all photos from table photo
        delete_sql = """
        DELETE
        FROM ece1779.photo
        WHERE id <> '-1';
        """
        cursor.execute(delete_sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def get_photo_table(cnx):
    try:
        cursor = cnx.cursor()

        # Get all photos from table photo
        get_sql = """
        SELECT *
        FROM ece1779.photo;
        """
        cursor.execute(get_sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def drop_schema(cnx):
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Drop the schema
        drop_sql = """
        DROP SCHEMA IF EXISTS ece1779;
        """
        cursor.execute(drop_sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def is_schema_existed(cnx):
    try:
        cursor = cnx.cursor()

        # Check whether schema exists
        get_sql = """
        SELECT SCHEMA_NAME
        FROM INFORMATION_SCHEMA.SCHEMATA
        WHERE SCHEMA_NAME = 'ece1779'
        """
        cursor.execute(get_sql)
        result = cursor.fetchall()
        assert(len(result) <= 1)
        return len(result) == 1
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))


@database_operation
def create_schema(cnx):
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Create the schema
        stmts = parse_sql(_MYSQL_SCHEMA_FILE)
        for stmt in stmts:
            cursor.execute(stmt)
        cnx.commit()
    except mysql.connector.Error as err:
        print(err)
        cnx.rollback()
    except Exception as e:
        print('Unexpected exception: ' + str(e))


def parse_sql(sql_file_path):
    '''
    Parse .sql file into sql statements
    https://python-forum.io/Thread-Execute-sql-file-in-python
    '''
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    stmt = ''
    stmts = []
    for line in data:
        if line:
            if line.startswith('--'):
                continue
            stmt += line.strip() + ' '
            if ';' in stmt:
                stmts.append(stmt.strip())
                stmt = ''
    return stmts


def create_schema_if_necessary():
    if not is_schema_existed():
        create_schema()
        return True
    return False