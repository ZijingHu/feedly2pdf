import re
import time
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
        self.origin_url = ''
        
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
        html = requests.get(url, headers={'User-Agent': 'GhostBrowser'}).content.decode('utf-8')
        return BeautifulSoup(html, 'lxml')
           
    def parse_bs_page(self, article_bs):
        '''parse article bs page
        
        :param bs4.BeautifulSoup article_bs: bs page
        :return str: article in string
        '''
        article_text = '<h2>%s</h2><p><i>%s, %s</i></p><br>'%(self.title, self.origin, self.published)
        for i in article_bs.find_all(re.compile(r'(h2|p|ul|img)')):
            if i.name == 'p' and not i.has_attr('class'):
                if i.find(re.compile(r'(img|iframe)')) is not None:
                    continue
                if len(str(i).strip()) == 0:
                    continue
                article_text += '%s<br>'%str(i).strip()
            if i.name == 'h2':
                article_text += '<h3>%s</h3>'%i.text
            if i.name == 'ul' and not i.has_attr('class'):
                article_text += '%s<br>'%str(i)
            if i.name == 'img' and ('jpeg' in i['src'] or 'svgz' in i['src'] or 'png' in i['src']):
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

    def test(self):
        print('Title: %s'%self.title, 
              'Journal: %s'%self.origin, 
              'Authors: %s'%self.published, 
              'Abstract: %s'%self.content, 
              sep='\n')
              

class ForbesArticles(Articles):
    '''Articles from Forbes'''
    def extract_content(self, url):
        bs = self.get_page(url)
        article_class = 'article-body fs-article fs-responsive-text current-article'
        article_bs = bs.find('div', {'class': article_class})
        self.content = self.parse_bs_page(article_bs)
        
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
        article_bs = bs.find('div', {'class': article_class})
        article_bs.find('div', {'class': 'left-rail--container'}).decompose()
        self.content = self.parse_bs_page(article_bs)
        
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
        article_bs = BeautifulSoup(stream_content['content']['content'], 'lxml')
        self.content = self.parse_bs_page(article_bs)


class McKinseyArticles(Articles):
    '''Articles from McKinsey Insight'''
    def extract_content(self, url):
        bs = self.get_page(url)
        article_class = 'divArticleBody'
        article_bs = bs.find('div', {'id': article_class})
        self.content = self.parse_bs_page(article_bs)

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
        article_bs = BeautifulSoup(stream_content['content']['content'], 'lxml')
        self.content = self.parse_bs_page(article_bs)
        
class ForresterArticles(Articles):
    '''Articles from Forrester'''
    def extract_content(self, url):
        bs = self.get_page(url)
        article_class = 'post-content post-body__item'
        article_bs = bs.find('div', {'class': article_class})
        self.content = self.parse_bs_page(article_bs)
        
    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        url = stream_content['canonicalUrl']
        self.extract_content(url)


class MartechArticles(Articles):
    '''Articles from Martech'''
    def get_content(self, stream_content):
        self.title = stream_content['title']
        self.origin = stream_content['origin']['title']
        self.origin_url = stream_content['origin']['htmlUrl']
        self.published = self.timestamp2str(stream_content['published'])
        url = stream_content['originId']
        article_bs = BeautifulSoup(stream_content['content']['content'], 'lxml')
        self.content = self.parse_bs_page(article_bs)


class Papers(Articles):
    def parse_bs_page(self, abstract):
        '''parse article bs page
        
        :param str abstract: abstract string
        :return str: article in string
        '''
        article_text = '<h3>%s</h3><p><i>Source: %s<br>%s</i></p><br><p>%s</p><br>'\
                       %(self.title, self.published, self.origin, abstract)
        return article_text


