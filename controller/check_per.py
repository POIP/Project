from functools import wraps
from flask import redirect, url_for, session
from model.message import message
from sqlalchemy import *


def admin_check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_account_id' not in session:
            return redirect(url_for('admin.login'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def driver_check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'driver_account_id' not in session:
            return redirect(url_for('driver.login'))
        else:
            return f(*args, **kwargs)

    return decorated_function


def driver_check_message(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        driver_ID = session['driver_account_id']
        number = message.query.filter(
            or_(and_(message.receiver_ID == driver_ID, message.flag == True, message.read_flag == False),
                and_(message.sender_ID == driver_ID, message.flag == False, message.read_flag == False))).all()
        length = len(number)
        if length == 0:
            length = ''
        session['message_count'] = length

        return f(*args, **kwargs)

    return decorated_function


def advter_check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'adv_account_id' not in session:
            return redirect(url_for('adv.login'))
        else:
            return f(*args, **kwargs)

    return decorated_function
