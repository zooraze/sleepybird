import tweepy


class TwitterBot(object):
    tweepy_api = None

    def __init__(self, consumer_key, consumer_secret, access_token=None, access_token_secret=None):
        """Setup application-only access."""
        # Configure Twitter access
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        if ((access_token and access_token_secret) is not None):
            auth.set_access_token(access_token, access_token_secret)
        self.tweepy_api = tweepy.API(auth)

    def get_user_tweets(self, username):
        """A single users tweets."""
        tweets = self.tweepy_api.user_timeline(screen_name=username)
        return [{'tweet': tweet.text,
                 'created_at': tweet.created_at,
                 'username': username,
                 'headshot_url': tweet.user.profile_image_url}
                for tweet in tweets]

    def get_query_results(self, search_term, limit):
        """Query results."""
        results = self.tweepy_api.search(q=search_term, count=limit)
        return [{'tweet': result.text,
                 'created_at': result.created_at,
                 'username': search_term,
                 'headshot_url': result.user.profile_image_url}
                for result in results]

    def get_cursor_results(self, search_term, limit):
        """Paginated query results."""
        # TODO(zooraze): optimize; tweepy.Cursor is causing a huge slowdown
        results = tweepy.Cursor(self.tweepy_api.search,
                                               q=search_term,
                                               lang="en").items(limit)

        return [{'tweet': result.text,
                 'created_at': result.created_at,
                 'username': search_term,
                 'headshot_url': result.user.profile_image_url}
                for result in results]
