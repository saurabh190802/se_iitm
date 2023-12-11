"""
    All views related to authorization are defined here and added to auth blueprint
"""

import jwt
from jwt.exceptions import DecodeError
from flask import Blueprint, g, request

from .backend_secret import SECRET_KEY
from .auth_classes import Register, Login
from .models import User
from .exceptions import (UserAlreadyExistsException,
                         InvalidInputException,
                         InvalidCredentialsException,
                         IncompleteFormException)

global_register = Register()
global_login = Login()

# blueprint to which all authoriztion views are registered
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = ('POST',))
def register():
    """
        Collects form data and attempts to add user 
    """
    try:
        return global_register.add_user()
    except IncompleteFormException as exc:
        return str(exc),400
    except InvalidInputException as exc:
        return str(exc), 400
    except UserAlreadyExistsException as exc:
        return str(exc), 400

@bp.route('/login', methods = ('POST',) )
def login():
    """
        Collects form data and attempts user login
    """

    try:
        return global_login.login_user()
    except IncompleteFormException as exc:
        return str(exc), 400
    except InvalidInputException as exc:
        return str(exc), 400
    except InvalidCredentialsException as exc:
        return str(exc), 400


@bp.before_app_request
def log_in_user():
    """
        Run before every request. Tries to get logged in user id from JWT token if sent.
        This user id is available to all functions in 'g' from Flask
    """
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']


    if not token :
        g.user = None

    else:
        try:
            sent_data = jwt.decode(token, SECRET_KEY,algorithms="HS256")
        except DecodeError:
            return 'Malformed Token sent', 400

        get_user_data = User.query.filter_by(user_id =sent_data['user_id']).first()

        g.user = get_user_data
