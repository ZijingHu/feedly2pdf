import os
import sys
from datetime import datetime


PATH = sys.path[0]

# path of Feedly token
TOKEN = os.path.join(PATH, 'src', 'access.token')
# path of wkhtmltopdf
WK = os.path.join(PATH, 'src', 'wkhtmltopdf.exe')
# path of css file
STYLE = os.path.join(PATH, 'src', 'style.css')
# path of output file
OUT = os.path.join(PATH, 'Articles%s.pdf'%datetime.now().strftime('%Y%m%d'))