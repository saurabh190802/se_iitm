"""
    Contains the blueprint that handles CRUD operation for profile
"""

from flask import Blueprint, request
from flask import request, g, jsonify
from werkzeug.exceptions import BadRequestKeyError


from .database import db
from .achievement_classes import EducationMaster, ProfessionMaster
from .exceptions import (IncompleteFormException,
                         UnAuthorizedAccessException,
                         InvalidEducationException,
                         InvalidProfessionException,
                         UserNotLoggedInException)

from .models import Education, Profession, User

global_education_master = EducationMaster()
global_profession_master = ProfessionMaster()

# blueprint to which all achievement views are registered
bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:user_id>', methods = ('GET', ))
def get_profile(user_id):
    """
        Gets all the education and profession for given user id
    """

    education_entries = []
    profession_entries = []
    
    try:
        existing_user_data = User.query.filter_by(user_id = user_id).first().__dict__.copy()
        existing_user_data.pop('_sa_instance_state')
        existing_user_data.pop('password')
    except:
        return "No user found",400

    existing_education_entries = Education.query.filter_by(user_id = user_id)

    for entry in existing_education_entries:
        education_entries.append(global_education_master.get_education(entry.education_id))
    
    existing_profession_entries = Profession.query.filter_by(user_id = user_id)

    for entry in existing_profession_entries:
        profession_entries.append(global_profession_master.get_profession(entry.profession_id))

    return jsonify({'user' : existing_user_data,
            'data' : education_entries,
            'profession' : profession_entries})

