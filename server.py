import flask
from flask import Flask, render_template, request, jsonify
import flask_login
from os import urandom
from user import User
from database import Database
import security

# data collection utilities
import webscraping.adviseescraper as advisee_scraper
from webscraping.components.student import Student
from webscraping.mygcc import MyGcc
import webscraping.errors as errors


### FOR DEBUG PURPOSES ONLY ###
OVERRIDE_IS_ADVISOR = None  # overrides the is_advisor login check (True|False|None)
                            # set the value to None to disable the override


# Initializes the flask application
app = Flask(__name__)
app.secret_key = urandom(16)

# Initializes the login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# This dictionary tracks all authenticated users
users = {}


### USER AUTHENTICATION ###

@login_manager.user_loader
def load_user(user_id):
    """ Returns the User associated with the specified user identifier. """
    return users.get(user_id)


@app.route('/', methods=['GET'])
@app.route('/login/', methods=['GET'])
def login_get():
    """
    This endpoint serves to provide unauthenticated users a visual
    way to perform site login. If the user requesting this endpoint
    is already authenticated, this will redirect them to the appropriate
    home page depending on if they are a student or an advisor.
    """

    # Fetch the user performing the request
    user = flask_login.current_user

    # If the user is logged in as an advisor, redirect them to the advisor home page.
    if user.is_authenticated and hasattr(user, 'is_advisor') and user.is_advisor:
        return flask.redirect(flask.url_for('advisor_landing_page'))

    # If the user is logged in as a student, redirect them to the student home page.
    if user.is_authenticated and hasattr(user, 'is_student') and not user.is_student:
        return flask.redirect(flask.url_for('student_landing_page'))

    # Since the user is not logged in, we'll serve them the login page.
    return render_template('loginPage.html')


@app.route('/', methods=['POST'])
@app.route('/login/', methods=['POST'])
def login_post():
    """
    This endpoint serves to receive incoming authentication requests
    from unauthenticated users attempting to perform site login. If
    fields are missing or authentication is unsuccessful, the page
    will redirect back to the login page. Otherwise, the page will
    redirect to the appropriate home page associated to the user.

    If the user performing the authentication is already logged in,
    invalid credentials will revoke the user's authenticated status.
    """

    # Invalidate the current user session to perform a fresh login
    current_user = flask_login.current_user
    if current_user.get_id() in users:
        del users[current_user.get_id()]
    flask_login.logout_user()

    # Retrieve the username and password from the form
    login_form = flask.request.form
    username = login_form.get('username')
    password = login_form.get('password')

    # Redirect if either the username or password is missing
    if not username or not password:
        return flask.redirect(flask.url_for('login_get'))

    # Interface with https://my.gcc.edu/ICS/
    portal = MyGcc(username, password)

    try:
        # Attempt to perform single-sign-on with provided credentials
        portal.login()

        # Fetch the user's identification number and whether they are an advisor
        user_id = portal.profile.user_id

        if OVERRIDE_IS_ADVISOR is None:
            is_advisor = portal.advising.is_advisor
        else:
            is_advisor = OVERRIDE_IS_ADVISOR

        # Ensure we were able to grab a user id; otherwise fishy is going on
        if user_id is not None:

            # Build the new user object for this session
            user = User(user_id, is_advisor, username, password)

            # Flag this user session as authenticated
            users[user.get_id()] = user
            flask_login.login_user(user)

            # Redirect to the student or advisor home page accordingly
            if is_advisor:
                return flask.redirect(flask.url_for("advisor_landing_page"))
            return flask.redirect(flask.url_for("student_landing_page"))

        # Redirect to login page if the user id was not present
        else:
            return flask.redirect(flask.url_for('login_get'))

    except errors.LoginError:
        # Redirect to login page if the supplied credentials were invalid
        return flask.redirect(flask.url_for('login_get'))


@app.route('/logout', methods=['POST'])
def logout():
    """
    This endpoint invalidates a user's session so that they
    are no longer authenticated. Any persistent cookies or
    cache for the user becomes invalidated and deleted.
    """

    # Removes the user from the user cache
    user = flask_login.current_user
    if user.get_id() in users:
        del users[user.get_id()]

    # Invalidates the current user session
    flask_login.logout_user()

    # Redirect back to the login page
    return flask.redirect(flask.url_for('login_get'))


### ADVISOR SPECIFIC ENDPOINTS ###

