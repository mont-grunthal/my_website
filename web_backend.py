#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, redirect, url_for, render_template


# In[ ]:


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", content = "testing")

@app.route("/mixture")
def mixture():
    return render_template("mixture.html")

@app.route("/rocks")
def rocks():
    return render_template("rock_climbing.html")
# In[ ]:


if __name__ == "__main__":
    app.run(debug = True)


# In[ ]:
