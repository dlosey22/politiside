from flask import Flask
from flask import render_template
from flask import send_from_directory
app = Flask("politisides", static_folder='styles')


@app.route('/')
def hello_world():
    with open("templates/today.html", "r") as f:
        a = f.read()
    return render_template("home.html")

@app.route('/files/today.html')
def files():
    return render_template("today.html")
@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")
@app.route("/styles/<path:file>")
def styles(file):
    print(file)
    return send_from_directory(app.static_folder,file)

@app.route("/about")
def channels():
    return render_template("about.html")
app.run(debug=True)
