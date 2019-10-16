import requests
import os
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

# url = 'https://www.w3schools.com/python/default.asp'
# Tuple unpacking
# scheme, netloc, path, *_ = urlparse(url)
# print(netloc)
# res = requests.get(url)
# print(res.status_code)
# print(res.encoding)
# soup = BeautifulSoup(res.text, "html.parser")
# Why cannot print this, unicode encoding error
# print(soup.prettify())

# print(soup.title.get_text())
# print(netloc + soup.select('link[href*="favicon.ico"]')[0].get('href'))

# Get images
# num = 0
# for img in soup.select('img'):
#     print(netloc + img.get('src'))
#     img_content = requests.get('http://' + netloc + img.get('src')).content
#     with open(f'./img/{num}.png', 'wb') as f:
#         f.write(img_content)
#     num = num + 1


class Crawler():
    def __init__(self, url):
        self.scheme, self.netloc, self.path, *_ = urlparse(url)
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")

    def get_title(self):
        return self.soup.title.get_text()

    def get_favicon(self):
        if len(self.soup.select('link[rel*="shortcut icon"]')) != 0:
            return self.netloc + self.soup.select('link[rel*="shortcut icon"]')[0].get('href')
        elif len(self.soup.select('link[href*="favicon.ico"]')) != 0:
            return self.netloc + self.soup.select('link[href*="favicon.ico"]')[0].get('href')
        else:
            return None

    def get_images(self):
        img_urls = []
        for img in self.soup.select('img'):
            # Is this cross platform?
            filename = os.path.basename(img.get('src'))
            img_urls.append(
                {'filename': filename, 'url': f'{self.scheme}://{self.netloc}' + img.get('src')})

        return img_urls

    def get_links(self):
        links = []
        for a in self.soup.select('a'):
            href = a.get('href')
            # Better way to check if is URL?
            if '/' in href:
                if self.netloc in href:
                    links.append(href)
                else:
                    links.append(f'{self.scheme}://{self.netloc}' + href)

        return links

    def get_h1(self):
        headers = []
        for h1 in self.soup.select('h1'):
            print(h1)
            headers.append(h1.get_text())

        return headers

    def get_h2(self):
        headers = []
        for h2 in self.soup.select('h2'):
            print(h2)
            headers.append(h2.get_text())

        return headers

    def get_h3(self):
        headers = []
        for h3 in self.soup.select('h3'):
            print(h3)
            headers.append(h3.get_text())

        return headers

    def get_p(self):
        paragraphs = []
        for p in self.soup.select('p'):
            print(p)
            paragraphs.append(p.get_text())

        return paragraphs


@app.route('/', methods=['GET'])
def crawl():
    url = request.args.get('url')
    print(url)
    my_crawler = Crawler(url)
    my_crawler.get_images()
    return {
        'title': my_crawler.get_title(),
        'favicon': my_crawler.get_favicon(),
        'images': my_crawler.get_images(),
        'links': my_crawler.get_links(),
        'h1': my_crawler.get_h1(),
        'h2': my_crawler.get_h2(),
        'h3': my_crawler.get_h3(),
        'p': my_crawler.get_p()
    }


# if __name__ == '__main__':
    # Do not use run() in production
    # app.run(debug=True)
