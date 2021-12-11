from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import story

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    """Return homepage."""
    return render_template("hello.html")

@app.route('/form')
def show_form():
    """Show story form."""
    prompts = story.prompts
    return render_template("form.html", prompts=prompts)

@app.route('/story')
def show_story():
    """Show story."""
    text = story.generate(request.args)
    print(request.args)
    return render_template("story.html", text=text)
   