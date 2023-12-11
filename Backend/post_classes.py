"""
    Handles all logic for the post CRUD operations
    PostMaster creates post
"""

from flask import request, g, jsonify
from werkzeug.exceptions import BadRequestKeyError


from .database import db
from .exceptions import (IncompleteFormException,
                         UnAuthorizedAccessException,
                         InvalidPostException,
                         InvalidInputException,
                         UserNotLoggedInException)
from .models import Post

class PostMaster:
    """
        Responsible for handling CRUD operations to Post table
    """
    def __init__(self):
        self.post_user_id = None
        self.post_title = None
        self.post_caption = None

    def get_form_data(self, request_type):
        """
            Gets the required data from the form input sent
            If all data is not present, raises Exception
        """
        try:
            self.post_user_id = g.user.user_id
        except:
            raise UserNotLoggedInException("No User Found. Login first.")
        try:
            self.post_title = request.json['post_title']
        except BadRequestKeyError as exc:
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                              post_title, post_caption.""") from exc
        try:
            self.post_caption = request.json['post_caption']
        except BadRequestKeyError as exc:
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                              post_title, post_caption.""") from exc

    def validate_data(self):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        if self.post_title == '':
            raise InvalidInputException("Post title can't be empty")
        return True

    def create_post(self):
        """
            Gets form data from request. Validates data
            Creates entry in Post table
        """
        self.get_form_data('POST')

        if self.validate_data():
            new_post = Post(**self.__dict__)
            db.session.add(new_post)


            new_post_data = new_post.__dict__.copy()

            new_post_data.pop('_sa_instance_state')
            db.session.commit()
            new_post_data['post_id'] = new_post.post_id


            return jsonify({'status':'ok','post_id':new_post_data['post_id']})
        return jsonify({'status':'Failed to create post'})

    def get_post(self, post_id):
        """
            Returns post data
            Raises exception if non-existent post id is given
        """
        existing_post = Post.query.filter_by(post_id = post_id).first()

        if existing_post is None:
            raise InvalidPostException("Post Id given doesn't match any existing post")

        existing_post_data = existing_post.__dict__.copy()

        existing_post_data.pop('_sa_instance_state')

        return existing_post_data

    def update_post(self,post_id):
        """
            Updates post if valid post id and user created the post.
            Updates the relevant fields sent
        """
        if g.user is None:
            raise UserNotLoggedInException("No User Found. Login first.")
        
        self.get_form_data('PUT')

        existing_post = Post.query.filter_by(post_id = post_id).first()

        if existing_post is None:
            raise InvalidPostException("Post Id given doesn't match any existing post")
        
        

        if existing_post.post_user_id != g.user.user_id:
            raise UnAuthorizedAccessException("You don't have permissions to update this post")


        if self.post_title is not None :
                #validation
            existing_post.post_title = self.post_title
        if self.post_caption is not None :
                #validation
            existing_post.post_caption = self.post_caption
        updated_post_data = existing_post.__dict__.copy()
        updated_post_data.pop('_sa_instance_state')
        db.session.commit()

        return jsonify({'status':'ok','post_id':existing_post.post_id})

    def delete_post(self,post_id):
        """
            Deletes post if valid post id and user created the post
        """

        if g.user is None:
            raise UserNotLoggedInException("No User Found. Login first.")
        
        existing_post = Post.query.filter_by(post_id = post_id).first()

        if existing_post is None:
            raise InvalidPostException("Post Id given doesn't match any existing post")

        if existing_post.post_user_id != g.user.user_id:
            raise UnAuthorizedAccessException("You don't have permissions to delete this post")

        db.session.delete(existing_post)
        db.session.commit()
        existing_posts = Post.query.all()
        post_data = []
        for post in existing_posts:
            post_data.append(self.get_post(post.post_id))

        return jsonify({'status':'ok','data':post_data})
