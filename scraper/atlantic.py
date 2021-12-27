from bs4 import BeautifulSoup   # For HTML parsing
import requests            # For HTTP requests
import re

urls = [
    "https://www.theatlantic.com/latest/",
    "https://www.theatlantic.com/most-popular/",
    "https://www.theatlantic.com/technology/",
    "https://www.theatlantic.com/science/",
    "https://www.theatlantic.com/projects/",
    "https://www.theatlantic.com/international/",
    "https://www.theatlantic.com/ideas/",
]


for url in urls:

    data = requests.get(url)

    # Parse the response
    soup = BeautifulSoup(data.text, "html.parser")
    articles = soup.findAll('li',{'class': 'LandingRiver_li__Db7WD'})

    articlesData = []

    for article in articles:
        try:

            d={}
            d['title']=article.find('h2',{'class': 'LandingRiver_title__4ibQ4'}).get_text()
            d['url']=article.find('a',{'class':'LandingRiver_titleLink__WHlTC'}).get('href')
            # d['image']=article.find('img').get('href')   
            d['description']=article.find('p',{'class':'LandingRiver_dek__u9vaI'}).get_text()
            # Make a request to article url
            content=requests.get(d.get('url'))
            # Get the soup object from the request text
            article_soup = BeautifulSoup(content.text, "html.parser")
            # Search for all the paragraphs and append the text of the paragraphs to a string
            paragraphs=article_soup.findAll('p',{'class': 'ArticleParagraph_root__wy3UI'})
            art_cont=''
            for para in paragraphs:
                art_cont += '\n' + para.get_text() + "\n"
            # Save it in the dictionary as the article content
            d['content']=art_cont

            articlesData.append(d)

            name =  re.sub(r'[^\w\s]','',d['title'])

            file_name = "./files/"+name+".txt"
            with open(file_name, 'w') as tf:
                tf.write(d['content'])

        except:
            pass
