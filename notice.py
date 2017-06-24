import urllib
import urllib2
import requests
import uuid
from bs4 import BeautifulSoup
from urllib import quote

##############################
gallery_id = 'japanese'
page_number = '1'
nickname = quote('닉네임')
pos = '-10000'
##############################

delete_list = []

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
            ps_notice = str(link[kk])
            delete_list.append(ps_notice[21:27])
            print ps_notice[21:27]
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
print "delete_list_cnt = {}".format(len(delete_list))

print delete_list

