import flask
from flask import Flask,render_template, request, jsonify
import flask_login
from flask_login import login_required
from os import urandom
from user import User
from mygcc import MyGcc
from database import Database
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

@app.route('/login/', methods=['POST'])
def login_post():
    username = flask.request.form['username']
    password = flask.request.form['password']
    mygcc = MyGcc(username, password)
    try:
        mygcc.login()
        user_id = mygcc.profile.user_id
        is_advisor = mygcc.advising.is_advisor
        if user_id is not None:
            user = User(user_id, is_advisor, username, password)
            users[user.get_id()] = user
            flask_login.login_user(user)
            if is_advisor:
                return flask.redirect(flask.url_for("advisorHomePreview"))
            else:
                return flask.redirect(flask.url_for("advisorHomePreview"))
        else:
            print('Bad Login')
    except Exception as exception:
        print('Bad Login', exception)
	#TODO Replace this route handler with proper login credential handling
    return render_template('loginPage.html')

## ADVISOR SCHEDULE REVIEW ##
@app.route('/advisorSchReview/')
def advisorSchReview():
    classes=["Fall 2021","Spring 2022","Fall 2022","Spring 2021"]
    statusSheet=[
	{
		"title":"Humanities Core",
		"classes": ["c1", "c2", "c3"]

	},
    {
		"title":"SSFT Requirement",
		"classes": ["c1", "c2", "c3"]

	},
    {
		"title":"Writing Requirement",
		"classes": ["c1", "c2", "c3"]

	},
    {
		"title":"Foundations of Social Sciences",
		"classes": ["c1", "c2", "c3"]

	},
	{
		"title":"Physical Education",
		"classes": ["c1", "c2", "c3"]

	}
]
    return render_template('advisorStudentScheduleReview.html', classes=classes, statusSheet=statusSheet)


@app.route('/advisorHomePreview/')
def advisorHomePreview():
    advisees = [
        {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'email': 'example@gcc.edu', 'status': 1, 'year': 'Senior'},
        {'id': 207458, 'name': 'Steve Stevenson', 'credits': 50, 'email': 'example@gcc.edu', 'status': 2, 'year': 'Junior'},
        {'id': 206832, 'name': 'Linus Tech Tips', 'credits': 55, 'email': 'example@gcc.edu', 'status': 3, 'year': 'Sophomore'},
        {'id': 208776, 'name': 'Shel Silverstein', 'credits': 47, 'email': 'example@gcc.edu', 'status': 4, 'year': 'Freshman'},
    ]
    return render_template('advisorLandingPage.html', advisees=advisees)


@app.route('/studentLanding')
def studentLanding():
	student = [ {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'status': 'Pending', 'grad_semester': 'Spring 2024', 'major': 'Computer Science'} ]
	studentSchedule = [
		{
			'semester': 'Fall 2020',
			'classes': ['COMP 141', 'COMP 155', 'MATH 161', 'PHYS 101', 'HUMA 102']
		},
		{
			'semester': 'Spring 2021',
			'classes': ['COMP 220', 'MATH 162', 'PHYS 102', 'WRIT 101', 'PHYE 100']
		},
		{
			'semester': 'Fall 2021',
			'classes': ['COMP 222', 'COMP 244', 'MATH 213', 'HUMA 200', 'PSYC 101', 'General Elective']
		},
		{
			'semester': 'Spring 2022',
			'classes': ['COMP 205', 'COMP 233', 'COMP 342', 'MATH 214', 'HUMA 202']
		},
		{
			'semester': 'Fall 2022',
			'classes': ['COMP 325', 'COMP 422', 'COMP 390', 'COMP 401', 'HUMA 301', 'General Elective']
		},
		{
			'semester': 'Spring 2023',
			'classes': ['COMP 314', 'COMP 340', 'COMP 350', 'COMP 402', 'General Elective', 'General Elective']
		},
		{
			'semester': 'Fall 2023',
			'classes': ['COMP 448', 'COMP 451', 'COMP 435', 'HUMA 303', 'General Elective', 'General Elective']
		},
		{
			'semester': 'Spring 2024',
			'classes': ['COMP 443', 'COMP 452', 'COMP 441', 'General Elective', 'General Elective']
		}
	]
	return render_template('studentLanding.html', student=student, studentSchedule=studentSchedule)

@app.route("/studentProfile/")
def advisorViewingStudent():
	student = [ {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'status': 'Pending', 'grad_semester': 'Spring 2024', 'major': 'Computer Science'} ]
	studentSchedule = [
		{
			'semester': 'Fall 2020',
			'classes': ['COMP 141', 'COMP 155', 'MATH 161', 'PHYS 101', 'HUMA 102']
		},
		{
			'semester': 'Spring 2021',
			'classes': ['COMP 220', 'MATH 162', 'PHYS 102', 'WRIT 101', 'PHYE 100']
		},
		{
			'semester': 'Fall 2021',
			'classes': ['COMP 222', 'COMP 244', 'MATH 213', 'HUMA 200', 'PSYC 101', 'General Elective']
		},
		{
			'semester': 'Spring 2022',
			'classes': ['COMP 205', 'COMP 233', 'COMP 342', 'MATH 214', 'HUMA 202']
		},
		{
			'semester': 'Fall 2022',
			'classes': ['COMP 325', 'COMP 422', 'COMP 390', 'COMP 401', 'HUMA 301', 'General Elective']
		},
		{
			'semester': 'Spring 2023',
			'classes': ['COMP 314', 'COMP 340', 'COMP 350', 'COMP 402', 'General Elective', 'General Elective']
		},
		{
			'semester': 'Fall 2023',
			'classes': ['COMP 448', 'COMP 451', 'COMP 435', 'HUMA 303', 'General Elective', 'General Elective']
		},
		{
			'semester': 'Spring 2024',
			'classes': ['COMP 443', 'COMP 452', 'COMP 441', 'General Elective', 'General Elective']
		}
	]
	return render_template('advisorViewingStudent.html', student=student, studentSchedule=studentSchedule)


if __name__ == "__main__":
    app.run(debug=True)

# Having debug=True allows possible Python errors to appear on the web page
# run with $> python server.py

@app.route('/searchClasses/')
def searchClasses():
    DB = Database()
    class_name = request.args.get('class_name', 0, type=str)
    
    query_results = DB.search_course_codes(class_name)

    return(jsonify(query_results))

