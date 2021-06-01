from flask import Flask, render_template, request, redirect, flash
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
    if len(responses) == len(satisfaction_survey.questions):
        return render_template('thanks.html', title = title)
    elif len(responses) == id: 
        question = satisfaction_survey.questions[id].question
        question_id = id + 1
        choice1 = satisfaction_survey.questions[id].choices[0]
        choice2 = satisfaction_survey.questions[id].choices[1]
        return render_template('questions.html', title = title, question = question, question_id = question_id, choice1 = choice1, choice2 = choice2)
    else:
        flash("Please follow question order!")
        id = len(responses)
        return redirect(f'/questions/{id}')

@app.route('/answer', methods=['POST'])
def post_answer():
    answer = request.form['question']
    responses.append(answer)
    if len(responses) == len(satisfaction_survey.questions):
        return render_template('thanks.html', title = title)
    else:
        num_answered = len(responses)
        return redirect(f'/questions/{num_answered}')