import flask
from flask import Flask,render_template, request, jsonify
import flask_login
from flask_login import login_required
from os import urandom
from user import User
from database import Database

from webscraping.mygcc import MyGcc
import webscraping.errors as errors
''' set app, cache time, and session secret key '''

#users dictionary
users = {}


app = Flask(__name__)
app.secret_key = urandom(16)

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # no cache
#app.config["SECRET_KEY"] = "!kn4fs%dkl#JED*BKS89" # Secret Key for Sessions

#set up login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#convert user id to a user object
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)





## LOGIN ##
@app.route('/')
@app.route('/login/', methods=['GET'])
def login_get():
    return render_template('loginPage.html')

@app.route('/', methods=['POST'])
@app.route('/login/', methods=['POST'])
def login_post():

    # fetch the username and password
    username = flask.request.form['username']
    password = flask.request.form['password']
    mygcc = MyGcc(username, password)

    try:
        # try to login to mygcc via the supplied credentials
        mygcc.login()

        # fetch the user's id and if they are an advisor
        user_id = mygcc.profile.user_id
        is_advisor = mygcc.advising.is_advisor

        if user_id is not None:
            user = User(user_id, is_advisor, username, password)
            users[user.get_id()] = user
            flask_login.login_user(user)
            if is_advisor:
                return flask.redirect(flask.url_for("advisorHomePreview"))
            else:
                return flask.redirect(flask.url_for("studentLanding"))
        else:
            # return to login if no user id was found
            return flask.redirect(flask.url_for('login_get'))

    except errors.LoginError:
        # return to login if the credentials were invalid
        return flask.redirect(flask.url_for('login_get'))

	#TODO Replace this route handler with proper login credential handling
    return render_template('loginPage.html')

@app.route('/logout', methods=['POST'])
def logout():
    # removes the user from the cache
    user = flask_login.current_user
    if user.get_id() in users:
        del users[user.get_id()]

    # logs out the user
    flask_login.logout_user()

    return flask.redirect(flask.url_for('login_get'))

## ADVISOR SCHEDULE REVIEW ##
@app.route('/advisorSchReview/')
def advisorSchReview():
    classes=["Fall 2021","Spring 2022","Fall 2022","Spring 2021"]

    DB = Database()
	
    statusSheet = DB.getRequirements("COMPUTER SCIENCE", "2020")

    query_results = DB.get_all_courses()

    return render_template('advisorStudentScheduleReview.html', classes=classes, statusSheet=statusSheet, allCourses=query_results)


@app.route('/advisorHomePreview/', methods=['GET', 'POST'])
def advisorHomePreview():
    if flask.request.method == 'POST':
        # json = flask.request.get_json()
        # if json is not None:
        #     user_id = json.get('user')
        #     print(f'requesting advisor view of student {user_id}')
        #     return flask.redirect(flask.url_for('advisorViewingStudent'))
        pass
    else:
        advisees = [
            {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'email': 'example@gcc.edu', 'status': 1, 'year': 'Senior', 'major': 'Major'},
            {'id': 207458, 'name': 'Steve Stevenson', 'credits': 50, 'email': 'example@gcc.edu', 'status': 2, 'year': 'Junior', 'major': 'Major'},
            {'id': 206832, 'name': 'Linus Tech Tips', 'credits': 55, 'email': 'example@gcc.edu', 'status': 3, 'year': 'Sophomore', 'major': 'Major'},
            {'id': 208776, 'name': 'Shel Silverstein', 'credits': 47, 'email': 'example@gcc.edu', 'status': 4, 'year': 'Freshman', 'major': 'Major'},
        ]
        return render_template('advisorLandingPage.html', advisees=advisees)


@app.route('/studentLanding')
def studentLanding():
	student = [ {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'status': 'Pending', 'grad_semester': 'Spring 2024', 'major': 'Computer Science'} ]
	db = Database()
	template = db.get_template(1)
	return render_template('studentLanding.html', student=student, studentSchedule=template)

@app.route("/studentProfile/")
def advisorViewingStudent():
	student = [ {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'status': 'Pending', 'grad_semester': 'Spring 2024', 'major': 'Computer Science'} ]
	db = Database()
	template = db.get_template(1)
	return render_template('advisorViewingStudent.html', student=student, studentSchedule=template)


@app.route('/searchClasses/')
def searchClasses():
    DB = Database()
    class_name = request.args.get('class_name', 0, type=str)

    query_results = DB.search_course_codes(class_name)

    return(jsonify(query_results))

@app.route('/getRequirements/')
def getRequirements():
	DB = Database()
	major_name = request.args.get('major_name', 0, type=str)
	major_year = request.args.get('major_year', 0, type=int)

	query_results = DB.getRequirements(major_name, major_year)

	return(jsonify(query_results))


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
