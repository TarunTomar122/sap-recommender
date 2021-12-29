from flask import Flask,jsonify
from werkzeug.wrappers import response
import db
import pymongo
from scraper import AtlanticScraper, MediumScraper

app = Flask(__name__)


@app.route("/")
def home():

    atlanticScraper = AtlanticScraper()
    mediumScraper = MediumScraper()

    atlanticArticles = atlanticScraper.scrapeIt()
    mediumArticles = mediumScraper.scrapeIt()

    articles = atlanticArticles + mediumArticles

    for article in articles:

        # save this article if the title doesn't already exist in the database
        if db.db.articles.find_one({"title": article['title']}) is None:
            db.db.articles.insert_one(article)

    return "saved articles"

@app.route("/get_articles")
def display():
    response={'data':[],'error':False}
    try:
        articles=db.db.articles.find().sort([('date',pymongo.DESCENDING),('score', pymongo.DESCENDING)])
        
        display_articles=[]
        for i in range(10):
            
            display_articles.append({
                'title': articles[i]['title'],
                'description': articles[i]['description'],
                'date': articles[i]['date'],
                'content': articles[i]['content'],
                'url': articles[i]['url'],
                

            })
        response['data']=display_articles
        return (response)
    except :
        response['error']=True
        return jsonify(response)
        
@app.route("/reduce_score")
def reduceScore():
    articles=db.db.articles.find().sort([('date',pymongo.DESCENDING),('score', pymongo.DESCENDING)])
    for i in range(10):
        articles[i]['score']=-1
        db.db.articles.find_one_and_update({'title':articles[i]['title']},{ '$set':{'score':-1}})
    return "score_reduced"



if __name__ == '__main__':
    app.run()
