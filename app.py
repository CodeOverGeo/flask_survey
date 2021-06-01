from flask import Flask, render_template, request, redirect
from surveys import satisfaction_survey
from logging import debug
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = 'swordfish'

debug = DebugToolbarExtension(app)

responses = []

title = satisfaction_survey.title
instructions = satisfaction_survey.instructions

@app.route('/')
def index():
    return render_template('index.html', title = title, instructions = instructions)

@app.route('/questions/<int:id>')
def ask_questions(id):
    question = satisfaction_survey.questions[id].question
    question_id = id + 1
    choice1 = satisfaction_survey.questions[id].choices[0]
    choice2 = satisfaction_survey.questions[id].choices[1]
    return render_template('questions.html', title = title, question = question, question_id = question_id, choice1 = choice1, choice2 = choice2)
