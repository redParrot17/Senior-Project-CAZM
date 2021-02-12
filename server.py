from flask import Flask,render_template

''' set app, cache time, and session secret key '''
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # no cache
app.config["SECRET_KEY"] = "!kn4fs%dkl#JED*BKS89" # Secret Key for Sessions

@app.route('/')
def index():
    return render_template('index.html', sample_value='Purple Unicorns!')


## LOGIN ##
@app.route('/login/', methods=['GET'])
def login_get():
    return render_template('loginPage.html')

@app.route('/login/', methods=['POST'])
def login_post():

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


@app.route('/advisorHomePreview')
def advisorHomePreview():
    advisees = [
        {'id': 209123, 'name': 'Sally Silly', 'credits': 54, 'email': 'example@gcc.edu', 'status': 1, 'year': 'Senior'},
        {'id': 207458, 'name': 'Steve Stevenson', 'credits': 50, 'email': 'example@gcc.edu', 'status': 2, 'year': 'Junior'},
        {'id': 206832, 'name': 'Linus Tech Tips', 'credits': 55, 'email': 'example@gcc.edu', 'status': 3, 'year': 'Sophomore'},
        {'id': 208776, 'name': 'Shel Silverstein', 'credits': 47, 'email': 'example@gcc.edu', 'status': 4, 'year': 'Freshman'},
    ]
    return render_template('advisorLandingPage.html', advisees=advisees)


if __name__ == "__main__":
    app.run(debug=True)

# Having debug=True allows possible Python errors to appear on the web page
# run with $> python server.py
