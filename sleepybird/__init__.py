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


def get_user_tweets(username):
    """Tweets for a given user."""
    tweets = tweepy_api.user_timeline(screen_name=username)
    return [{'tweet': tweet.text,
             'created_at': tweet.created_at,
             'username': username,
             'headshot_url': tweet.user.profile_image_url}
            for tweet in tweets]


def get_query_results(search_term):
    """Query results."""
    results = tweepy_api.search(q=search_term, count=30)
    return [{'tweet': result.text,
             'created_at': result.created_at,
             'username': search_term,
             'headshot_url': result.user.profile_image_url}
            for result in results]


def get_paginated_results(search_term):
    """Paginated query results."""
    tweet_limit = 1000
    paginated_tweets = [status for status in tweepy.Cursor(
        tweepy_api.search, q=query).items(tweet_limit)]
    results = tweepy_api.search(q=search_term, count=30)
    return [{'tweet': result.text,
             'created_at': result.created_at,
             'username': search_term,
             'headshot_url': result.user.profile_image_url}
            for result in results]


@app.route('/search/<string:search_term>')
def search(search_term):
    return render_template("search.html",
                           results=get_query_results(search_term),
                           search_term=search_term)


@app.route('/user/<string:username>')
def tweets(username):
    return render_template("tweets.html",
                           tweets=get_user_tweets(username),
                           username=username)


@app.route('/')
def root():
    search_term = request.args.get('q')
    if search_term == None:
        search_term = 'test'
    return render_template('index.html',
                           results=get_query_results(search_term),
                           search_term=search_term)
