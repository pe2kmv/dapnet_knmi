import feedparser
import configparser
from txmapping import txmap as txmap
from txmapping import rubricmap as rubricmap
from knmimysql import *
from sendmsg import *

DBInit()

feedurl = 'https://www.knmi.nl/rssfeeds/rss_KNMIwaarschuwingen'

knmifeed = feedparser.parse(feedurl)

dbmessages = GetMsgList()

from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# lookup in dictionary
def SearchCode(keyword):
	if len(dbmessages) > 0:
		for msg in dbmessages:
			if keyword in msg:
				return(msg[1])
	else:
		return()

for entry in knmifeed.entries:
	try:
		location = entry.title.split()[1]
		txgroup = txmap[location].split(',')
		rubrics = rubricmap[location].split(',')
		knmimsg = strip_tags(entry.summary)
		knmicode = strip_tags(entry.summary.split()[1].upper().replace('.',''))
		msgcode = SearchCode(location)
		if knmicode != SearchCode(location):
#			send_page('pe2kmv','3',txgroup,'False',location + ': '+ knmimsg)
			for rb in rubrics:
				send_rubric(location + ': ' + knmimsg,rb)
		AddWarningMessage(knmicode,location,knmimsg)
	except:
		pass

CleanDB()
