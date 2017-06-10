import requests
import uuid
from bs4 import BeautifulSoup

#########################
# input your id / pw / gall_id
dc_id = 'example' 
dc_pw = '123'
gallery_id = 'japanese'
#########################

#------------ COOKIE GERNERATE ------------#
hello = uuid.uuid4()
hello = str(hello).replace("-","")
print "cookie = {}".format(hello)

#------------ LOGIN ------------#
url = "https://dcid.dcinside.com/join/member_check.php"
cookies = {'PHPSESSID':hello}
payload = {
    's_url':'http://www.dcinside.com/',
    'ssl':'Y',
    'user_id':dc_id,
    'password':dc_pw
}
headers = {
    'Upgrade-Insecure-Requests':'1',
    'DNT':'1',
    'Referer':'http://www.dcinside.com/'
}

r = requests.post(url, cookies=cookies, data=payload, headers=headers)

#------------ NAME COLLECT ------------#
url = 'http://www.dcinside.com/'
cookies = {'PHPSESSID':hello}
r = requests.post(url, cookies=cookies, data=payload, headers=headers)

con = r.text
soup = BeautifulSoup(con, "lxml")
link = soup.find_all("strong", { "class" : "fc_2b" })
dc_name = link[0].string
dc_name = str(dc_name) #safe

##############################
page_number = '1'
nickname = dc_name
pos = '-10000'
##############################

#------------ NOTICE COLLECTION ------------#
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
            ps_notice = link[kk].string
            delete_list.append(str(ps_notice))
            notice_cnt += 1
            total_cnt += 1
        page_cnt += 1
        if(notice_cnt == 0):
            break
        notice_cnt = 0
    page_cnt = 0
    print "loading...{}/-300000".format(pos)
    tmp = int(pos) - 10000
    pos = str(tmp)
    if(pos == '-300000'):
        break
print "total notice = {}".format(total_cnt)
print "delete_list_cnt = {}".format(len(delete_list))
print delete_list

for DN in delete_list:
    #------------ INIT ------------#
    payload = {}
    sessionID = hello 
    noticeNUM = DN 
    #noticeNUM = '231815'
    csrfToken = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    #------------ GET FORM DATA ------------#
    print ("==================================================================================================")
    url="http://gall.dcinside.com/board/delete/?id=japanese&no=" + noticeNUM
    cookies = {'PHPSESSID':sessionID,'ci_c':csrfToken,'notice_no':noticeNUM}
    data = {}
    con = requests.get(url, data=data, cookies=cookies).text 
    soup = BeautifulSoup(con, "lxml")
    link = soup.find_all("input")
    for nn in range(4,len(link)-1):
	try:
	    tmp = link[nn]
	    payload[tmp['name']] = tmp['value']
	except BaseException:
	    pass

    try:
        link = soup.find_all("script")
        strlink = str(link[28])
        lastindex = strlink.find('formData += "&')
    
        #------------ MAKE PAYLOAD ------------#
        jsform = strlink[lastindex+14:lastindex+95]
        jsformKey = strlink[lastindex+14:lastindex+54]
        jsformVal = strlink[lastindex+55:lastindex+95]
        payload[jsformKey] = jsformVal
    except BaseException:
        pass

    #------- DELETE REQUEST -------#
    url="http://gall.dcinside.com/forms/delete_submit"
    cookies = {'PHPSESSID':sessionID,'ci_c':csrfToken,'notice_no':noticeNUM}
    headers = {'X-Requested-With':'XMLHttpRequest'}
    con = requests.post(url, data=payload, cookies=cookies, headers=headers)
    print con