@app.route('/advisorHomePreview/', methods=['GET', 'POST'])
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_advisors  # you must be an advisor to view this page
def advisor_landing_page():
    """
    This endpoint serves to provide advisors an overview of all their
    advisee students. This is the default landing page that advisors
    get redirected to after performing site login.
    """

    if flask.request.method == 'GET':

        # Fetch all of the student's this advisor is responsible for
        advisor = flask_login.current_user
        advisor_students = advisee_scraper.get_advisers_students(advisor.id, advisor.username, advisor.password)

        # Format all the user data into something we can pass into the html template
        data = [
            {
                'id': student.student_id,
                'name': f'{student.firstname} {student.lastname}',
                'credits': student.credits_completed,
                'email': student.email,
                'status': 1,    # TODO: populate this with their schedule status
                'year': student.classification,
                'major': None if not student.majors else student.majors[0][0],  # TODO: handle multiple majors
            } for student in advisor_students
        ]

        # Serve the advisor landing page template to the user
        return render_template('advisorLandingPage.html', advisees=data)

    elif flask.request.method == 'POST':

        # TODO: instead of this being handled here, do it in advisor_viewing_student()

        # # Fetch the student the advisor is requesting to view the page of
        # student_id = 1  # TODO: fetch this value from the post result
        #
        # # Fetch the user id of the advisor performing this request
        # advisor_id = flask_login.current_user.id
        #
        # # Fetch the student the advisor is requesting
        # db = Database()
        # student = db.get_student(student_id, advisor_id)
        # db.close()
        #
        # if student is not None:
        #     pass
        #
        # # Redirect to unauthorized page since the advisor does not have access to this student
        # else:
        #     return flask.redirect(flask.url_for('unauthorized'))

        # json = flask.request.get_json()
        # if json is not None:
        #     user_id = json.get('user')
        #     print(f'requesting advisor view of student {user_id}')
        #     return flask.redirect(flask.url_for('advisorViewingStudent'))
        pass


@app.route("/studentProfile/")
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_advisors  # you must be an advisor to view this page
def advisor_viewing_student():
    """
    This endpoint serves to provide advisors with a way to
    view the schedule and student profile of their advisee.

    Redirects to the unauthorized page if the advisor does
    not have access to the student they are requesting.
    """

    # Fetch the student the advisor is requesting to view the page of
    student_id = 123456  # TODO: fetch this value from the post result

    # Fetch the user id of the advisor performing this request
    advisor_id = flask_login.current_user.id

    # Fetch the student the advisor is requesting
    db = Database()
    student = db.get_student(student_id, advisor_id)
    db.close()

    # Ensure the advisor has access to this student within the database
    if student is not None:
        # Format the student's data into that which can be passed to the html template
        data = {
            'id': student.student_id,
            'name': f'{student.firstname} {student.lastname}',
            'credits': student.credits_completed,
            'email': student.email,
            'status': 1,    # TODO: populate this with their schedule status
            'year': student.classification,
            'major': None if not student.majors else student.majors[0][0],  # TODO: handle multiple majors
        }

        # TODO: decide if we want to stick with this old structure or adapt the html to work with the new
        data = {
            'id': student.student_id,
            'name': f'{student.firstname} {student.lastname}',
            'credits': student.credits_completed,
            'email': student.email,
            'status': 'Pending',
            'grad_semester': f'{student.graduation_semester} {student.graduation_year}',
            'major': None if not student.majors else student.majors[0][0],
        }

        # TODO: the following section needs review
        # Fetch the student's schedule from the database
        db = Database()
        schedule = db.get_template(1)
        db.close()

        # Serve the student overview page to the advisor performing the request
        return render_template('advisorViewingStudent.html', student=data, studentSchedule=schedule)

    # Redirect to the unauthorized page since the advisor does not have access to the requested student
    else:
        return login_manager.unauthorized()


@app.route('/advisorSchReview/')
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_advisors  # you must be an advisor to view this page
def advisor_sch_review():

    # TODO: verify that the advisor has access to this schedule
    # TODO: fetch the schedule information from the database
    
    """
    TODO
    1) get Prereqs from server
    2) Build prereq hierarchy with dataset attributes
    3) Special js function for first semester
    4) Build Pool of Prereqs met (include year standing)
    5) Check against pool for each class (User object? ask christian)
    """

    classes = [{'Semester': 'Fall', 'Year': 2020, 'Semester-Order': 0}, {'Semester': 'Spring', 'Year': 2021, 'Semester-Order': 1} , {'Semester': 'Fall', 'Year': 2021, 'Semester-Order': 2}, {'Semester': 'Spring', 'Year': 2022, 'Semester-Order': 3}]

    db = Database()

    status_sheet = db.getRequirements("COMPUTER SCIENCE", "2020")

    query_results = db.get_all_courses()

    list_of_courses = db.get_courses()
    
    return render_template(
        'advisorStudentScheduleReview.html', classes=classes, statusSheet=status_sheet, allCourses=query_results, listOfCourses=list_of_courses)



### STUDENT SPECIFIC ENDPOINTS ###

