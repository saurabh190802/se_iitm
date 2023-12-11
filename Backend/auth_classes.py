"""
    Register class that has all functionality for user signup.
    Login class has all functionality for login
"""


from flask import request, jsonify
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

from .exceptions import (IncompleteFormException,
                         InvalidCredentialsException,
                         UserAlreadyExistsException,
                         InvalidInputException)

from .database import db
from .models import User
from .backend_secret import SECRET_KEY


class Register:
    """
        Functionality for user signup.
        Gets data from request, validates data and adds new user to db
    """
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.password = None

    def get_form_data(self):
        """
            Collects user details from post request. Raises Exception if all fields not present
        """
        try:
            self.first_name = request.json['first_name']
            self.last_name = request.json['last_name']
            self.email = request.json['email']
            self.password = generate_password_hash(request.json['password'])

        except BadRequestKeyError as exc:
            raise IncompleteFormException("""All details have not been sent. Required Fields :
                                           first_name, last_name, email, password.""") from exc

    def validate_data(self):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        if self.first_name == "":
            raise InvalidInputException("First name can't be empty")
        return True

    def add_user(self):
        """
            If data is valid adds new user to db
        """

        self.get_form_data()

        if self.validate_data():
            check_existing_user = User.query.filter_by(email = self.email).first()

            if check_existing_user is not None:
                raise UserAlreadyExistsException("""User with same email already exists.
                                                 Try with a different email""")
            new_user = User(**self.__dict__)
            db.session.add(new_user)
            db.session.commit()
            return jsonify ({ 'status':'ok'})
        return jsonify ({'status':'Failed to create user'})

class Login:
    """
        Functionality for user login.
        Gets data from request, validates data and logs in user if credentials match. 
        Returns a dict object with JWT token and user attributes on success.
    """
    def __init__(self):
        self.email = None
        self.password = None

    def get_form_data(self):
        """
            Collects user details from post request. Raises Exception if all fields not present
        """
        try:
            self.email = request.json['email']
            self.password = request.json['password']
        except BadRequestKeyError as exc:
            raise IncompleteFormException("""All details have not been sent. Required Fields :
                                           email, password.""") from exc

    def validate_data(self):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        if self.email == "":
            raise InvalidInputException("Email can't be empty")
        return True

    def login_user(self):
        """
            If valid data and credentials match, returns user details a dict with following fields:
            first_name, last_name, email, user_id, jwt_token
        """

        self.get_form_data()

        if self.validate_data():
            existing_user = User.query.filter_by(email = self.email).first()

            if existing_user is None:
                raise InvalidCredentialsException('Email or password or both are wrong')

            if not check_password_hash(existing_user.password, self.password):
                raise InvalidCredentialsException('Email or password or both are wrong')

            existing_user_data = existing_user.__dict__

            token_payload = {'user_id':existing_user_data['user_id']}
            encoded_token = jwt.encode(token_payload, SECRET_KEY,algorithm="HS256")
            existing_user_data['jwt_token'] = encoded_token
            existing_user_data['status'] = 'ok'

            existing_user_data.pop('_sa_instance_state')
            existing_user_data.pop('password')

            return jsonify({'jwt_token':existing_user_data['jwt_token'],'status' : 'ok','user_id':existing_user_data['user_id']})

        return jsonify({ 'status' : 'Failed to Login' })
    