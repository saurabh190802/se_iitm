"""
    Handles all logic for the quiz CRUD operations
    QuizMaster creates quiz
    It calls QuestionMaster to create questions
    QuestionMaster calls OptionMaster to create options
"""

from flask import request, g
from werkzeug.exceptions import BadRequestKeyError


from .database import db
from .exceptions import (IncompleteFormException,
                         UnAuthorizedAccessException,
                         InvalidQuizException,
                         InvalidQuestionException,
                         InvalidOptionException)

from .models import Quiz, Question, Option


class QuizMaster:
    """
        Responsible for handling CRUD operations to Quiz table
        Calls QuestionMaster to handle functionality of CRUD for questions
    """
    def __init__(self):
        self.quiz_user_id = None
        self.quiz_title = None
        self.quiz_caption = None
        self.quiz_questions = None

    def get_form_data(self):
        """
            Gets the required data from the json input sent
            If all data is not present, raises Exception
        """
        try:
            self.quiz_user_id = g.user.user_id
        except:
            pass

        try:
            self.quiz_title = request.get_json()['quiz_title']
            self.quiz_caption = request.get_json()['quiz_caption']
            self.quiz_questions = request.get_json()['quiz_questions']

        except BadRequestKeyError as exc:
            raise IncompleteFormException("""All details have not been sent.Required Fields :
                                          quiz_title, quiz_caption, quiz_questions""") from exc


    def validate_data(self):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        return True

    def get_quiz(self, quiz_id):
        """
            Returns all the quiz data with questions and options
            Raises exception if non-existent quiz id is given
        """
        existing_quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()

        if existing_quiz is None:
            raise InvalidQuizException("Quiz id doesn't match any existing quiz")

        existing_quiz_data = existing_quiz.__dict__

        existing_quiz_data.pop('_sa_instance_state')

        existing_quiz_data['quiz_questions'] = {}

        existing_questions = Question.query.filter_by(question_quiz_id = quiz_id).order_by(Question.question_id.asc()).all()

        question_master = QuestionMaster(quiz_id)

        for i,j in enumerate(existing_questions) :
            existing_quiz_data['quiz_questions'][i+1] = question_master.get_question(j.question_id)

        return existing_quiz_data


    def create_quiz(self):
        """
            Gets json data from request, validates it.
            Creates entry in Quiz table.
            Passes data to QuestionMaster to create questions
        """
        self.get_form_data()
        if self.validate_data():
            new_quiz = Quiz(quiz_user_id = self.quiz_user_id,
                            quiz_title = self.quiz_title,
                            quiz_caption = self.quiz_caption)

            db.session.add(new_quiz)
            db.session.commit()

            question_master = QuestionMaster(new_quiz.quiz_id)

            for question  in self.quiz_questions:
                question_master.add_question(self.quiz_questions[question])
            
            return self.get_quiz(new_quiz.quiz_id)

    def delete_quiz(self,quiz_id):
        """
            Deletes quiz if valid quiz id and user created the quiz
            Entry deleted in quiz table. DB deletes respective questions and options
        """
        existing_quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()

        if existing_quiz is None :
            raise InvalidQuizException("Quiz id doesn't match any existing quiz")

        if existing_quiz.quiz_user_id != g.user.user_id :
            raise UnAuthorizedAccessException("You don't have permissions to delete this quiz")

        db.session.delete(existing_quiz)

        db.session.commit()

    def update_quiz(self,quiz_id):
        """
            Updates quiz if valid quiz id and user created the quiz.
            First deletes the quiz and creates quiz from the new complete data sent
        """
        existing_quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()

        if existing_quiz is None :
            raise InvalidQuizException("Quiz id doesn't match any existing quiz")

        if existing_quiz.quiz_user_id != g.user.user_id :
            raise UnAuthorizedAccessException("You don't have permissions to update this quiz")

        self.delete_quiz(quiz_id=quiz_id)

        return self.create_quiz()


class QuestionMaster:
    """
        Responsible for creating and querying entries in Question Table
        Gets question data from QuizMaster to create question
        Passes data to OptionMaster to handle operations for options
    """
    def __init__(self, quiz_id):
        self.question_quiz_id = quiz_id

    def validate_question(self,question):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        return True

    def get_question(self,question_id):
        """
            Returns complete data on question.
            Requests option information from OptionMaster
            Raises exception if invalid question id
        """

        existing_question = Question.query.filter_by(question_id = question_id).first()

        if existing_question is None:
            raise InvalidQuestionException("Question id doesn't match any existing question")

        existing_question_data = existing_question.__dict__

        existing_question_data.pop('_sa_instance_state')
        existing_question_data.pop('question_quiz_id')
        existing_question_data.pop('question_answer')

        existing_options = Option.query.filter_by(option_question_id = question_id).order_by(Option.option_id.asc()).all()

        option_master = OptionMaster(question_id)

        existing_question_data['options'] = {}

        for i,j in enumerate(existing_options):
            existing_question_data['options'][i+1] = option_master.get_option(j.option_id)

        return existing_question_data

    def add_question(self, question):
        """
            Creates entry in Question table if data is validated
            Passes option data to OptionMaster to create entries in Option table
        """

        if self.validate_question(question):
            new_question = Question(question_quiz_id = self.question_quiz_id,
                                    question_text = question['question_text'],
                                    question_answer = question['question_answer'])

            db.session.add(new_question)
            db.session.commit()

            option_master = OptionMaster(new_question.question_id)

            for option in question['options']:
                option_master.add_option(question['options'][option])

class OptionMaster:
    """
        Handles Read and Create Operations for options
        Gets data from QuestionMaster
    """
    def __init__(self, question_id):
        self.option_question_id = question_id

    def validate_option(self,option):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        return True

    def get_option(self,option_id):
        """
            Returns data on option
            Raises Exception if invalid option id
        """

        existing_option = Option.query.filter_by(option_id = option_id).first()

        if existing_option is None:
            raise InvalidOptionException("Option id doesn't match any existing question")

        existing_option_data = existing_option.__dict__

        existing_option_data.pop('_sa_instance_state')
        existing_option_data.pop('option_question_id')

        return existing_option_data

    def add_option(self, option):
        """
            Creates entry in Option Table if data is validated
        """
        if self.validate_option(option):
            new_option = Option(option_question_id = self.option_question_id,
                                option_sequence_id = option['sequence_id'],
                                option_text = option['text'])
            db.session.add(new_option)
            db.session.commit()
