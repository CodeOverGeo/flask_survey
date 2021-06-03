from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = 'swordfish'

debug = DebugToolbarExtension(app)

# responses = []


title = satisfaction_survey.title
instructions = satisfaction_survey.instructions

@app.route('/')
def index():
    """Route home traffic to index.html, passing in title and instructions from constructed Class object"""
    return render_template('index.html', title = title, instructions = instructions)

@app.route('/questions/<int:id>')
def ask_questions(id):
    """Handle answered questions after POST routes sets session data to cookie"""
    responses = session.get('responses')
    if (responses is None):
        #If no questions have been answered, send to index.html
        return redirect('/')
    if (len(responses) == len(satisfaction_survey.questions)):
        #if all questions have been answered, send to thanks.html
        return render_template('thanks.html', title = title)
    elif (len(responses) == id): 
        #if the number of responses in the cookie match the id of the question, get the new question and display the 
        #questions and choices on the page
        question = satisfaction_survey.questions[id].question
        question_id = id + 1
        choice1 = satisfaction_survey.questions[id].choices[0]
        choice2 = satisfaction_survey.questions[id].choices[1]
        return render_template('questions.html', title = title, question = question, question_id = question_id, choice1 = choice1, choice2 = choice2)
    else:
        #If the user tries to go out of turn, flash error instructions and redirect to next question
        id = len(responses) +1
        flash(f"Please follow question order! Answer question {id}")
        return redirect(f'/questions/{id}')

@app.route('/answer', methods=['POST'])
def post_answer():
    """Handle answers to questions by POSTing data to cookie in session list"""    
    answer = request.form['question']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    if len(responses) == len(satisfaction_survey.questions):
        #once user has answered all questions, send to thank you page
        return render_template('thanks.html', title = title)
    else:
        #If user has not answered all questions, send to next question
        num_answered = len(responses)
        return redirect(f'/questions/{num_answered}')

@app.route('/set_session', methods=['POST'])
def set_session():
    #clear session cookie when starting survey
    session['responses'] = []
    return redirect('/questions/0')