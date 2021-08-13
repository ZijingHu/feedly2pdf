from datetime import datetime

# pip install feedly-client
# Feedly API  https://developers.feedly.com/
from feedly.api_client.session import FeedlySession
from feedly.api_client.stream import StreamOptions

BACKTRACKING = 10000 # unit: hour
MAX_RSS = 29

class FeedlyRSS:
    '''Access RSS feed via Feedly token
    Python client code for the feedly api https://developers.feedly.com/
    
    :attr str token: Feedly token
    :attr str today: 13-digit timestamp = now - BACKTRACKING
    :attr list article_json_list: a list to store Feedly stream contents
    '''
    def __init__(self, token_file):
        '''Initialization
        
        :param str token_file: name of file that stores the token
        '''
        with open(token_file, 'r') as f:
            self.token = f.read().strip()
        self.today = (datetime.now().timestamp() - 3600*BACKTRACKING)*1000
        self.article_json_list = []

    def get_rss(self, category):
        '''Get Feedly stream contents
        
        :param str category: Feedly category code
            can be found via FeedlySession(token).user.get_categories()
        '''
        opts = StreamOptions(max_count=MAX_RSS)
        with FeedlySession(auth=self.token) as sess:
            for con in sess.user.get_category(category).stream_contents(opts):
                if con.json['published'] > self.today:
                    self.article_json_list.append(con.json)
                else:
                    break