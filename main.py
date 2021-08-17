import os
import sys
import argparse
from datetime import datetime

from scripts.category import *
from scripts.feedly_rss import *
from scripts.articles import *
from scripts.converter import *

PATH = sys.path[0]

# path of Feedly token
TOKEN = os.path.join(PATH, 'src', 'access.token')
# path of wkhtmltopdf
WK = os.path.join(PATH, 'src', 'wkhtmltopdf.exe')
# path of css file
STYLE = os.path.join(PATH, 'src', 'style.css')

def main(token_file, category, wkhtmltopdf, out='out', css=None):
    if css == 'None': css = None
    if '.pdf' not in out: out += '.pdf'
    article_list = []
    feedly_api = FeedlyRSS(token_file)
    feedly_api.get_rss(category)
    count = 0
    log_all = ''
    for article_json in feedly_api.article_json_list:
        count += 1
        article_cls, ori = article_factory(article_json)
        if 'originId' in article_json.keys():
            url = article_json['originId']
        if 'canonicalUrl' in article_json.keys():
            url = article_json['canonicalUrl']
        log = 'Article %s from %s '%(count, ori)
        try:
            article_obj = article_cls()
            article_obj.get_content(article_json)
            article_list.append(article_obj)
            log = log + 'done.'
        except AttributeError:
            log = log + 'failed (NoAttribute).\n  ' + url
        except TypeError:
            log = log + 'failed (NoType).\n  ' + url
        except KeyError:
            log = log + 'failed (NoKey).\n  ' + url
        print(log)
        log_all += log + '\n'
    with open('log_%s.txt'%category, 'w') as f:
        f.write(log_all)
    cvt = Converter(wkhtmltopdf, out, css)
    cvt.string_to_pdf(article_list)


def cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                 required=False,
                 default=TOKEN,
                 type=str,
                 dest='token',
                 metavar='<token file>',
                 help='path of the token file')
    parser.add_argument('-c', '--category',
                 required=False,
                 default='daily',
                 type=str,
                 dest='cat',
                 metavar='<category>',
                 help='name of the category')
    parser.add_argument('-wk', '--wkhtmltopdf',
                 required=False,
                 default=WK,
                 type=str,
                 dest='wk',
                 metavar='<wkhtmltopdf>',
                 help='path of wkhtmltopdf')
    cat = parser.parse_args().cat
    out = os.path.join(PATH, '%s_%s.pdf'%(cat, datetime.now().strftime('%Y%m%d')))
    parser.add_argument('-o', '--out',
                 required=False,
                 default=out,
                 type=str,
                 dest='out',
                 metavar='<output>',
                 help='path of the output file')
    parser.add_argument('-s', '--style',
                 required=False,
                 default=STYLE,
                 type=str,
                 dest='style',
                 metavar='<style>',
                 help='path of the css file')
    return parser.parse_args()


if __name__ == '__main__':
    args = cmd_parser()
    # path of output file
    
    main(args.token, cat_dict[args.cat], args.wk, args.out, args.style)