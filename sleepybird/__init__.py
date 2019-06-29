from flask import Flask, render_template, json, request
from sleepybird.analysis import Analysis
from sleepybird.twitterbot import TwitterBot

# TODO(zooraze): move to utility class?
import itertools


app = Flask(__name__)
# Load configuration file
app.config.from_object('config')

# Pagination
page_size = app.config['PAGE_SIZE']
visible_page_count = app.config['VISIBLE_PAGE_COUNT']

# Twitter
consumer_key = app.config['TWITTER_CONSUMER_KEY']
consumer_secret = app.config['TWITTER_CONSUMER_SECRET']
access_token = app.config['TWITTER_ACCESS_TOKEN']
access_token_secret = app.config['TWITTER_ACCESS_TOKEN_SECRET']

twitterbot = TwitterBot(consumer_key, consumer_secret)
analysis = Analysis()

# Routes
@app.route('/search/<string:search_term>')
def search(search_term):
    limit = 30
    return render_template("search.html",
                           results=twitterbot.get_query_results(
                               search_term, limit),
                           search_term=search_term)


@app.route('/user/<string:username>')
def tweets(username):
    return render_template("tweets.html",
                           tweets=twitterbot.get_user_tweets(username),
                           username=username)


@app.route('/')
def root():
    # Twitter query
    search_term = request.args.get('q')
    # TODO(zooraze): should give an introduction when user arrives
    if search_term == None:
        search_term = 'test'
    tweet_limit = 15

    results = twitterbot.get_cursor_results(search_term, tweet_limit)

    # Gather words from all tweets
    report_limit = 10
    all_tweets = []

    for result in results:
        all_tweets.append(result.get('tweet'))
    list_of_word_lists = [tweet.lower().split() for tweet in all_tweets]
    word_list = list(itertools.chain(*list_of_word_lists))

    word_count = analysis.count_words(word_list)
    top_words_counter = analysis.top_words(word_list, report_limit)

    return render_template('index.html',
                           results=results,
                           search_term=search_term,
                           current_time=analysis.current_time(),
                           word_count=word_count,
                           top_words_counter=top_words_counter)
