import urllib
import urllib2
import requests
import uuid
from bs4 import BeautifulSoup

##############################
gallery_id = 'japanese'
page_number = '1'
nickname = '%EA%B7%B9%ED%9D%91%ED%97%AC%EB%A0%8C%EC%BC%88%EB%9F%AC'
pos = '-10000'
##############################

page_cnt = 0
notice_cnt = 0
total_cnt = 0

while True:
    for page_number in range(1,7+1):
	url = "http://gall.dcinside.com/board/lists/"
	payload = {
	    'id':gallery_id,
	    'page':page_number,
	    's_type':'search_name',
	    's_keyword':nickname,
	    'search_pos':pos,
	}

	r = requests.get(url, params=payload)

	con = r.text

	soup = BeautifulSoup(con, "lxml")
	link = soup.find_all("td", { "class" : "t_notice" })

	for kk in range(0,len(link)):
	    print link[kk]
	    notice_cnt += 1
            total_cnt += 1
	page_cnt += 1
	if(notice_cnt == 0):
	    print "==================================== NOTHING"
	    break
	print "==================================== page_cnt =  {} / notice_cnt = {}".format(page_cnt, notice_cnt)
	notice_cnt = 0
    page_cnt = 0
    print pos
    tmp = int(pos) - 10000
    pos = str(tmp)
    if(pos == '-300000'):
        break

print "total notice = {}".format(total_cnt)
