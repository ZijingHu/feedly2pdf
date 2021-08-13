import argparse

import config
from scripts.category import *
from scripts.feedly_rss import *
from scripts.articles import *
from scripts.converter import *


def main(token_file, category, wkhtmltopdf, out='out', css=None):
    if css == 'None': css = None
    if '.pdf' not in out: out += '.pdf'
    article_list = []
    feedly_api = FeedlyRSS(token_file)
    feedly_api.get_rss(category)
    for article_json in feedly_api.article_json_list:
        article_cls = article_factory(article_json)
        article_list.append(article_cls())
        try:
            article_list[-1].get_content(article_json)
        except AttributeError:
            pass
    cvt = Converter(wkhtmltopdf, out, css)
    cvt.string_to_pdf(article_list)


def cmd_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                 required=False,
                 default=config.TOKEN,
                 type=str,
                 dest='token',
                 metavar='<token file>',
                 help='path of the token file')
    parser.add_argument('-c', '--category',
                 required=False,
                 default=cat_dict['daily'],
                 type=str,
                 dest='cat',
                 metavar='<category>',
                 help='name of the category')
    parser.add_argument('-wk', '--wkhtmltopdf',
                 required=False,
                 default=config.WK,
                 type=str,
                 dest='wk',
                 metavar='<wkhtmltopdf>',
                 help='path of wkhtmltopdf')
    parser.add_argument('-o', '--out',
                 required=False,
                 default=config.OUT,
                 type=str,
                 dest='out',
                 metavar='<output>',
                 help='path of the output file')
    parser.add_argument('-s', '--style',
                 required=False,
                 default=config.STYLE,
                 type=str,
                 dest='style',
                 metavar='<style>',
                 help='path of the css file')
    return parser.parse_args()


if __name__ == '__main__':
    args = cmd_parser()
    main(args.token, args.cat, args.wk, args.out, args.style)