import requests
import re
from bs4 import BeautifulSoup
from sys import modules

def crawler(url, toFile=True):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    match = re.search(r'(medium\.com)|(aiacademy)|(blocktempo)|(gartner)|(digfingroup)|(digitimes)|(storm)|(sina)|(ltn)|(ithome)|(cnyes)|(cmmedia)|(ctee)|(chinatimes)|(udn\.com)|(money\.udn)|(cw\.com)|(bnext)|(nownews)|(businessweekly)|(inside)', url)
    if match:
        source = match.group()
        title, content, keywords = getattr(modules['crawler'],
                                           source.replace('.', '').replace('/', ''))(soup)
        if toFile:
            write(title, content, keywords)
        return title, content, keywords, source
    else:
        return 'title', 'content', 'keywords', ''

def mediumcom(soup):
    title = soup.find('h1').text
    article = soup.find_all(class_ = ['ia', 'ky', 'jn'])
    content = '\n'.join([p.text for p in article])
    keywords = [key.text for key in soup.find_all(class_ = 'oh')]
    return title, content, keywords

def aiacademy(soup):
    title = soup.find('h1').text
    article = soup.find_all(['p', 'h2'])
    content = '\n'.join([p.text for p in article])
    keywords = []
    return title, content, keywords

def blocktempo(soup):
    title = soup.find('h1').text
    article = soup.find(class_ = 'content-inner').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = [key.text for key in soup.find_all(rel = 'tag')]
    return title, content, keywords

def gartner(soup):
    title = soup.find('h1').text
    summary = soup.find(class_ = 'entry-summary').text.strip()
    article = soup.find(class_ = 'entry-content').find_all(['p', 'h2', 'ol'])
    content = summary + '\n'.join([p.text for p in article])
    keywords = []
    return title, content, keywords

def digfingroup(soup):
    title = soup.find(itemprop = 'headline').text
    article = soup.find(class_ = 'theiaPostSlider_preloadedSlide').find_all(['p', 'h4'])
    content = '\n'.join([p.text for p in article])
    keywords = [key.text for key in soup.find_all(rel = 'tag')]
    return title, content, keywords

def digitimes(soup):
    title = soup.find(class_  = 'txt-blue2').text
    article = soup.find(class_ = 'Article').find_all('p')
    content = '\n'.join([p.text.strip() for p in article[1:-1]])
    keys = soup.find(id = 'keyword').text.split('\n\n\n\n')
    keywords = [key.strip() for key in keys[1:-1]]
    return title, content, keywords

def storm(soup):
    title = soup.find(id = 'article_title').text
    article = soup.find(itemprop = 'articleBody').find_all(['p', 'h2'])
    content = '\n'.join([p.text.strip() for p in article])
    keywords = [key.text for key in soup.find_all(class_ = 'tag')]
    return title, content, keywords

def sina(soup):
    title = soup.find('h1').text
    content =  soup.find(class_ = 'pcont').find_all('p')
    content = '\n'.join([p.text for p in content])
    keywords = []
    return title, content, keywords

def ltn(soup):
    title = soup.find('h1').text.strip()
    article = soup.find(itemprop = 'articleBody').find_all(['p', 'h4'])[:-2]
    content = '\n'.join(p.text for p in article)
    keywords = []
    return title, content, keywords

def ithome(soup):
    title = soup.find(class_ = 'page-header').text
    summary = soup.find(class_ = 'content-summary').text.strip()
    content = soup.find(class_ = 'contents-wrap').find_all(['p', 'h3'])
    content = summary + '\n'.join([p.text.strip() for p in content])
    keywords = []
    return title, content, keywords

def cnyes(soup):
    title = soup.find('h1').text
    content = soup.find(itemprop = 'articleBody').find_all('p')
    content = '\n'.join([p.text for p in content])
    keywords = [k.text for k in soup.find_all(class_ = '_1E-R')]
    return title, content, keywords

def cmmedia(soup):
    title = soup.find(itemprop = 'headline').text
    article = soup.find(itemprop = 'articleBody').find_all('p')
    content = '\n'.join([p.text for p in article]).split('更多內容')[0]
    keywords = soup.find('meta', itemprop = 'keywords')
    keywords = keywords['content'].split(',')
    return title, content, keywords

def ctee(soup):
    try:
        title = soup.find(class_ = 'entry-title').text.strip()
    except:
        title = soup.find(itemprop = 'headline').text
    article = soup.find(class_ = 'entry-content').find_all(['p', 'h3'])
    content = '\n'.join([p.text for p in article]).split('延伸閱讀')[0]
    keywords = [key.text for key in soup.find_all(rel = 'tag')]
    return title, content, keywords

def chinatimes(soup):
    title = soup.find('h1').text
    article = soup.find(class_ = 'article-body').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = soup.find(class_ = 'article-hash-tag').text.split('\n#')[1:]
    return title, content, keywords

def udncom(soup):
    title = soup.find('h1').text
    article = soup.find(class_ = 'article-content').find_all('p')
    content = ''.join([p.text for p in article])
    keywords = soup.find(class_ = 'keywords').text.strip().split('\n')
    return title, content, keywords

def moneyudn(soup):
    title = soup.find('h2').text
    article = soup.find(id = 'article_body').find_all('p')
    content = ''.join([p.text for p in article])
    keywords = soup.find(id = 'story_tags').text.strip().split('\n')
    return title, content, keywords

def cwcom(soup):
    title = soup.find('h1').text
    article = soup.find(class_ = 'nevin').find_all('p')
    content = '\n'.join([p.text.strip() for p in article])
    keywords = [key.text.strip() for key in soup.find_all(class_ = 'keywords')]
    return title, content, keywords

def nownews(soup):
    title = soup.find(class_ = 'entry-title').text
    article = soup.find(itemprop = 'articleBody').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = [key.text for key in soup.find(class_ = 'td-tags').contents[1:]]
    return title, content, keywords

def bnext(soup):
    title = soup.find(class_ = 'article_title').text.strip()
    article = soup.find(itemprop = 'articleBody').find_all(['h2', 'p'])
    content = '\n'.join([p.text.strip() for p in article])
    try:
        keywords = soup.find(class_ = 'article_tags').text.split('\n#')[1:]
    except:
        keywords = soup.find(class_ = 'article_tag').text.split('\n')[1:-1]
    return title, content, keywords

def businessweekly(soup):
    title = soup.find('h1').text
    article = soup.find(class_ = 'articlebody').find_all('p')
    content = '\n'.join([p.text for p in article])
    keywords = soup.find(class_ = 'tag').text.split('\n')
    return title, content, keywords

def inside(soup):
    title = soup.find('h1').text
    intro = soup.find(class_ = 'post_introduction').text.strip()+'\n'
    article = soup.find(itemprop = 'articleBody').find_all(['h3', 'p'])
    content = intro + '\n'.join([p.text for p in article]).split('延伸閱讀')[0]
    keywords = [key.text for key in soup.find(class_ = 'content').find_all(class_ = 'hero_slide_tag')]
    return title, content, keywords

def write(title, content, keywords):
    with open('nn.txt','w')as f:
        print(f"{title}\n---\n{content}\n===\n")
        f.write(f"{title}\n---\n{content}\n===\n")
        for keyword in keywords:
            print(keyword)
            f.write(f"{keyword}\n")

if '__main__' == __name__:
    crawler(url)

