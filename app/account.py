import hashlib
import random
import struct

from flask import g, redirect, render_template, request, session, url_for, abort

from app import main, webapp, database


@webapp.route('/api/account_actions', methods=['POST'])
# Web handler for account actions
def account_actions_handler():
    # Get requests
    account_action_type = request.form.get('action')
    username = request.form.get('username')
    password = request.form.get('password')
    rememberme = (request.form.get('rememberme') == 'True')

    if account_action_type == 'login':
        err_msg = account_login(username, password, rememberme)
    else:
        assert(account_action_type == 'register')
        err_msg = account_register(username, password, rememberme)

    if err_msg:
        return main.main(guest_welcome_args=main.GuestWelcomeArgs(username=username, password=password, error_message=err_msg))
    else:
        return redirect('/')


@webapp.route('/api/register', methods=['POST'])
# API handler for account register
def account_register_handler():
    # Get requests
    # NOT TESTED YET!
    username = request.form.get('username')
    password = request.form.get('password')

    err_msg = account_register(username, password)

    if err_msg:
        abort(406)
    else:
        return redirect('/')


@webapp.route('/api/logout', methods=['POST'])
# Web handler for logout
def account_logout_handler():
    account_logout()
    return redirect('/')


def account_is_logged_in():
    return session.get('username') is not None and session.get('userid') is not None


def account_get_logged_in_username():
    assert(account_is_logged_in())
    return session['username']


def account_get_logged_in_userid():
    assert(account_is_logged_in())
    return session['userid']


def account_register(username, password, rememberme=False):
    '''
    if successful, None; else, error message
    '''
    print('Registering: u=' + username + ' p=' + password)

    if account_is_logged_in():
        account_logout()
    
    # Validate input (format)
    if not username:
        return 'Error! Username is not valid!'
    if not password:
        return 'Error! Password is not valid!'
    
    USERNAME_MAX_LENGTH = 100
    if len(username) > USERNAME_MAX_LENGTH:
        return 'Error! "' + username + '" exceeds ' + str(USERNAME_MAX_LENGTH) + ' characters!'

    # Register the user (business)
    salt = bytes(random.getrandbits(8) for _ in range(4)).hex()
    encrypted_password = account_hash_password(password, salt)
    error_message = database.create_new_account(username, encrypted_password, salt)
    if error_message:
        return error_message
    print('    Successful!')

    # Login the user (business)
    login_result = account_login(username, password, rememberme)

    return login_result


def account_login(username, password, rememberme=False):
    '''
    if successful, None; else, error message
    '''
    if account_is_logged_in():
        account_logout()

    print('Login: u=' + username + ' p=' + password + ' rememberme=' + str(rememberme))

    # Validate input (business)
    userid = account_verify_password(username, password)
    if userid is None:
        return 'Error! Username or Password is not correct!'

    # Create a session (business)
    assert(not account_is_logged_in())
    session['username'] = username
    session['userid'] = userid
    session.permanent = rememberme
    print('    Successful!')


def account_logout():
    if account_is_logged_in():
        # Clear the session (business)
        username = account_get_logged_in_username()
        print('Logout: u=' + username)
        session.pop('username')
        session.clear()
        print('    Successful!')
    else:
        print('Already logged out!')


def account_verify_password(username, password):
    '''
    Return userid if successful; otherwise None
    '''
    result = database.get_account_credential(username)
    if result:
        account_id, encrypted_password, salt = result
        if account_hash_password(password, salt) == encrypted_password:
            return account_id
    return None


def account_hash_password(password, salt):
    '''
    password must be a str type
    salt must be a char[8]
    encrypted_password is a char[64]
    '''

    password_salt_bytearray = bytearray()
    password_salt_bytearray.extend(str(password).encode())
    password_salt_bytearray.extend(bytes.fromhex(salt))

    encrypted_password = hashlib.sha256(password_salt_bytearray).hexdigest()
    return encrypted_password
