from flask import Flask, jsonify, request
from werkzeug.wrappers import response
import db
import pymongo
from scraper import AtlanticScraper, MediumScraper
from flask_apscheduler import APScheduler
import functools
import datetime

# set configuration values


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


def compare(a, b):

    aDate = a['date']
    bDate = b['date']
    aScore = a.get('score', 0)
    bScore = b.get('score', 0)

    if aDate.date() == bDate.date():

        if aScore > bScore:
            return -1
        elif aScore < bScore:
            return 1
        else:
            return 0

    elif aDate.date() > bDate.date():
        return -1
    else:
        return 1

# cron examples


@scheduler.task('cron', id='add_articles', hour='23')
def add_articles():

    print("Adding articles")

    atlanticScraper = AtlanticScraper()
    mediumScraper = MediumScraper()

    atlanticArticles = atlanticScraper.scrapeIt()
    mediumArticles = mediumScraper.scrapeIt()

    articles = atlanticArticles + mediumArticles

    for article in articles:

        # save this article if the title doesn't already exist in the database
        if db.db.articles.find_one({"title": article['title']}) is None:
            db.db.articles.insert_one(article)

    articles = sorted(list(db.db.articles.find()),
                      key=functools.cmp_to_key(compare))

    for i in range(len(articles)-1, len(articles)-10, -1):

        title = articles[i]['title']

        # Remove this article from db
        db.db.articles.delete_one({'title': title})

        # Add this article in model for ml
        db.db.bigData.insert_one({
            'title': title,
            'score': 0
        })

    print("Articles added")


@app.route("/get_articles", methods=['GET'])
def display():
    response = {'data': [], 'error': False, 'bookmarked': []}
    try:

        articles = sorted(list(db.db.articles.find()),
                          key=functools.cmp_to_key(compare))

        display_articles = []
        for i in range(10):

            display_articles.append({
                'title': articles[i]['title'],
                'description': articles[i]['description'],
                'date': articles[i]['date'],
                'img': articles[i].get('img', None),
                'url': articles[i]['url'],
            })

        response['data'] = display_articles

        b_articles = sorted(list(db.db.bookmarks.find()),
                            key=functools.cmp_to_key(compare))

        bookmarked_articles = []

        for i in range(min(10, len(b_articles))):
            bookmarked_articles.append({

                'title': b_articles[i]['title'],
                'description': b_articles[i]['description'],
                'date': b_articles[i]['date'],
                'img': b_articles[i].get('img', None),
                'url': b_articles[i]['url'],

            })

        response['bookmarked'] = bookmarked_articles

        return jsonify(response)
    except:
        response['error'] = True
        return jsonify(response)


@app.route("/get_article", methods=['POST'])
def getArticle():
    title = request.json['title']
    article = db.db.articles.find_one({'title': title})

    # update the score of this article
    db.db.articles.update_one(
        {'title': title},
        {'$inc': {'score': -100}}
    )

    # Add this article in model for ml
    db.db.bigData.insert_one({
        'title': title,
        'score': 1
    })

    responseArticle = {
        'title': article['title'],
        'description': article['description'],
        'date': article['date'],
        'content': article['content'],
        'url': article['url'],
        'img': article.get('img', None)
    }
    return jsonify(responseArticle)


@app.route("/get_bookmarked", methods=['POST'])
def getBookmarked():
    title = request.json['title']
    article = db.db.bookmarks.find_one({'title': title})

    responseArticle = {
        'title': article['title'],
        'description': article['description'],
        'date': article['date'],
        'content': article['content'],
        'url': article['url'],
        'img': article.get('img', None)
    }
    return jsonify(responseArticle)


@app.route("/reduce_score", methods=['GET'])
def reduceScore():
    articles = sorted(list(db.db.articles.find()),
                      key=functools.cmp_to_key(compare))
    for i in range(10):
        db.db.articles.find_one_and_update(
            {'title': articles[i]['title']}, {'$set': {'score': articles[i]['score']-1}})
    return "score_reduced"


@app.route("/save_bookmark", methods=['POST'])
def bookmark():
    try:
        title = request.json['title']
        bookmark_article = db.db.articles.find_one({'title': title})
        db.db.bookmarks.insert_one(bookmark_article)

        # delete this article from the articles collection
        db.db.articles.delete_one({'title': title})

        return "bookmarked"
    except:
        return "no such title"


@app.route("/test", methods=["GET"])
def test():
    response = {
        "data": "api is working",
        "error": None
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
