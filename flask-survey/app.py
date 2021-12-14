from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

user_responses = []


@app.route("/")
def show_survey_start():
    """Select a survey."""
    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Start with 1 question"""
    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_questions(qid):
    """Show the question based on the id"""
    if (len(user_responses) != qid):
      flash(f"Invalid question id: {qid}.")
      return redirect(f"/questions/{len(user_responses)}")
    print("user_response", len(user_responses))
    
    if (len(user_responses) >= len(survey.questions)):
        # They've answered all the questions! Thank them.
        print(len(user_responses))
        return redirect("/complete")
   
    question = survey.questions[qid]
  
    return render_template("question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""
    # get the response choice
    choice = request.form['answer']
    # saving the answer on the server list
    user_responses.append(choice)

    if (len(user_responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(user_responses)}")

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")