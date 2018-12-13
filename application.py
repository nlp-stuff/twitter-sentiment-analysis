from flask import Flask, redirect, render_template, request, url_for

import helpers
import os, sys
from analyzer import Analyzer, stupid_analyzer


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name.lstrip("@"), count = 10)
    # print(tweets, len(tweets))
    # if invalid or protected screen name
    if tweets == None:
        return redirect(url_for("index"))
    
    for tweet in tweets:
        tweet.update(stupid_analyzer(tweet['text']))


    return render_template("search1.html", tweets=tweets, screen_name=screen_name)




if __name__ == '__main__':
    app.run(port=5000, debug=True)