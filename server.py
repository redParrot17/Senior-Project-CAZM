from flask import Flask,render_template

''' set app, cache time, and session secret key '''
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # no cache
app.config["SECRET_KEY"] = "!kn4fs%dkl#JED*BKS89" # Secret Key for Sessions

@app.route('/')
def index():
    return render_template('index.html', sample_value='Purple Unicorns!')

@app.route('/login/')
def login():
    return render_template('loginPage.html')

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


if __name__ == "__main__":
    app.run(debug=True)

# Having debug=True allows possible Python errors to appear on the web page
# run with $> python server.py
