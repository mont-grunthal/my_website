from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/mixture")
def mixture():
    return render_template("mixture.html")

@app.route("/rocks")
def rocks():
    return render_template("rock_climbing.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")


if __name__ == "__main__":
    app.run(host = '0.0.0.0')
