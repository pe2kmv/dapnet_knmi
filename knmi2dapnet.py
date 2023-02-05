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

# lookup in dictionary
def SearchCode(keyword):
	for msg in dbmessages:
		if keyword in msg:
			return(msg[1])

for entry in knmifeed.entries:
	try:
		location = entry.title.split()[1]
		txgroup = txmap[location].split(',')
		rubrics = rubricmap[location].split(',')
		knmimsg = entry.summary
		knmicode = entry.summary.split()[1].upper().replace('.','')
		msgcode = SearchCode(location)
		if knmicode != SearchCode(location):
#			send_page('pe2kmv','3',txgroup,'False',location + ': '+ knmimsg)
			for rb in rubrics:
				send_rubric(location + ': ' + knmimsg,rb)
		AddWarningMessage(knmicode,location,knmimsg)
	except:
		pass

CleanDB()
