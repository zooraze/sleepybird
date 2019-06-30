import datetime
import collections


class Analysis(object):

    # TODO(zooraze): move to utility class?
    def current_time(self):
        """Current date and time.

        Returns:
            string: YYYY-MM-DD HH:MM:SS
        """
        currentDT = datetime.datetime.now()

        return currentDT.strftime("%Y-%m-%d %H:%M:%S")

    # TODO(zooraze): reconsider what tokens consititute "words"
    # i.e. url, username, hashtag, etc.

    def count_words(self, words):
        """Total number of words in a list.

        Args:
            words (list): words to count
        Returns:
            integer
        """

        return len(words)

    def top_words(self, words, limit):
        """Most frequently occurring words.

        Args:
            words (list): words to parse
            limit (integer): number of words to report
        Returns:
            list
        """

        return collections.Counter(words).most_common(limit)
