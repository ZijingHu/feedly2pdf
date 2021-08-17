from datetime import datetime

# Installing wkhtmltopdf
# https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
# https://wkhtmltopdf.org/downloads.html
import pdfkit

OPTIONS = {
    'margin-left': '12mm',
    'margin-right': '12mm',
    'margin-bottom': '20mm',
    'margin-top': '20mm'
}

class Converter:
    '''Convert article list (list of Article classes) to pdf
    
    :attr pdfkit.configuration.Configuration config: set wkhtmltopdf path
    :attr str content: string that will be convert to pdf
    :attr str css: path of css file
    :attr str out: path of output pdf file
    '''
    def __init__(self, wkhtmltopdf, out='out.pdf', css=None):
        '''Initialization
        
        :param str wkhtmltopdf: path of wkhtmltopdf
        :param str css: path of css file
        :param str out: path of output pdf file
        '''
        now = datetime.now().strftime('%Y-%m-%d')
        self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
        self.content = '<h1>Articles %s</h1>'%now
        self.css = css
        self.out = out
        
    def string_to_pdf(self, article_list):
        '''Convert string to pdf file
        
        :param list article_list: list of Article classes
        '''
        for a in article_list:
            self.content += a.content 
        self.content = self.content.replace('<p></p><br>', '')
        meta = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
        html_string = '<html><head>%s</head><body>%s</body></html>'%(meta, self.content)
        pdfkit.from_string(html_string, 
                     self.out,
                     options=OPTIONS,
                     configuration=self.config, 
                     css=self.css)