# flask utilities
import flask
from flask import Flask, render_template, request, jsonify
import flask_login

# internal utilities
from os import urandom
from user import User
from database import Database
import security

# data collection utilities
import webscraping.adviseescraper as advisee_scraper
from webscraping.components.student import Student
from webscraping.components.schedule import Schedule
from webscraping.components.course import Course
from webscraping.mygcc import MyGcc
import webscraping.errors as errors
from webscraping.backoff import exponential_backoff
from requests.exceptions import RequestException


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

@app.route('/advisorHomePreview/')
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_advisors  # you must be an advisor to view this page
def advisor_landing_page():
    """
    This endpoint serves to provide advisors an overview of all their
    advisee students. This is the default landing page that advisors
    get redirected to after performing site login.
    """

    # Fetch all of the student's this advisor is responsible for
    advisor = flask_login.current_user
    advisor_students = advisee_scraper.get_advisers_students(advisor.id, advisor.username, advisor.password)

    # Format all the user data into something we can pass into the html template
    with Database() as db:
        data = []

        for student in advisor_students:
            # Fetches the student's schedule status and defaults to awaiting creation
            schedule = db.get_student_schedule(student.student_id)
            schedule_status = schedule.status if schedule else 3

            data.append({
                'id': student.student_id,
                'name': f'{student.firstname} {student.lastname}',
                'credits': student.credits_completed,
                'email': student.email,
                'status': schedule_status,
                'year': student.classification,
                'major': None if not student.majors else student.majors[0][0],  # TODO: handle multiple majors
            })

    # Serve the advisor landing page template to the user
    return render_template('advisorLandingPage.html', advisees=data)


@app.route("/studentProfile/", methods=["POST"])
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
    student_form = flask.request.form
    student_id = student_form.get('student_id')
    if student_id is not None:
        student_id = int(student_id)

    # Fetch the user id of the advisor performing this request
    advisor_id = flask_login.current_user.id

    # Fetch the student the advisor is requesting
    with Database() as db:
        student = db.get_student(student_id, advisor_id)
        schedule = db.get_student_schedule(student_id)

    # Ensure the advisor has access to this student within the database
    if student is not None:

        # Format the student's data into that which can be passed to the html template
        data = {
            'id': student.student_id,
            'name': f'{student.firstname} {student.lastname}',
            'credits': student.credits_completed,
            'email': student.email,
            'status': schedule.status_str if schedule else 'Awaiting Student Creation',
            'grad_semester': f'{student.graduation_semester} {student.graduation_year}',
            'major': None if not student.majors else student.majors[0][0],
        }

        # TODO: needs review
        current_year = 2021
        current_semester = 'Spring'
        schedule_data = {'semester': current_semester, 'year': current_year, 'classes': []}

        if schedule is not None:
            for course in schedule.courses:
                if course.semester == current_semester and course.year == current_year:
                    if course.course_code not in schedule_data['classes']:
                        schedule_data['classes'].append(course.course_code)

        # Serve the student overview page to the advisor performing the request
        return render_template('advisorViewingStudent.html', student=data, studentSchedule=[schedule_data])

    # Redirect to the unauthorized page since the advisor does not have access to the requested student
    else:
        return login_manager.unauthorized()


@app.route('/advisorSchReview/', methods=['POST'])
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_advisors  # you must be an advisor to view this page
def advisor_sch_review():
    """
    This endpoint serves to provide advisors with a way to
    view and edit the schedule for one of their advisees.

    Redirects to the unauthorized page if the advisor does
    not have access to the student whose schedule is being edited.
    """

    # Fetch the input fields from the request form
    page_form = flask.request.form

    advisor_id = flask_login.current_user.id
    student_id = page_form.get('student_id')
    if student_id is not None:
        student_id = int(student_id)

    # Ensure the fields were filled out appropriately
    if student_id is not None:

        with Database() as db:
            student = db.get_student(student_id, advisor_id)
            schedule = db.get_student_schedule(student_id)
            major_name, major_year = student.majors[0] 


        # Make sure the advisor has access to this student's schedule
        if student is None:
            return login_manager.unauthorized()




        # TODO: make this page exist standalone from the student side

      

        with Database() as db:
             # TODO: [SP-78] this cannot be a hardcoded value
            # status_sheet = db.getRequirements(major_name, major_year)

            query_results = db.get_all_courses()
            list_of_courses = db.get_courses()

        return render_template(
            'advisorStudentScheduleReview.html',
            student_id=student_id,
            allCourses=query_results,
            listOfCourses=list_of_courses)



### STUDENT SPECIFIC ENDPOINTS ###

# Exponential backoff required due to an occasional domain resolution failure.
@exponential_backoff(RequestException, retries=5, timeslot=0.5)
def scrape_student_data(__student_id, __username, __password):
    """ Builds a student object of the student who's credentials are passed in.

    :param __student_id:    student's unique identifier
    :param __username:      student's https://my.gcc.edu username
    :param __password:      student's https://my.gcc.edu password
    :return: the student object containing the student's data
    """

    profile = MyGcc(__username, __password).profile

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
        student_id=__student_id,
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

    return student


