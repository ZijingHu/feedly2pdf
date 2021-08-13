import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class Articles:
    '''Class to story article information

    :attr str title: title of the article
    :attr str content: title of the article
    :attr list article_json_list: a list to store Feedly stream contents
    :attr str origin: origin of the article
    '''
    def __init__(self):
        self.title = ''
        self.content = ''
        self.published = ''
        self.origin = ''
        
    @staticmethod
    def timestamp2str(timestamp):
        '''Convert timestamp to datetime str (%Y-%m-%d) 

        :param int/str timestamp: 9-digit timestamp
        :return str: datetime (%Y-%m-%d)
        '''
        timestamp = int(timestamp) / 1000
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
    @staticmethod
    def get_page(url):
        '''get bs parsed page
        
        :param str url: url of page
        :return bs4.BeautifulSoup
        '''
        html = requests.get(url).content.decode('utf-8')
        return BeautifulSoup(html, 'lxml')
           
    def parse_bs_page(self, atricle_bs):
        '''parse article bs page
        
        :param bs4.BeautifulSoup atricle_bs: bs page
        :return str: article in string
        '''
        article_text = '<h2>%s</h2><p><i>%s, %s</i></p><br>'%(self.title, self.origin, self.published)
        for i in atricle_bs.find_all(re.compile(r'(h2|p|ul|img)')):
            if i.name == 'p' and not i.has_attr('class'):
                if len(str(i).strip()) == 0:
                    continue
                article_text += '%s<br>'%str(i).strip()
            if i.name == 'h2':
                article_text += '<h3>%s</h3>'%i.text
            if i.name == 'ul' and not i.has_attr('class'):
                article_text += '%s<br>'%str(i)
            if i.name == 'img' and ('jpeg' in i['src'] or 'svgz' in i['src']):
                if 'http' not in i['src']:
                    i['src'] = self.origin_url + i['src']
                i['src'] = i['src'].replace('svgz', 'png')
                article_text += '<center><img src="%s" style="width:80%%"></center>'%i['src']
        article_text = article_text.replace('<br><h', '<h')\
                                   .replace('\n', '')
        return article_text
    
    def extract_content(self, url):
        '''Extract content from webpages
        
        :param str url: url of the page to scrape
        '''
        pass
        
    def get_content(self, stream_content):
        '''combine title, content and publish date
        
        :param dict stream_content: Feedly stream contents        
        '''
        pass


class ForbesArticles(Articles):
    '''Articles from Forbes'''
    def extract_content(self, url):
        bs = self.get_page(url)
        article_class = 'article-body fs-article fs-responsive-text current-article'
        atricle_bs = bs.find('div', {'class': article_class})
        self.content = self.parse_bs_page(atricle_bs)
        
    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        url = stream_content['canonicalUrl']
        self.extract_content(url)


class HbrArticles(Articles):
    '''Articles from Harvard Business Review'''
    def extract_content(self, url):
        bs = self.get_page(url)
        article_class = 'article-body standard-content'
        atricle_bs = bs.find('div', {'class': article_class})
        atricle_bs.find('div', {'class': 'left-rail--container'}).decompose()
        self.content = self.parse_bs_page(atricle_bs)
        
    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        url = stream_content['canonicalUrl']
        self.extract_content(url)

class SmrArticles(Articles):
    '''Articles from MIT Sloan Management Review'''        
    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        atricle_bs = BeautifulSoup(stream_content['content']['content'], 'lxml')
        self.content = self.parse_bs_page(atricle_bs)

class McKinseyArticles(Articles):
    '''Articles from McKinsey Insight'''
    def extract_content(self, url):
        bs = self.get_page(url)
        article_class = 'divArticleBody'
        atricle_bs = bs.find('div', {'id': article_class})
        self.content = self.parse_bs_page(atricle_bs)

    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        url = stream_content['canonicalUrl']
        self.extract_content(url)
        
class NielsenArticles(Articles):
    '''Articles from Nielsen'''        
    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        atricle_bs = BeautifulSoup(stream_content['content']['content'], 'lxml')
        self.content = self.parse_bs_page(atricle_bs)

ORI_DICT = {
    'Forbes - Entrepreneurs': ForbesArticles,
    'Harvard Business Review': HbrArticles,
    'MIT Sloan Management Review': SmrArticles,
    'McKinsey': McKinseyArticles,
    'Insights – Nielsen': NielsenArticles
}
    
 
def article_factory(article_json):
    '''Determine article class based on the article's origin
    
    :param dict article_json: Feedly stream contents
    :return Articles
    '''
    ori = article_json['origin']['title'].strip()
    return ORI_DICT[ori]