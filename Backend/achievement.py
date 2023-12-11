"""
    Contains the blueprint that handles CRUD operation for education and profession
"""

from flask import Blueprint, request

from .achievement_classes import EducationMaster, ProfessionMaster
from .exceptions import (InvalidEducationException,
                         InvalidProfessionException,
                         UnAuthorizedAccessException,
                         IncompleteFormException,
                         UserNotLoggedInException)

global_education_master = EducationMaster()
global_profession_master = ProfessionMaster()

# blueprint to which all achievement views are registered
bp = Blueprint('achievement', __name__, url_prefix='/achievement')

@bp.route('/education', methods = ('POST', ))
@bp.route('/education/<int:education_id>', methods = ('GET','PUT', 'DELETE'))
def education(education_id = None):
    """
        For each request, calls the appropriate functions in global_education_master
    """
    if request.method == 'GET' :
        try:
            return global_education_master.get_education(education_id)
        except UserNotLoggedInException as exc:
            return str(exc),400
        except InvalidEducationException as exc:
            return str(exc), 400

    elif request.method == 'POST' :
        try:
            return global_education_master.create_education()
        except UserNotLoggedInException as exc:
            return str(exc),400
        except IncompleteFormException as exc:
            return str(exc), 400

    elif request.method == 'PUT' :
        try:
            return global_education_master.update_education(education_id)
        except InvalidEducationException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400

    elif request.method == 'DELETE' :
        try:
            return global_education_master.delete_education(education_id)
        except InvalidEducationException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400

    return 'Invalid Request'


@bp.route('/profession', methods = ('POST', ))
@bp.route('/profession/<int:profession_id>', methods = ('GET','PUT', 'DELETE'))
def profession(profession_id = None):
    """
        For each request, calls the appropriate functions in global_profession_master
    """
    if request.method == 'GET' :
        try:
            return global_profession_master.get_profession(profession_id)
        except UserNotLoggedInException as exc:
            return str(exc),400
        except InvalidProfessionException as exc:
            return str(exc), 400

    elif request.method == 'POST' :
        try:
            return global_profession_master.create_profession()
        except UserNotLoggedInException as exc:
            return str(exc),400
        except IncompleteFormException as exc:
            return str(exc), 400

    elif request.method == 'PUT' :
        try:
            return global_profession_master.update_profession(profession_id)
        except UserNotLoggedInException as exc:
            return str(exc),400
        except InvalidProfessionException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400

    elif request.method == 'DELETE' :
        try:
            global_profession_master.delete_profession(profession_id)
            return 'Profession deleted'
        except UserNotLoggedInException as exc:
            return str(exc),400
        except InvalidProfessionException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400

    return 'Invalid Request'
    