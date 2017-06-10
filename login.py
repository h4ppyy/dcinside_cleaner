import urllib
import urllib2
import requests
import uuid
from bs4 import BeautifulSoup

#########################
# input your id / pw
dc_id = 'example' 
dc_pw = '123123'
#########################

#------------ COOKIE GERNERATE ------------#
hello = uuid.uuid4()
hello = str(hello).replace("-","")
print hello

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

# DEBUG
print cookies
r = requests.post(url, cookies=cookies, data=payload, headers=headers)

#------------ INIT ------------#
payload = {}
sessionID = hello 
noticeNUM = '231815'
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
link = soup.find_all("script")
strlink = str(link[28])
lastindex = strlink.find('formData += "&')

#------------ MAKE PAYLOAD ------------#
jsform = strlink[lastindex+14:lastindex+95]
jsformKey = strlink[lastindex+14:lastindex+54]
jsformVal = strlink[lastindex+55:lastindex+95]
payload[jsformKey] = jsformVal

#------- DELETE REQUEST -------#
url="http://gall.dcinside.com/forms/delete_submit"
cookies = {'PHPSESSID':sessionID,'ci_c':csrfToken,'notice_no':noticeNUM}
headers = {'X-Requested-With':'XMLHttpRequest'}
con = requests.post(url, data=payload, cookies=cookies, headers=headers)
print con
