# Usage

python main.py [-h] [-t <token file>] [-c <category>] 
               [-wk <wkhtmltopdf>] [-o <output>] [-s <style>]

# Config

config.py: change default token path, wkhtmltopdf path, css path and output path
category.py: add/remove category

# Scripts

feedly_rss.py: get Feedly RSS feeds (json)
articles.py: scrape articles through urls in Feedly RSS info
converter.py: convert html string to pdf