@flask_login.login_required
def get_student_data():
    # Fetch the student id of the requesting user
    current_user = flask_login.current_user
    student_id = current_user.id

    # Fetch the information about this student
    with Database() as db:
        student = db.get_student(student_id)
        schedule = db.get_student_schedule(student_id)

    # Fetch the information from the college if not cached
    if student is None:
        student = scrape_student_data(student_id, current_user.username, current_user.password)

        # Caching the new student data within the database
        db = Database()
        db.create_new_student(student)
        db.close()

    # Format the student data into something that can be passed to the html page
    data = {
        'id': student.student_id,
        'name': f'{student.firstname} {student.lastname}',
        'credits': student.credits_completed,
        'status': schedule.status_str if schedule else 'Awaiting Student Creation',
        'enrolled_semester': student.enrolled_semester,
        'enrolled_year': student.enrolled_year,
        'grad_semester': student.graduation_semester,
        'grad_year': student.graduation_year,
        'enrolled_semester_combined': f'{student.enrolled_semester} {student.enrolled_year}',
        'grad_semester_combined': f'{student.graduation_semester} {student.graduation_year}',
        'majors': [],
        # 'major_name': student.majors[0][0],
        # 'major_year': student.majors[0][1],
        # 'major': student.majors[0][0] if student.majors else None,  # TODO: add support for multiple majors
    }

    for major in student.majors:
        data['majors'].append({
            'major_name': major[0],
            'major_year': major[1]
        })

    return data


@app.route('/studentData')
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_students  # you must be a student to view this page
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
    student_id = flask_login.current_user.id
    data = get_student_data()

    with Database() as db:
        schedule = db.get_student_schedule(student_id)

        if not schedule.courses:
            # load and save template schedule
            student_majors = db.get_student_majors(student_id)
            
            major_name, major_year = student_majors[0]

            major_code = db.get_major_code(major_name, major_year)

            template = db.get_template(major_code[0])

            # status 3 = Awaiting Student Creation
            schedule = Schedule(student_id=student_id, status=3, courses=[])

            for semester in template:
                for course_code in semester["classes"]:
                    schedule.courses.append(db.get_course(course_code, semester["year"], semester["semester"]))

            # save schedule to db
            db.update_student_schedule(schedule)

            # save schedule status "awaiting student creation" to db
            db.setStudentStatus(student_id, 3)
    
    semesters = ['January', 'Spring', 'May', 'Summer', 'Fall', 'Winter Online']
    schedule_data = []

    for year in range(data['enrolled_year'], data['grad_year'] + 1):
        for sem in semesters:
            classes = []
            for course in schedule.courses:
                if course.semester.lower() == sem.lower() and course.year == year:
                    classes.append(course.course_code)

            if classes:
                schedule_data.append({'semester': sem, 'year': year, 'classes': classes})
                
    # if schedule is not None:
    #     for course in schedule.courses:
    #         if course.semester == current_semester and course.year == current_year:
    #             if course.course_code not in schedule_data['classes']:
    #                 schedule_data['classes'].append(course.course_code)

    # Serve the formatted landing page to the student requesting this endpoint
    return render_template('studentLanding.html', student=data, studentSchedule=schedule_data)


@app.route('/studentSchReview/')
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_students  # you must be a student to view this page
def student_sch_review():

    student_id = flask_login.current_user.id
    with Database() as db:
        student = db.get_student(student_id)
        schedule = db.get_student_schedule(student_id)
        status = schedule.status
        courses = schedule.courses
        
    json_courses = [{'course_code' : c.course_code,
                     'name' : c.name,
                     'year': c.year,
                     'semester':c.semester
                     }for c in courses]

    db = Database()

   
    query_results = db.get_all_courses()

    list_of_courses = db.get_courses()

    return render_template(
        'advisorStudentScheduleReview.html',        
        allCourses=query_results,
        studentStatus=status,
        listOfCourses=list_of_courses,
        StudentCourses = json_courses)


@app.route('/studentSchReview/', methods=["POST"])
@flask_login.login_required     # you must be logged in to view this page
@security.restrict_to_students  # you must be a student to view this page
def student_sch_review_post():
    data = request.json
    # print("\n\n",data)
    changed = data["changed"]
    courses = data["courses"]
    student_id = flask_login.current_user.id

    with Database() as db:
        schedule = db.get_student_schedule(student_id)
        if(schedule.status == 4):
            db.setStudentStatus(student_id, 1)
        elif(schedule.status == 3):
            if(changed):
                db.setStudentStatus(student_id, 1)
            else:
                db.setStudentStatus(student_id, 4)
        elif(schedule.status == 2):
            db.setStudentStatus(student_id, 1)
        elif(schedule.status == 1):
            db.setStudentStatus(student_id, 1)
        else:
            db.setStudentStatus(student_id, 2)

        db.clearStudentSchedule(student_id)
        for course in courses:
            db.addCourseToStudentSchedule(student_id, course["course_code"], course["semester"], course["year"])
            # print("\nLINE:", student_id, course)
    return jsonify({"success":1}), 200

### UTILITY ENDPOINTS ###

@app.route('/searchClasses/')
@flask_login.login_required     # you must be logged in to access this endpoint
def search_classes():
    with Database() as db:
        class_name = request.args.get('class_name', 0, type=str)
        query_results = db.search_course_codes(class_name)
    return jsonify(query_results)


@app.route('/filterDuplicates/')
@flask_login.login_required     # you must be logged in to access this endpoint
def filter_duplicate_classes():
    with Database() as db:
        schedule_id = request.args.get('schedule_id', 0, type=int)
        query_results = db.filter_duplicates(schedule_id)
    return jsonify(query_results)

@app.route('/filterSemester/')
@flask_login.login_required
def filter_semester():
    with Database() as db:
        semester = request.args.get('semester', 0, type=str)
        query_results = db.get_courses_by_semester(semester)
    return jsonify(query_results)


@app.route('/getRequirements/')
@flask_login.login_required     # you must be logged in to access this endpoint
def get_requirements():
    student_id = request.args.get('id', 0, type=str)

    # print(major_name,major_year)

    with Database() as db:
        query_results = db.getRequirements(student_id)
        # print(query_results)
    return jsonify(query_results)


@app.route('/getRequisites/')
@flask_login.login_required     # you must be logged in to access this endpoint
def get_requisites():
    with Database() as db:
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
