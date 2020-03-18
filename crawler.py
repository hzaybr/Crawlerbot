import requests
import re
from bs4 import BeautifulSoup
from sys import modules

#url = 'https://inside.com.tw/article/18241-2019ESUN-FHC-fintech-talent2'
#url = 'https://www.businessweekly.com.tw/magazine/Article_mag_page.aspx?id=7000834'
#url = 'https://www.nownews.com/news/20191229/3849441/?fbclid=IwAR1za3nsGizFooNTEe__my0knMZWLPdZ7Gt-xL_YSSS1emA9PppoQRr2XwI'
#url = 'https://www.bnext.com.tw/article/56060/itts-teco-group-history--ipo-event?fbclid=IwAR3xToVkFYYSjxDZ06xzsXiAJEzCEaBhCHB5QeCiJSpFM71x9Zn5zNKtBZc'
def crawler(url, toFile=True):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    match = re.search(r'(bnext)|(nownews)|(businessweekly)|(inside)', url)
    if match:
        title, content, keywords = getattr(modules['crawler'], match.group())(soup)
        return title, content, keywords
        if toFile:
            write(title, content, keywords)
    else:
        pass

def nownews(soup):
    title = soup.find(class_ = 'entry-title').text
    article = soup.find(itemprop = 'articleBody').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = []
    key = soup.find(class_ = 'td-tags td-post-small-box clearfix').contents
    for k in key[1:]:
        keywords.append(k.text)
    return title, content, keywords

def bnext(soup):
    title = soup.find(class_ = 'article_title bitem_title').text
    article = soup.find(itemprop = 'articleBody').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = soup.find(class_ = 'article_tags').text.split('\n')
    return title, content, keywords

def businessweekly(soup):
    title = soup.find('header', class_ = 'headline').text
    article = soup.find(class_ = 'articlebody').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = soup.find(class_ = 'tag clearfix').text.split('\n')
    return title, content, keywords

def inside(soup):
    title = soup.find('h1').text
    article = soup.find(itemprop = 'articleBody').find_all(['h3', 'p'])
    content = '\n'.join([p.text for p in article])
    keywords = []
    key = soup.find(class_ = 'content').find_all(class_ = 'hero_slide_tag')
    for k in key:
        keywords.append(k.text)
    return title, content, keywords

def write(title, content, keywords):
    with open('nn.txt','w')as f:
        print(title + '\n---\n' + content + '\n===\n')
        f.write(title + '\n---\n' + content + '\n===\n')
        for keyword in keywords:
            print(keyword)
            f.write(keyword + ' ')

if '__main__' == __name__:
    crawler(url)
