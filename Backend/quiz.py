"""
    Contains the blueprint that handles CRUD operation for quizzes
"""

from flask import Blueprint, request

from .quiz_classes import QuizMaster

from .exceptions import (InvalidQuizException,
                         UnAuthorizedAccessException,
                         IncompleteFormException)

# Handles underlying logic for the CRUD operations
global_quiz_master = QuizMaster()

# blueprint to which all quiz views are registered
bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@bp.route('/', methods = ('POST', ))
@bp.route('/<int:quiz_id>', methods = ('GET','PUT', 'DELETE'))
def quiz(quiz_id = None):
    """
        For each request, calls the appropriate functions in global_quiz_master
    """
    if request.method == 'GET':
        try:
            return global_quiz_master.get_quiz(quiz_id)
        except InvalidQuizException as exc:
            return str(exc), 400

    elif request.method == 'POST':

        try:
            return global_quiz_master.create_quiz()

        except IncompleteFormException as exc:
            return str(exc), 400

    elif request.method == 'PUT':

        try:
            return global_quiz_master.update_quiz(quiz_id)
        except InvalidQuizException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400


    elif request.method == 'DELETE':

        try:
            global_quiz_master.delete_quiz(quiz_id)
            return 'Quiz Deleted'
        except InvalidQuizException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400
    return 'Invalid Request'
