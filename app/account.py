from flask import render_template, redirect, url_for, request, g
from app import webapp


@webapp.route('/api/account_actions', methods=['POST'])
# Web handler for account actions
def account_actions_handler():
    account_action_type = request.form.get('action')
    username = request.form.get('username')
    password = request.form.get('password')
    if account_action_type == 'login':
        return account_login(username, password)
    elif account_action_type == 'register':
        return account_register(username, password)
    else:
        # No other actions are supported yet
        assert 0


@webapp.route('/api/register', methods=['POST'])
# API handler for account register
def account_register_handler():
    username = request.form.get('username')
    password = request.form.get('password')
    return account_register(username, password)


def account_register(username, password):
    print('Registering: u=' + username + ' p=' + password)
    
    if not username:
        return 'Error! Username is not valid!'
    if not password:
        return 'Error! Password is not valid!'
    
    if username in accounts:
        return 'Error! ' + username + ' is already registered!'

    accounts[username] = password
    print('    Successful!')

    login_result = account_login(username, password)

    return 'Successfully Registered: u=' + username + ' p=' + password + '! ' + login_result


def account_login(username, password):
    print('Login: u=' + username + ' p=' + password)

    if not username:
        return 'Error! Username is not valid!'
    if not password:
        return 'Error! Password is not valid!'

    if accounts.get(username) is None or accounts.get(username) != password:
        return 'Error! Username or Password is not correct!'

    print('    Successful!')
    return 'Successfully Login: u=' + username + ' p=' + password


def account_logout():
    pass

# Mock database for accounts (Clear Text)
# {username:password}
accounts = dict()