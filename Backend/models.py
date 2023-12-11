"""
    All tables in database are defined here.
    To create a new table, add a new class here
"""

from .database import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

    post = db.relationship('Post', backref = 'user', lazy = True, cascade='all,delete-orphan')
    quiz = db.relationship('Quiz', backref = 'user', lazy = True, cascade='all,delete-orphan')

    education = db.relationship('Education', backref = 'user', lazy = True, cascade='all,delete-orphan')
    profession = db.relationship('Profession', backref = 'user', lazy = True, cascade='all,delete-orphan')

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    post_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete = 'cascade'))
    post_title = db.Column(db.String, nullable = False)
    post_caption = db.Column(db.String, nullable = False)

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key = True)
    quiz_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete = 'cascade'))
    quiz_title = db.Column(db.String, nullable = False)
    quiz_caption = db.Column(db.String, nullable = False)

    question = db.relationship('Question', backref = 'quiz', lazy = True, cascade='all,delete-orphan')

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key = True)
    question_quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id", ondelete = 'cascade'))
    question_text = db.Column(db.String, nullable = False)
    question_answer = db.Column(db.Integer, nullable = False)

    option = db.relationship('Option', backref = 'question', lazy = True, cascade='all,delete-orphan')

class Option(db.Model):
    option_id = db.Column(db.Integer, primary_key = True)
    option_question_id = db.Column(db.Integer, db.ForeignKey("question.question_id", ondelete = 'cascade'))
    option_sequence_id = db.Column(db.Integer, nullable = False)
    option_text = db.Column(db.String, nullable = False)

class Education(db.Model):
    education_id  = db.Column(db.Integer, primary_key = True)           
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete = 'cascade'))
    college_name = db.Column(db.String, nullable = False)
    joining_year = db.Column(db.Integer, nullable = False)
    graduation_year = db.Column(db.Integer)

class Profession(db.Model):
    profession_id = db.Column(db.Integer, primary_key = True)           
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete = 'cascade'))
    company_name = db.Column(db.String, nullable = False)
    joining_year = db.Column(db.Integer, nullable = False)
    graduation_year = db.Column(db.Integer)
