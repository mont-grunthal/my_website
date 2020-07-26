from flask import Flask, redirect, url_for, render_template, request
import crawler

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

@app.route("/CatTwitter", methods = ["POST","GET"])
def Cat_Twitter():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user",usr = user))
    else:
        return render_template("Cat_Twitter.html")

@app.route("/<usr>", methods=['GET', 'POST'])
def user(usr):
    username = usr
    return render_template("CNN.html",cat_path = crawler.driver(username,consumer_key,consumer_secret,access_token,access_secret))

if __name__ == "__main__":
    app.run(debug = True)
