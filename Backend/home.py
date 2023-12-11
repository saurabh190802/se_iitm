"""
    Contains the blueprint that gets all post and quiz entries for home page
"""

from flask import Blueprint, request, jsonify
from flask import request, g
from werkzeug.exceptions import BadRequestKeyError


from .database import db
from .achievement_classes import EducationMaster, ProfessionMaster
from .exceptions import (IncompleteFormException,
                         UnAuthorizedAccessException,
                         InvalidEducationException,
                         InvalidProfessionException,
                         UserNotLoggedInException)

from .models import Education, Profession, User, Post, Quiz
from .post_classes import PostMaster
from .quiz_classes import QuizMaster

global_post_master = PostMaster()
global_quiz_master = QuizMaster()

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/', methods = ('GET', ))
def home_data():

    
    existing_posts = Post.query.all()

    post_data = []

    for post in existing_posts:
        post_data.append(global_post_master.get_post(post.post_id))
    
    existing_quizzes = Quiz.query.all()
    
    quiz_data = []

    for quiz in existing_quizzes:
        quiz_data.append(global_quiz_master.get_quiz(quiz.quiz_id))

    return jsonify ({
            'data': post_data,
            })