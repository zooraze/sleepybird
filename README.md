# sleepybird
Lightweight Flask application for accessing the Twitter API.

[![Build Status](https://travis-ci.org/zooraze/sleepybird.svg?branch=master)](https://travis-ci.org/zooraze/sleepybird)

## Features
* Search box to query against Twitter's search API
* Pagination (currently 1000 result limit)
* Count every word in every tweet
* Report top 10 words across all results
* Log all queries, as well as timestamps and reports [WIP]

## Local testing
```python main.py```

## Deploy
Make a copy of config_dist.py as config.py. In config.py, enter the Twitter API access information.

### Google Cloud
```gcloud app deploy```

## 3rd Party Libraries
[Flask](http://flask.pocoo.org/): Python microframework for the back-end

[Tweepy](https://www.tweepy.org/): Python library for simplifying Twitter API access 

[Bootstrap](https://getbootstrap.com/): front-end component library

[Sphinx](http://www.sphinx-doc.org/en/master/): generate documentation. [WIP]
