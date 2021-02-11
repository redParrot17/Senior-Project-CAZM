from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', sample_value='Purple Unicorns!')

@app.route('/login/')
def login():
    return render_template('loginPage.html')

@app.route('/advisorSchReview/')
def advisorSchReview():
    return render_template('advisorStudentScheduleReview.html')
