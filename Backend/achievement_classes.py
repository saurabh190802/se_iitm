"""
    Handles all logic for the education and profession CRUD operations
"""

from flask import request, g, jsonify
from werkzeug.exceptions import BadRequestKeyError


from .database import db

from .exceptions import (IncompleteFormException,
                         UnAuthorizedAccessException,
                         InvalidEducationException,
                         InvalidProfessionException,
                         UserNotLoggedInException)

from .models import Education, Profession

class EducationMaster:
    """
        Responsible for handling CRUD operations to Education table
    """

    def __init__(self):
        self.user_id = None
        self.college_name = None
        self.joining_year = None
        self.graduation_year = None

    def get_form_data(self, request_type):
        """
            Gets the required data from the form input sent
            If all data is not present and it is a post request, raises Exception
        """

        try:
            self.user_id = g.user.user_id
        except:
            raise UserNotLoggedInException("No User Found. Login first.")

        try:
            self.college_name = request.json['college_name']
        except BadRequestKeyError as exc:
            print(exc)
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                            college_name, joining_year, graduation_year""") from exc
        try:
            self.joining_year = int(request.json['joining_year'])
        except BadRequestKeyError as exc:
            print(exc)
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                            college_name, joining_year, graduation_year""") from exc
        try:
            self.graduation_year = int(request.json['graduation_year'])
        except BadRequestKeyError as exc:
            print(exc)
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                            college_name, joining_year, graduation_year""") from exc

    def validate_data(self):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        return True

    def create_education(self):
        """
            Gets form data from request, validates it.
            Creates entry in Education table.
        """

        self.get_form_data('POST')

        if self.validate_data():
            new_education = Education(**self.__dict__)

            db.session.add(new_education)

            new_education_data = new_education.__dict__.copy()

            db.session.commit()

            new_education_data.pop('_sa_instance_state')
            new_education_data['education_id'] = new_education.education_id

            return new_education_data

        return 'Failed to add education'

    def get_education(self, education_id):
        """
            Returns all the education data for that entry
            Raises exception if non-existent education id is given
        """

        if g.user is None:
            raise UserNotLoggedInException("No User Found. Login first.")
            
        existing_education = Education.query.filter_by(education_id = education_id).first()

        if existing_education is None:
            raise InvalidEducationException("Education id doesn't match any existing entry")

        existing_education_data = existing_education.__dict__

        existing_education_data.pop('_sa_instance_state')

        return existing_education_data

    def update_education(self, education_id):
        """
            Updates education entry if valid education_id and user created it.
            Updates the relevant fields sent
        """

        self.get_form_data('PUT')
        existing_education = Education.query.filter_by(education_id = education_id).first()

        if existing_education is None:
            raise InvalidEducationException("Education id doesn't match any existing entry")

        if existing_education.user_id != g.user.user_id :
            raise UnAuthorizedAccessException("You don't have permissions to update this entry.")

        if self.college_name is not None:
            existing_education.college_name = self.college_name
        if self.joining_year is not None:
            existing_education.joining_year = self.joining_year
        if self.graduation_year is not None:
            existing_education.graduation_year = self.graduation_year

        db.session.commit()

        return self.get_education(existing_education.education_id)

    def delete_education(self, education_id):
        """
            Deletes education entry if valid education_id and user created the entry
        """
        if g.user is None:
            raise UserNotLoggedInException("No User Found. Login first.")
        
        existing_education = Education.query.filter_by(education_id = education_id).first()

        if existing_education is None:
            raise InvalidEducationException("Education id given doesn't match any existing entry")

        if existing_education.user_id != g.user.user_id :
            raise UnAuthorizedAccessException("You don't have permissions to delete this entry.")

        db.session.delete(existing_education)
        db.session.commit()
        education_entries = []
        new_education_entries = Education.query.filter_by(user_id = g.user.user_id)
        for entry in new_education_entries:
            education_entries.append(self.get_education(entry.education_id))
        return jsonify({'status':'Education Deleted','data':education_entries})



class ProfessionMaster:
    """
        Responsible for handling CRUD operations to Profession table
    """
    def __init__(self):
        self.user_id = None
        self.company_name = None
        self.joining_year = None
        self.graduation_year = None

    def get_form_data(self, request_type):
        """
            Gets the required data from the form input sent
            If all data is not present and it is a post request, raises Exception
        """

        try:
            self.user_id = g.user.user_id
        except:
            raise UserNotLoggedInException("No User Found. Login first.")

        try:
            self.company_name = request.form['company_name']
        except BadRequestKeyError as exc:
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                            company_name, joining_year, graduation_year""") from exc
        try:
            self.joining_year = request.form['joining_year']
        except BadRequestKeyError as exc:
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                            company_name, joining_year, graduation_year""") from exc
        try:
            self.graduation_year = request.form['graduation_year']
        except BadRequestKeyError as exc:
            if request_type == 'POST':
                raise IncompleteFormException("""All details have not been sent. Required Fields :
                                            company_name, joining_year, graduation_year""") from exc

    def validate_data(self):
        """
            Returns True if all fields meet the following requirements, else raises exception
        """
        return True

    def create_profession(self):
        """
            Gets form data from request. Validates data
            Creates entry in Profession table
        """

        self.get_form_data('POST')

        if self.validate_data():
            new_profession = Profession(**self.__dict__)

            db.session.add(new_profession)

            new_profession_data = new_profession.__dict__.copy()
            db.session.commit()

            new_profession_data.pop('_sa_instance_state')
            new_profession_data['profession_id'] = new_profession.profession_id

            return new_profession_data

        return 'Failed to add profession'

    def get_profession(self, profession_id):
        """
            Returns profession data
            Raises exception if non-existent post id is given
        """

        if g.user is None:
            raise UserNotLoggedInException("No User Found. Login first.")


        existing_profession = Profession.query.filter_by(profession_id = profession_id).first()

        if existing_profession is None:
            raise InvalidProfessionException("Profession Id given doesn't match any existing entry")

        existing_profession_data = existing_profession.__dict__

        existing_profession_data.pop('_sa_instance_state')

        return existing_profession_data

    def update_profession(self, profession_id):
        """
            Updates profession entry if valid profession id and user created the entry.
            Updates the relevant fields sent
        """

        self.get_form_data('PUT')
        existing_profession = Profession.query.filter_by(profession_id = profession_id).first()

        if existing_profession is None:
            raise InvalidProfessionException("Profession Id given doesn't match any existing entry")

        if existing_profession.user_id != g.user.user_id :
            raise UnAuthorizedAccessException("You don't have permissions to update this entry.")

        if self.company_name is not None:
            existing_profession.company_name = self.company_name
        if self.joining_year is not None:
            existing_profession.joining_year = self.joining_year
        if self.graduation_year is not None:
            existing_profession.graduation_year = self.graduation_year

        db.session.commit()

        return self.get_profession(existing_profession.profession_id)

    def delete_profession(self, profession_id):
        """
            Deletes profession entry if valid profession id and user created the entry
        """

        existing_profession = Profession.query.filter_by(profession_id = profession_id).first()

        if existing_profession is None:
            raise InvalidProfessionException("Profession Id given doesn't match any existing entry")

        if existing_profession.user_id != g.user.user_id :
            raise UnAuthorizedAccessException("You don't have permissions to delete this entry.")

        db.session.delete(existing_profession)
        db.session.commit()
        return 'Profession Deleted'
