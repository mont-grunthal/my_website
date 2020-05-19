#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, redirect, url_for, render_template


# In[ ]:


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/mixture")
def mixture():
    return render_template("mixture.html")

@app.route("/rocks")
def rocks():
    return render_template("rock_climbing.html")
# In[ ]:


if __name__ == "__main__":
    app.run()


# In[ ]: