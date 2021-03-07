from flask import current_app
from functools import wraps
import flask_login


def restrict_to_advisors(func):
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in as an advisor before calling the actual view. (If they are
    not, it calls the :attr:`LoginManager.unauthorized` callback.) For
    example::

        @app.route('/post')
        @restrict_to_advisors
        def post():
            pass

    If there are only certain times you need to require that your user is
    an advisor, you can do so with::

        if not current_user.is_advisor:
            return current_app.login_manager.unauthorized()

    ...which is essentially the code that this function adds to your views.

    :param func: The view function to decorate.
    :type func: function
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Fetch the user performing the request
        user = flask_login.current_user

        # Ensure the user is logged in as an advisor
        if hasattr(user, 'is_advisor') and user.is_advisor:
            return func(*args, **kwargs)

        # Perform unauthorized redirect
        return current_app.login_manager.unauthorized()
    return decorated_view


def restrict_to_students(func):
    """
    If you decorate a view with this, it will ensure that the current user is
    logged in as a student before calling the actual view. (If they are
    not, it calls the :attr:`LoginManager.unauthorized` callback.) For
    example::

        @app.route('/post')
        @restrict_to_students
        def post():
            pass

    If there are only certain times you need to require that your user is
    a student, you can do so with::

        if not current_user.is_student:
            return current_app.login_manager.unauthorized()

    ...which is essentially the code that this function adds to your views.

    :param func: The view function to decorate.
    :type func: function
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Fetch the user performing the request
        user = flask_login.current_user

        # Ensure the user is logged in as a student
        if hasattr(user, 'is_student') and user.is_student:
            return func(*args, **kwargs)

        # Perform unauthorized redirect
        return current_app.login_manager.unauthorized()
    return decorated_view
