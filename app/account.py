import hashlib
import random
import struct

from flask import g, redirect, render_template, request, session, url_for

from app import main, webapp


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
        return main.main_guest_welcome(username, password, err_msg)
    else:
        return redirect('/')


@webapp.route('/api/register', methods=['POST'])
# API handler for account register
def account_register_handler():
    # Get requests
    username = request.form.get('username')
    password = request.form.get('password')

    err_msg = account_register(username, password)

    if err_msg:
        return main.main_guest_welcome(username, password, err_msg)
    else:
        return redirect('/')


@webapp.route('/api/logout', methods=['GET'])
# Web handler for logout
def account_logout_handler():
    account_logout()
    return redirect('/')


def account_is_logged_in():
    return session.get('username') is not None


def account_get_logged_in_user():
    assert(account_is_logged_in())
    return session['username']


def account_register(username, password, rememberme=False):
    '''
    if successful, None; else error message
    '''
    print('Registering: u=' + username + ' p=' + password)

    if account_is_logged_in():
        account_logout()
    
    # Validate input (format)
    if not username:
        return 'Error! Username is not valid!'
    if not password:
        return 'Error! Password is not valid!'

    # Validate input (business)
    if username in accounts:
        return 'Error! ' + username + ' is already registered!'
    
    USERNAME_MAX_LENGTH = 100
    if len(username) > USERNAME_MAX_LENGTH:
        return 'Error! "' + username + '" exceeds ' + str(USERNAME_MAX_LENGTH) + ' characters!'

    # Register the user (business)
    salt = random.random()
    encrypted_password = account_hash_password(password, salt)
    accounts[username] = (encrypted_password, salt)
    print('    Successful!')

    # Login the user (business)
    login_result = account_login(username, password, rememberme)

    return login_result


def account_login(username, password, rememberme=False):
    '''
    if successful, None; else error message
    '''
    if account_is_logged_in():
        account_logout()

    print('Login: u=' + username + ' p=' + password + ' rememberme=' + str(rememberme))

    # Validate input (business)
    if accounts.get(username) is None or not account_verify_password(username, password):
        return 'Error! Username or Password is not correct!'

    # Create a session (business)
    assert(not account_is_logged_in())
    session['username'] = username
    session.permanent = rememberme
    print('    Successful!')


def account_logout():
    if account_is_logged_in():
        # Clear the session (business)
        username = account_get_logged_in_user()
        print('Logout: u=' + username)
        session.pop('username')
        session.clear()
        print('    Successful!')
    else:
        print('Already logged out!')


def account_verify_password(username, password):
    encrypted_password, salt = accounts[username]
    return account_hash_password(password, salt) == encrypted_password


def account_hash_password(password, salt):
    '''
    password must be a str type
    salt must be a float type
    encrypted_password is bytes type
    '''

    password_salt_bytearray = bytearray()
    password_salt_bytearray.extend(str(password).encode())
    password_salt_bytearray.extend(struct.pack('f', float(salt)))

    encrypted_password = hashlib.sha256(password_salt_bytearray).digest()
    return encrypted_password


# Mock database for accounts (Encrypted Text)
# {username:(account_hash_password(password+salt):bytes, salt:float)}
accounts = dict()
