import collections


class Analysis(object):
    """Analyze tweets."""

    # TODO(zooraze): reconsider what tokens consititute "words"
    # i.e. url, username, hashtag, etc.

    def count_words(self, words):
        """Total number of words in a list.

        Args:
            words (list): words to count
        Returns:
            int
        """

        return len(words)

    def top_words(self, words, limit):
        """Most frequently occurring words.

        Args:
            words (list): words to parse
            limit (int): number of words to report
        Returns:
            list
        """

        return collections.Counter(words).most_common(limit)
