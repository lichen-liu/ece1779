from flask import render_template, redirect, url_for, request, g, session
from app import webapp


@webapp.route('/api/account_actions', methods=['POST'])
# Web handler for account actions
def account_actions_handler():
    account_action_type = request.form.get('action')
    username = request.form.get('username')
    password = request.form.get('password')
    rememberme = (request.form.get('rememberme') == 'True')
    if account_action_type == 'login':
        return account_login(username, password, rememberme)
    elif account_action_type == 'register':
        return account_register(username, password, rememberme)
    else:
        # No other actions are supported yet
        assert(False)


@webapp.route('/api/register', methods=['POST'])
# API handler for account register
def account_register_handler():
    username = request.form.get('username')
    password = request.form.get('password')
    return account_register(username, password)


@webapp.route('/api/logout', methods=['GET'])
# Web handler for logout
def account_logout_handler():
    if account_is_logged_in():
        account_logout()
    return redirect('/')


def account_register(username, password, rememberme=False):
    print('Registering: u=' + username + ' p=' + password)
    
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
        return 'Error! ' + username + ' exceeds ' + str(USERNAME_MAX_LENGTH) + ' characters!'

    # Register the user (business)
    accounts[username] = password
    print('    Successful!')

    # Login the user (business)
    login_result = account_login(username, password, rememberme)

    return login_result


def account_is_logged_in():
    return session.get('username')


def account_login(username, password, rememberme=False):
    if session.get('username') is None:
        print('Login: u=' + username + ' p=' + password + ' rememberme=' + str(rememberme))

        # Validate input (format)
        if not username:
            return 'Error! Username is not valid!'
        if not password:
            return 'Error! Password is not valid!'

        # Validate input (business)
        if accounts.get(username) is None or accounts.get(username) != password:
            return 'Error! Username or Password is not correct!'

        # Create a session (business)
        assert(session.get('username') is None)
        session['username'] = username
        session.permanent = rememberme
        print('    Successful!')

    return redirect('/')


def account_logout():
    # Clear the session (business)
    assert(session.get('username') is not None)
    username = session.get('username')
    print('Logout: u=' + username)
    session.pop('username')
    session.clear()
    print('    Successful!')


# Mock database for accounts (Clear Text)
# {username:password}
accounts = dict()