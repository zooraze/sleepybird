# sleepybird
Single-page application skeleton for accessing the Twitter API.

## Features
* Search box to query against Twitter's search API [WIP]
* Pagination (currently 1000 result limit) [WIP]
* Count every word in every tweet
* Report top 10 words across all results [WIP]
* Log all queries, as well as timestamps and reports

## Local testing
```python main.py```

## Deploy
Make a copy of config_dist.py as config.py. In config.py, enter the Twitter API access information.
```gcloud app deploy```

## 3rd Party Libraries
[Flask](http://flask.pocoo.org/): Python microframework for the back-end [WIP]

[Tweepy](https://www.tweepy.org/): Python library for simplifying Twitter API access [WIP]

[Bootstrap](https://getbootstrap.com/): front-end component library [WIP]

[Sphinx](http://www.sphinx-doc.org/en/master/): generate documentation. [WIP]
