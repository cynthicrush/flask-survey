from flask import Flask, request, render_template, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh_secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    """Show title and instructions on the root """
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def start():
    """Start the survey"""
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')



@app.route('/questions/<int:id>')
def show_question(id):
    """Show question on the page"""
    responses = session.get(RESPONSES_KEY)
    if responses is None:
        return redirect('/')

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/completed')

    if(len(responses) != id):
        flash(f'Invalid question')
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[id]
    return render_template('question.html', question=question, question_id=id)


@app.route('/answer', methods=['POST'])
def save_response():
    """Save responses and redirect to question"""
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/completed')

    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/completed')
def completed():
    """Show completed page"""
    return render_template('completed.html')
