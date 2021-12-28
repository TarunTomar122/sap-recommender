from flask import Flask
import db

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


if __name__ == '__main__':
    app.run()
