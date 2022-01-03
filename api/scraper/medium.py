from bs4 import BeautifulSoup as BeautifulSoup
import requests
import datetime


class MediumScraper:

    urls = ["https://medium.com/tag/tech/latest", "https://medium.com/tag/tech/",
            # "https://medium.com/tag/programming", "https://medium.com/tag/programming/latest",
            # "https://medium.com/tag/innovation", "https://medium.com/tag/innovation/latest",
            # "https://medium.com/tag/startups", "https://medium.com/tag/startups/latest",
            # "https://medium.com/tag/lifelessons", "https://medium.com/tag/lifelessons/latest",
            # "https://medium.com/tag/design", "https://medium.com/tag/design/latest",
            # "https://medium.com/tag/business", "https://medium.com/tag/business/latest",
            # "https://medium.com/tag/articles/latest", "https://medium.com/tag/articles/",
            # "https://medium.com/tag/writing", "https://medium.com/tag/writing/latest",
            # "https://medium.com/tag/life", "https://medium.com/tag/life/latest",
            # "https://medium.com/tag/life-hacks", "https://medium.com/tag/life-hacks/latest",
            # "https://medium.com/tag/creativity", "https://medium.com/tag/creativity/latest",
            # "https://medium.com/tag/productivity", "https://medium.com/tag/productivity/latest",
            ]
    articlesData = []

    def scrapeIt(self):

        for temp_url in self.urls:

            data = requests.get(temp_url)
            soup = BeautifulSoup(data.content, 'html.parser')

            articles = soup.findAll('div', {"class": "el l"})

            links = []

            for i in articles:
                try:
                    url = i.a.get('href')
                    if url[0] == '/':
                        url = 'https://medium.com' + url
                    links.append(url)
                except:
                    pass

            for link in links:

                try:

                    data = requests.get(link)
                    soup = BeautifulSoup(data.content, 'lxml')

                    ssoup = BeautifulSoup(data.content, 'html.parser')
                    title = ssoup.findAll('h1')[0].get_text()
                    img = ssoup.findAll('img')[0].get('src')

                    article = ssoup.findAll('article')[0]
                    # print(article)

                    i = 0

                    storage = ""

                    for something in article:
                        if i == 2:

                            title = something.find('h1').get_text()

                            divs = something.findAll('div')[0]

                            section = divs.findAll('section')[0]

                            divss = section.findAll('div')[0]

                            divsss = divss.findAll('div')[0]

                            for item in divsss:
                                if item.name == 'p':

                                    storage += " \n" + item.get_text() + " \n"

                                # elif item.name == 'img' or item.name == 'fig':
                                #     storage += 'II' + item.get('src') + "\n"

                                elif item.name == 'h1':

                                    storage += "\n# " + item.get_text() + " \n"

                                elif item.name == 'h2':

                                    storage += "\n# " + item.get_text() + " \n"

                                elif item.name == 'h3':

                                    storage += "\n# " + item.get_text() + " \n"

                        i += 1

                    if(len(storage) > 400):

                        self.articlesData.append({
                            'title': title,
                            'img': img,
                            'content': storage,
                            'url': link,
                            'description': storage[:200],
                            'date': datetime.datetime.now(),
                            'score':0,
                        })

                except:
                    pass

        return self.articlesData
