import smtplib
import imaplib
import datetime
import string
import secrets

from flask import redirect, request, session, url_for, render_template
from manager_app import webapp


_SMTP_SERVER = 'smtp.gmail.com'
_IMAP_SERVER = 'imap.gmail.com'
_SENDER_EMAIL = 'lichen.liu.ece1779.manager@gmail.com'
_SENDER_PASSWORD = 'ece1779password'


# PUT YOUR EMAIL ADDRESS HERE
_EMAIL_WHITELIST = ['liulichen112233@gmail.com', 'huang627158768@gmail.com', 'bwuzhang@gmail.com']


def send_email(to_addr, msg):
    with smtplib.SMTP(_SMTP_SERVER, 587) as server:
        server.ehlo()
        server.starttls()
        server.login(_SENDER_EMAIL, _SENDER_PASSWORD)
        server.sendmail(_SENDER_EMAIL, to_addr, msg)
        
        print('Message sent to: ' + to_addr + '!')


def delete_all_inbox_emails():
    with imaplib.IMAP4_SSL('imap.gmail.com', 993) as server:
        server.login(_SENDER_EMAIL, _SENDER_PASSWORD)
        #server.select('inbox')
        server.select('INBOX')  # required to perform search, m.list() for all lables, '[Gmail]/Sent Mail'
        _, data = server.search(None, 'ALL')
        for num in data[0].split():
            server.store(num, '+X-GM-LABELS', '\\Trash')

        server.select('[Gmail]/Trash')  # select all trash
        server.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
        server.expunge()  # not need if auto-expunge enabled

        print('All messages in Inbox are deleted!')


def delete_all_sent_emails():
    with imaplib.IMAP4_SSL('imap.gmail.com', 993) as server:
        server.login(_SENDER_EMAIL, _SENDER_PASSWORD)
        server.select('"[Gmail]/Sent Mail"')
        _, data = server.search(None, 'ALL')
        for num in data[0].split():
            server.store(num, '+X-GM-LABELS', '\\Trash')

        server.select('[Gmail]/Trash')  # select all trash
        server.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
        server.expunge()  # not need if auto-expunge enabled

        print('All messages in Sent Mail are deleted!')


def generate_otp():
    '''
    (password, timestamp)
    '''
    password = ''.join(secrets.choice(string.digits) for i in range(6))
    timestamp = datetime.datetime.utcnow()
    return(password, timestamp)


def verify_otp(input_password, password, timestamp):
    '''
    password is valid for 60 seconds
    '''
    if datetime.datetime.utcnow() - timestamp < datetime.timedelta(seconds=60):
        return input_password == password
    return False


def set_authenticating(email, password, timestamp):
    session.clear()
    session['email'] = email
    session['password'] = password
    session['timestamp'] = timestamp


def get_authenticating_credential():
    '''
    (email, password, timestamp)
    '''
    assert(is_authenticating())
    return (session['email'], session['password'], session['timestamp'])


def set_authenticated():
    session.clear()
    session['authenticated'] = True


def set_deauthenticated():
    session.clear()


def is_authenticating():
    return session.get('email') is not None and session.get('password') is not None and session.get('timestamp') is not None


def is_authenticated():
    return session.get('authenticated')


@webapp.route('/api/authenticate', methods=['POST'])
def authentication_main_handler():
    if is_authenticated():
        set_deauthenticated()

    request_value = request.form.get('textfield_name')
    if not is_authenticating() and request_value is None:
        return render_email_authentication_page()
    elif not is_authenticating() and request_value is not None:
        email = request_value
        if email in _EMAIL_WHITELIST:
            password, timestamp = generate_otp()
            msg="""\
Subject: [One Time Password]

This is your login token, please use it within 60 seconds: """ + password
            send_email(to_addr=email, msg=msg)
            delete_all_sent_emails()
            set_authenticating(email=email, password=password, timestamp=timestamp)
            return render_authentication_page(
                title='Please Enter Your One Time Password', form_action=url_for('authentication_main_handler'), 
                textfield_label='One Time Password', textfield_value=None,
                description='Your One Time Password has been sent to your email: ' + email + '. Please use it within 60 seconds.')
        else:
            set_deauthenticated()
            return render_email_authentication_page(textfield_value=None, description='Your email (' + email + ') is not privileged, please contact website administrator.')
    else:
        assert(is_authenticating())

        input_password = request_value
        email, password, timestamp = get_authenticating_credential()
        
        if verify_otp(input_password=input_password, password=password, timestamp=timestamp):
            set_authenticated()
            return redirect('/')
        else:
            set_deauthenticated()
            return render_email_authentication_page(textfield_value=email, description='Incorrect or expired One Time Password: ' + input_password + '.')


def render_email_authentication_page(textfield_value=None, description=None):
    return render_authentication_page(
        title='Please Enter Your Email', form_action=url_for('authentication_main_handler'), textfield_label='Email',
        textfield_value=textfield_value, description=description)


def render_authentication_page(title, form_action, textfield_label, textfield_value=None, description=None):
    return render_template('authentication.html',
        title=title,
        form_action=form_action,
        textfield_label=textfield_label,
        textfield_value=textfield_value,
        description=description)


def logout_handler():
    set_deauthenticated()
    return redirect('/')


@webapp.before_request
def pre_request_handler():
    if not is_authenticated() and not is_authenticating():
        print('goto authentication_main_handler')
        return authentication_main_handler()

    if request.args.get('logout'):
        print('goto logout')
        return logout_handler()
