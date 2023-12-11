"""
    Contains the blueprint that handles CRUD operation for posts    
"""


from flask import  Blueprint, request, jsonify

from .post_classes import PostMaster
from .exceptions import (IncompleteFormException,
                         InvalidInputException,
                         InvalidPostException,
                         UnAuthorizedAccessException,
                         UserNotLoggedInException)


# blueprint to which all post views are registered
bp = Blueprint('post', __name__, url_prefix='/post')

global_post_master = PostMaster()

@bp.route('/', methods = ('POST', ))
@bp.route('/<int:post_id>', methods = ('GET', 'PUT', 'DELETE') )
def post_master(post_id = None):
    """
        For each request, calls the appropriate functions in global_post_master
    """
    if request.method == 'GET':
        try:
            existing_post_data = global_post_master.get_post(post_id)
            return jsonify({'post_title':existing_post_data['post_title'], 'post_body':existing_post_data['post_caption']})

        except InvalidPostException as exc:
            return str(exc), 400

    elif request.method == 'POST' :

        try:
            return global_post_master.create_post()
        except IncompleteFormException as exc:
            return str(exc), 400
        except InvalidInputException as exc:
            return str(exc), 400


    elif request.method == 'PUT' :

        try:
            return global_post_master.update_post(post_id)
        except UserNotLoggedInException as exc:
            return str(exc), 400
        except InvalidPostException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400


    elif request.method == 'DELETE':

        try:
            return global_post_master.delete_post(post_id)
        except UserNotLoggedInException as exc:
            return str(exc), 400
        except InvalidPostException as exc:
            return str(exc), 400
        except UnAuthorizedAccessException as exc:
            return str(exc), 400

    return 'Invalid Request'
    