@flask_login.login_required
def get_student_data():
    # Fetch the student id of the requesting user
    current_user = flask_login.current_user
    student_id = current_user.id

    # Fetch the information about this student
    db = Database()
    student = db.get_student(student_id)
    db.close()

    # Fetch the information from the college if not cached
    if student is None:
        portal = MyGcc(current_user.username, current_user.password)
        profile = portal.profile

        student_name = profile.name

        enrolled = profile.enrolled_date
        enrolled_year = enrolled.split('/')[-1]
        enrolled_semester = 'Spring' if int(enrolled.split('/')[0]) < 7 else 'Fall'

        graduation = profile.planned_graduation
        graduation_year = graduation.split('/')[-1]
        graduation_semester = 'Spring' if int(graduation.split('/')[0]) < 7 else 'Fall'

        # TODO: actually fetch this rather than constructing it
        email = student_name['lastname'] + \
            student_name['firstname'][0] + \
            student_name['middlename'][0] + \
            enrolled_year[-2:] + '@gcc.edu'

        student = Student(
            student_id=current_user.id,
            advisor_id=None,
            firstname=student_name['firstname'],
            lastname=student_name['lastname'],
            email=email,
            majors=[(profile.major, int(enrolled_year))],
            classification=profile.classification,
            graduation_year=int(graduation_year),
            graduation_semester=graduation_semester,
            enrolled_year=int(enrolled_year),
            enrolled_semester=enrolled_semester)

        # Caching the new student data within the database
        db = Database()
        db.create_new_student(student)
        db.close()

    # Format the student data into something that can be passed to the html page
    data = {
        'id': student.student_id,
        'name': f'{student.firstname} {student.lastname}',
        'credits': student.credits_completed,
        'status': 'Pending',    # TODO: fetch this value
        'enrolled_semester' : student.enrolled_semester,
        'enrolled_year' : student.enrolled_year,
        'grad_semester' : student.graduation_semester,
        'grad_year' : student.graduation_year,
        'enrolled_semester_combined' : f'{student.enrolled_semester} {student.enrolled_year}',
        'grad_semester_combined' : f'{student.graduation_semester} {student.graduation_year}',

        'major': student.majors[0][0] if student.majors else None,  # TODO: add support for multiple majors
    }

    return data



@app.route('/studentData')
@security.restrict_to_students
@flask_login.login_required     # you must be logged in to view this page
def get_student_info_json():
    """
    Returns Student info JSON for logged in student
    """
    return jsonify(get_student_data())


@app.route('/studentLanding')
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_students  # you must be a student to view this page
def student_landing_page():
    """
    This endpoint serves to provide an overview to a specific student's
    academic scheduling information. This is the default landing page
    for students once they perform site login.
    """
    data = get_student_data()
    
    # TODO: this following section requires review
    # Fetch the student's schedule from the database
    db = Database()
    template = db.get_template(1)
    db.close()

    # Serve the formatted landing page to the student requesting this endpoint
    return render_template('studentLanding.html', student=data, studentSchedule=template)


@app.route('/studentSchReview/')
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_students  # you must be a student to view this page
def student_sch_review():

    # TODO: verify that the student has access to this schedule
    # TODO: fetch the schedule information from the database

    classes=["Fall 2021", "Spring 2022", "Fall 2022", "Spring 2021"]

    db = Database()

    status_sheet = db.getRequirements("COMPUTER SCIENCE", "2020")

    query_results = db.get_all_courses()

    list_of_courses = db.get_courses()
    
    return render_template(
        'advisorStudentScheduleReview.html', classes=classes, statusSheet=status_sheet, allCourses=query_results, listOfCourses=list_of_courses)


### UTILITY ENDPOINTS ###

@app.route('/searchClasses/')
@flask_login.login_required     # you must be logged in to access this endpoint
def search_classes():
    db = Database()
    class_name = request.args.get('class_name', 0, type=str)

    query_results = db.search_course_codes(class_name)

    return jsonify(query_results)


@app.route('/filterDuplicates/')
@flask_login.login_required     # you must be logged in to access this endpoint
def filter_duplicate_classes():
    db = Database()
    schedule_id = request.args.get('schedule_id', 0, type=int)
    query_results = db.filter_duplicates(schedule_id)
    return jsonify(query_results)


@app.route('/getRequirements/')
@flask_login.login_required     # you must be logged in to access this endpoint
def get_requirements():
    db = Database()
    major_name = request.args.get('major_name', 0, type=str)
    major_year = request.args.get('major_year', 0, type=int)

    query_results = db.getRequirements(major_name, major_year)

    return jsonify(query_results)

  
@app.route('/getRequisites/')
@flask_login.login_required     # you must be logged in to access this endpoint
def get_requisites():
    db = Database()

    query_results = db.getRequisites()

    return jsonify(query_results)


if __name__ == "__main__":
    # from webscraping.adviseescraper import AsyncAdviseeScraper
    # import getpass
    # username = input('Username: ')
    # password = getpass.getpass()
    # scraper = AsyncAdviseeScraper(username, password, lambda a: _)
    # scraper.start()
    app.run(debug=True)

# Having debug=True allows possible Python errors to appear on the web page
# run with $> python server.py
