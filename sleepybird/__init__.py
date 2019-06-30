from flask import Flask, render_template, json, request
from flask_caching import Cache

import sleepybird.util
from sleepybird.analysis import Analysis
from sleepybird.twitterbot import TwitterBot
from sleepybird.pagination import Pagination
import itertools

app = Flask(__name__)
app.config.from_object('config')

cache = Cache(app)
twitterbot = TwitterBot(app.config['TWITTER_CONSUMER_KEY'],
                        app.config['TWITTER_CONSUMER_SECRET'])
analysis = Analysis()


# Routes
@app.route('/search/<string:search_term>')
def search(search_term):
    limit = 100
    return render_template("search.html",
                           results=twitterbot.get_query_results(
                               search_term, limit),
                           search_term=search_term)


@app.route('/user/<string:username>')
def tweets(username):
    return render_template("user.html",
                           tweets=twitterbot.get_user_tweets(username),
                           username=username)


@app.route('/')
def root():
    # Config
    tweet_limit = 1000

    # Twitter query
    search_term = request.args.get('q')

    if search_term == None or search_term == "":
        return render_template('welcome.html')

    results = cache.get(search_term)

    # TODO(zooraze): Log new queries to datastore
    if not results:
        results = twitterbot.get_cursor_results(search_term, tweet_limit)
        cache.set(search_term, results)

    # Gather words from all tweets
    report_limit = 10
    all_tweets = []

    for result in results:
        all_tweets.append(result.get('tweet'))
    list_of_word_lists = [tweet.lower().split() for tweet in all_tweets]
    word_list = list(itertools.chain(*list_of_word_lists))

    word_count = analysis.count_words(word_list)
    top_words_counter = analysis.top_words(word_list, report_limit)

    # Pagination
    # TODO(zooraze): Lazy load tweets for more responsive-feeling experience
    page = int(request.args.get('page', 1))
    tweet_count = len(all_tweets)
    data = range(tweet_count)
    pager = Pagination(page, tweet_count)
    pages = pager.get_pages()
    skip = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE']
    data_to_show = results[skip: skip + limit]

    return render_template('index.html',
                           pages=pages,
                           results=data_to_show,
                           search_term=search_term,
                           current_time=util.current_time(),
                           word_count=word_count,
                           top_words_counter=top_words_counter)
