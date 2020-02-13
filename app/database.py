import mysql.connector
from mysql.connector import errorcode


# Decorator for connecting to and disconnecting from the database
def database_operation(func):
    def inner(*args, **kwargs):
        error_message = None
        try:
            cnx = mysql.connector.connect(user='flask_server', password='password', host='127.0.0.1', database='ece1779')
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
        FROM account
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
            INSERT INTO account
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
        FROM account
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
        INSERT INTO photo
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
        FROM photo
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
        FROM photo
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
def delete_account_table(cnx):
    try:
        cnx.start_transaction()
        cursor = cnx.cursor()

        # Remove all accounts from table account
        delete_sql = """
        DELETE
        FROM account
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

        # Remove all accounts from table account
        get_sql = """
        SELECT *
        FROM account;
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
        FROM photo
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

        # Remove all accounts from table account
        get_sql = """
        SELECT *
        FROM photo;
        """
        cursor.execute(get_sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print('Unexpected exception: ' + str(e))
