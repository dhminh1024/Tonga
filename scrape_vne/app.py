from flask import Flask, render_template

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://vnexpress.net/'

app = Flask(__name__)

def get_url(URL):
    """Get HTML from URL
    """
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def crawl_vnexpress(URL):
    soup = get_url(URL)
    articles = soup.find_all('article', class_='list_news')
    data = []
    for article in articles:
        d = {'title':'', 'link':'', 'image_url':'', 'description':''}
        try:
            d['title'] = article.a.string
            d['link'] = article.a['href']
            d['description'] = article.p.text
            if article.img:
                d['image_url'] = article.img['data-original']
        except:
            pass
        data.append(d)
    return data

@app.route('/')
def index():
    data = crawl_vnexpress(BASE_URL)
    return render_template('home.html', data=data)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 