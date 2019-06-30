import tweepy
import sleepybird.util


class TwitterBot(object):
    """
    Access tweets using the Twitter API and manipulate the results.

    Args:
        tweets (list): tweets to format
        query (:obj:`str`, optional): the query issued to API
    Attributes:
        tweepy_api (API): provide access to the twitter RESTful API
    """

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token=None,
                 access_token_secret=None):
        # Configure Twitter authorization
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        if ((access_token and access_token_secret) is not None):
            auth.set_access_token(access_token, access_token_secret)
        self.tweepy_api = tweepy.API(auth)

    def format_queried_tweets(self, tweets, query=None):
        """Format tweets acquired by querying the Twitter API.

        Args:
            tweets (iterator): tweets to format
            query (:obj:`str`, optional): the query issued to API
        Returns:
            :obj:`list` of :obj:`dict`
        """
        return [{'tweet': tweet.text,
                 'created_at': tweet.created_at,
                 'query': query,
                 'headshot_url': tweet.user.profile_image_url}
                for tweet in tweets]

    def get_user_tweets(self, username):
        """A single users tweets.

        Args:
            username (str): user to retrieve tweets from
        Returns:
            :obj:`list` of :obj:`dict`
        """
        tweets = self.tweepy_api.user_timeline(screen_name=username)
        return self.format_queried_tweets(tweets, username)

    def get_query_results(self, search_term, limit):
        """Retrieve up to 100 query results. Quickly but not reliably.

        Args:
            search_term (str): user to retrieve tweets from
            limit (int): number of results to retrieve
        Returns:
            :obj:`list` of :obj:`dict`
        """
        results = self.tweepy_api.search(q=search_term, count=limit)
        return self.format_queried_tweets(results, search_term)

    def get_cursor_results(self, search_term, limit):
        """Query results using cursor.

        Args:
            search_term (str): user to retrieve tweets from
            limit (int): number of results to retrieve
        Returns:
            :obj:`list` of :obj:`dict`
        """
        # TODO(zooraze): should clean data; might be losing words due to urls
        # TODO(zooraze): optimize; tweepy.Cursor is causing slowdown?
        results = tweepy.Cursor(self.tweepy_api.search,
                                q=search_term,
                                lang="en").items(limit)

        return self.format_queried_tweets(results, search_term)