class SagePapers(Papers):
    '''JMR, JM'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        article_info = article_bs.find('meta', {'property': 'og:title'})['content']
        self.title, authors = article_info.split(' - ', 1)
        self.origin = authors[:-6]
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']
        abstract = article_bs.find('div', {'class': 'abstractSection abstractInFull'}).text
        self.content = self.parse_bs_page(abstract)


class InformsPapers(Papers):
    '''ISR, MktgSci, MngSci'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl'].split('?')[0]
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'dc.Title'})['content']
        authors = article_bs.find_all('meta', {'name': 'dc.Creator'})
        self.origin  = ', '.join([i['content'].strip().replace('  ', ' ') for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('div', {'class': 'abstractSection abstractInFull'}).text
        self.content = self.parse_bs_page(abstract)


class OxfordPapers(Papers):
    '''JCR, QJE'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['originId']
        self.title = stream_content['title']
        self.origin  = stream_content['author']
        self.published = stream_content['origin']['title'].replace(' Current Issue', '')
        abstract = stream_content['summary']['content']\
                     .replace('<span><div>Abstract</div>', '').replace('</span>', '')
        self.content = self.parse_bs_page(abstract)


class WileyPapers(Papers):
    '''Econometrica'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'property': 'og:title'})['content']
        authors = article_bs.find_all('meta', {'name': 'citation_author'})
        self.origin  = ', '.join([i['content'].strip() for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('div', {'class': 'article-section__content en main'}).text
        self.content = self.parse_bs_page(abstract)


class NBERPapers(Papers):
    '''NBER'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'dcterms.title'})['content']
        self.origin = article_bs.find('meta', {'name': 'dcterms.creator'})['content']
        self.published = article_bs.find('meta', {'name': 'citation_technical_report_institution'})['content']       
        abstract = article_bs.find('div', {'class': 'page-header__intro-inner'}).text
        self.content = self.parse_bs_page(abstract)


class AEAPapers(Papers):
    '''AER'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'citation_title'})['content']
        authors = article_bs.find_all('meta', {'name': 'citation_author'})
        self.origin = ', '.join([' '.join(i['content'].split(', ')[::-1]) for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('section', {'class': 'article-information abstract'}).text
        self.content = self.parse_bs_page(abstract)


class ChicagoPapers(Papers):
    '''JPE'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl'].split('?')[0]
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'dc.Title'})['content']
        authors = article_bs.find_all('meta', {'name': 'dc.Creator'})
        self.origin  = ', '.join([i['content'].strip().replace('  ', ' ') for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('div', {'class': 'abstractSection abstractInFull'}).text
        self.content = self.parse_bs_page(abstract)


class MITPapers(Papers):
    '''RES'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'citation_title'})['content']
        authors = article_bs.find_all('div', {'class': 'info-card-name'})
        self.origin  = ', '.join([i.text.strip() for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('section', {'class': 'abstract'}).text
        self.content = self.parse_bs_page(abstract)


class PNASPapers(Papers):
    '''PNAS'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'DC.Title'})['content']
        authors = article_bs.find_all('meta', {'name': 'DC.Contributor'})
        self.origin  = ', '.join([i['content'].strip() for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('meta', {'name': 'citation_abstract'})['content']
        self.content = self.parse_bs_page(abstract)


class NatureDataPapers(Papers):
    '''Nature'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'citation_title'})['content']
        authors = article_bs.find_all('a', {'data-test': 'author-name'})
        if len(authors) > 3:
            tail = ' ...'
            authors = authors[:3]
        else:
            tail = ''
        self.origin  = ', '.join([i.text.strip() for i in authors]) + tail
        self.published = article_bs.find('meta', {'name': 'WT.cg_n'})['content']       
        abstract = article_bs.find('div', {'class': 'c-article-section__content'}).text
        self.content = self.parse_bs_page(abstract)


class ElsevierPapers(Papers):
    '''IJRM'''
    @staticmethod
    def get_name(name_html):
        f = name_html.find('span', {'class': 'text given-name'}).text
        l = name_html.find('span', {'class': 'text surname'}).text
        return f + ' ' + l
        
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'citation_title'})['content']
        authors = article_bs.find_all('a', {'class': 'author size-m workspace-trigger'})
        self.origin  = ', '.join([self.get_name(i) for i in authors])
        self.published = article_bs.find('meta', {'name': 'citation_journal_title'})['content']       
        abstract = article_bs.find('p', {'id': 'sp0005'}).text
        self.content = self.parse_bs_page(abstract)


class JMISPapers(Papers):
    '''JMIS'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['canonicalUrl']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('div', {'class': 'margin-bottom-5'}).text
        authors = article_bs.find('div', {'class': 'margin-bottom-10'}).find_all('a')
        self.origin = ', '.join([' '.join(i.text.split(', ')[::-1]) for i in authors])
        self.published = article_bs.find('h4').text      
        abstract = stream_content['summary']['content']\
                     .replace('ABSTRACT: <p>', '').replace('</p>', '')
        self.content = self.parse_bs_page(abstract)


class MISQPapers(Papers):
    '''MISQ'''
    def get_content(self, stream_content):
        self.origin_url = stream_content['originId']
        article_bs = self.get_page(self.origin_url)
        self.title = article_bs.find('meta', {'name': 'bepress_citation_title'})['content']
        authors = article_bs.find_all('meta', {'name': 'bepress_citation_author'})
        self.origin = ', '.join([' '.join(i['content'].split(', ')[::-1]) for i in authors])
        self.published = article_bs.find('meta', {'name': 'bepress_citation_journal_title'})['content']       
        abstract = article_bs.find('meta', {'name': 'description'})['content']
        self.content = self.parse_bs_page(abstract)
    
    
ORI_DICT = {
    # News
    'Forbes - Entrepreneurs': ForbesArticles,
    'Harvard Business Review': HbrArticles,
    'MIT Sloan Management Review': SmrArticles,
    'McKinsey': McKinseyArticles,
    'Insights – Nielsen': NielsenArticles,
    'Featured Blogs – Forrester': ForresterArticles,
    'MarTech' : MartechArticles,
    # Papers
    'SAGE Publications Inc: Journal of Marketing: Table of Contents': SagePapers,
    'SAGE Publications Inc: Journal of Marketing Research: Table of Contents': SagePapers,
    'iorms: Information Systems Research: Table of Contents': InformsPapers,
    'iorms: Marketing Science: Table of Contents': InformsPapers,
    'iorms: Management Science: Table of Contents': InformsPapers,
    'Journal of Consumer Research Current Issue': OxfordPapers,
    'The Quarterly Journal of Economics Current Issue': OxfordPapers,
    'Wiley: Econometrica: Table of Contents': WileyPapers,
    'National Bureau of Economic Research Working Papers': NBERPapers,
    'American Economic Review': AEAPapers,
    'The University of Chicago Press: Journal of Political Economy: Table of Contents': ChicagoPapers,
    'MIT Press: Review of Economics and Statistics: Table of Contents': MITPapers,
    'Proceedings of the National Academy of Sciences Social Sciences': PNASPapers,
    'Scientific Data - nature.com science feeds': NatureDataPapers,
    'ScienceDirect Publication: International Journal of Research in Marketing': ElsevierPapers,
    'Journal of Management Information Systems': JMISPapers,
    'Management Information Systems Quarterly': MISQPapers
}

 
def article_factory(article_json):
    '''Determine article class based on the article's origin
    
    :param dict article_json: Feedly stream contents
    :return Articles
    '''
    ori = article_json['origin']['title'].strip()
    return ORI_DICT[ori], ori