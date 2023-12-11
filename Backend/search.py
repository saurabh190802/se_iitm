"""
    Contains the search functionality views.
    Given a query string, returns output that is similar to it.
"""

from flask import Blueprint, jsonify
from .models import User, Post,Quiz

# blueprint to which all search views are registered
bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/users/<search_query>', methods = ('GET',))
def search_users(search_query=None):
    """
        Returns user data whose first name or last name is similar to the search query
    """
    if search_query is None:
        return 'Empty Search Query', 400

    search_string = f'%{search_query}%'.format(search_query)
    results = User.query.filter((User.first_name.like(search_string)) |
                                (User.last_name.like(search_string))).all()

    results = [i.__dict__ for i in results]
    for i in results:
        i.pop('_sa_instance_state')
        i.pop('password')
    return jsonify({'data':results})

@bp.route('/posts/<search_query>', methods = ('GET',))
def search_posts(search_query=None):
    """
        Returns post data whose title or caption is similar to the search query
    """
    if search_query is None:
        return 'Empty Search Query', 400

    search_string = f'%{search_query}%'.format(search_query)
    results = Post.query.filter((Post.post_title.like(search_string)) |
                                (Post.post_caption.like(search_string))).all()

    results = [i.__dict__ for i in results]


    for i in results:
        i.pop('_sa_instance_state')

    return jsonify({'data':results})

@bp.route('/quizzes/<search_query>', methods = ('GET',))
def search_quizzes(search_query=None):
    """
        Returns quiz data whose title or caption is similar to the search query
    """
    if search_query is None:
        return 'Empty Search Query', 400

    search_string = f'%{search_query}%'.format(search_query)
    results = Quiz.query.filter((Quiz.quiz_title.like(search_string)) |
                                (Quiz.quiz_caption.like(search_string))).all()

    results = [i.__dict__ for i in results]

    for i in results:
        i.pop('_sa_instance_state')

    return jsonify({'data':results})
