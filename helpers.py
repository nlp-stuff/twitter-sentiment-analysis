import html
import os
import plotly
import socket
import json
from twython import Twython
from twython import TwythonAuthError, TwythonError, TwythonRateLimitError

def chart(positive, negative, neutral):
    """Return a pie chart for specified sentiments as HTML."""

    # offline plot
    # https://plot.ly/python/pie-charts/
    # https://plot.ly/python/reference/#pie
    figure = {
        "data": [
            {
                "labels": ["positive", "negative", "neutral"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "rgb(0,255,00)",
                        "rgb(255,0,0)",
                        "rgb(255,255,0)"
                    ]
                },
                "type": "pie",
                "values": [positive, negative, neutral]
            }
        ],
        "layout": {
            "showlegend": True
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)

def get_user_timeline(screen_name, count=200):
    """Return list of most recent tweets posted by screen_name."""

    # ensure count is valid
    if count < 1 or count > 200:
        raise RuntimeError("invalid count")

    # ensure environment variables are set
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    if not os.environ.get("API_SECRET"):
        raise RuntimeError("API_SECRET not set")

    # get screen_name's most recent tweets
    # https://dev.twitter.com/rest/reference/get/users/lookup
    # https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    # https://github.com/ryanmcgrath/twython/blob/master/twython/endpoints.py
    try:
        twitter = Twython(os.environ.get("API_KEY"), os.environ.get("API_SECRET"))
        user = twitter.lookup_user(screen_name=screen_name)
        if user[0]["protected"]:
            return None
        tweets = twitter.get_user_timeline(screen_name=screen_name, count=count)

        tweets = _format_tweets(tuple(tweets))

        # print(json.dumps(tweets, indent=2))

        return tweets
    except TwythonAuthError as e:
        raise RuntimeError("invalid API_KEY and/or API_SECRET") from None
    except TwythonRateLimitError:
        raise RuntimeError("you've hit a rate limit") from None
    except TwythonError:
        return None


def _format_tweets(tweets):
    tweet_return = []

    for tweet in tweets:
        tweet_dict = {
            'text': html.unescape(tweet["text"].replace("\n", " ")),
            'created_at': tweet['created_at'],
            'coordinates': tweet['coordinates'],
            'id': tweet['id'],
            'lang': tweet['lang']
        }

        tweet_return.append(tweet_dict)

    return tweet_return