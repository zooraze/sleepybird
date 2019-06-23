# [START gae_python37_render_template]
import datetime

from flask import Flask, render_template, json, request
import tweepy

app = Flask(__name__)

# Load configuration file
app.config.from_object('config')

# Configure Twitter access
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])

tweepy_api = tweepy.API(auth)


def get_tweets(username):
    tweets = tweepy_api.user_timeline(screen_name=username)
    return [{'tweet': t.text,
             'created_at': t.created_at,
             'username': username,
             'headshot_url': t.user.profile_image_url}
            for t in tweets]


@app.route('/<string:username>')
def tweets(username):
    # 'tweets' is passed as a keyword-arg (**kwargs)
    # **kwargs are bound to the 'tweets.html' Jinja Template context
    return render_template("tweets.html", tweets=get_tweets(username))


@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
