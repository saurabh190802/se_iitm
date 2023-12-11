"""
    All custom exceptions thrown during execution are defined here
"""

class IncompleteFormException(Exception):
    """
        Raised when some of the fields in a post request are missing
    """

class InvalidInputException(Exception):
    """
        Raised when input field doesn't meet validation criteria
    """

class UserAlreadyExistsException(Exception):
    """
        Raised when user with same email is already present in the system
    """

class InvalidCredentialsException(Exception):
    """
        Raised when provided email or password or both during login are wrong
    """

class InvalidPostException(Exception):
    """
        Raised when trying to access a post that doesn't exist
    """

class InvalidQuizException(Exception):
    """
        Raised when trying to access a quiz that doesn't exist
    """

class InvalidQuestionException(Exception):
    """
        Raised when trying to access a question that doesn't exist
    """

class InvalidOptionException(Exception):
    """
        Raised when trying to access an option that doesn't exist
    """

class InvalidEducationException(Exception):
    """
        Raised when trying to access an education entry that doesn't exist
    """

class InvalidProfessionException(Exception):
    """
        Raised when trying to access a profession entry that doesn't exist
    """

class UnAuthorizedAccessException(Exception):
    """
        Raised when trying to access or modify objects that user doesn't have permissions for
    """
    
class UserNotLoggedInException(Exception):
    """
        Raised when trying to access a resource that requires user to be logged in
    """