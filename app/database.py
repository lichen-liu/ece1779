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
        finally:
            cnx.close()
            return error_message
    return inner


@database_operation
def create_new_account(cnx, username, password_hash, salt):
    '''
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
            cnx.abort()

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
        print(err)
        error_message = str(err)
        cnx.abort()
    finally:
        return error_message


@database_operation
def get_account_credential(cnx, username):
    '''
    Return (password_hash, salt) if successful; otherwise None
    '''
    result = None
    try:
        cursor = cnx.cursor()

        # Check whether the username has already been registered
        get_sql = """
        SELECT password_hash, salt
        FROM account
        WHERE username = %s;
        """
        get_val = (username,)
        cursor.execute(get_sql, get_val)
        get_results = cursor.fetchall()
        if get_results:
            result = (get_results[0][0], get_results[0][1])
    except mysql.connector.Error as err:
        print(err)
    finally:
        return result


# Testing
print('res = ' + repr(create_new_account('yonghu', b'12345678901234567890123456789012', b'abcd')))
print('res = ' + repr(create_new_account('yonghu1', b'12345678901234567890123456789012', b'abcd')))
print('res = ' + repr(create_new_account('yonghu2', b'12345678901234567890123456789012', b'abcd')))
print('res = ' + repr(create_new_account('yonghu3', b'12345678901234567890123456789012', b'abcd')))
print('res = ' + repr(create_new_account('yonghu4', b'12345678901234567890123456789012', b'abcd')))
print('get = ' + repr(get_account_credential('yonghu5')))