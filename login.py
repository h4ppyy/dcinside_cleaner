import urllib
import urllib2
import requests
from bs4 import BeautifulSoup

#------------ INIT ------------#
payload = {} 
sessionID = 'edvrkg5q3rpbv66algrth2la56'
noticeNUM = '231786'
csrfToken = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

#------------ LOGIN ------------#
url="https://dcid.dcinside.com/join/member_check.php"
data = {
    's_url':'http://www.dcinside.com/',
    'ssl':'Y',
    'user_id':'example0',
    'password':'####'
}
endata = urllib.urlencode(data)
request = urllib2.Request(url, endata)
response = urllib2.urlopen(request)

cookie = response.headers.get('Set-Cookie')

print cookie

realcookie = "'" + cookie[10:42] + "'"

print realcookie

#------------ GET FORM DATA ------------#
print ("==================================================================================================")
url="http://gall.dcinside.com/board/delete/?id=japanese&no=" + noticeNUM
cookies = {'PHPSESSID':sessionID,'ci_c':csrfToken,'notice_no':noticeNUM}
con = requests.get(url, data=data, cookies=cookies).text 

soup = BeautifulSoup(con, "lxml")
link = soup.find_all("input")

# DEBUG
#for kk in range(3,len(link)):
#    print link[kk]
#print ("==================================================================================================")

for nn in range(4,len(link)-1):
    try:
        tmp = link[nn]
        # DEBUG
        #print "{}={}".format(tmp['name'], tmp['value'])
        payload[tmp['name']] = tmp['value']
    except BaseException:
        pass
        # DEBUG
        #print "{}=".format(tmp['name'])

link = soup.find_all("script")

strlink = str(link[28])
lastindex = strlink.find('formData += "&')
# DEBUG
#print strlink[lastindex+14:lastindex+95]

#------------ MAKE PAYLOAD ------------#
#print ("==================================================================================================")

jsform = strlink[lastindex+14:lastindex+95]
jsformKey = strlink[lastindex+14:lastindex+54]
jsformVal = strlink[lastindex+55:lastindex+95]

#print jsform
#print jsformKey
#print jsformVal

payload[jsformKey] = jsformVal

# DEBUG
#print payload
#print ("==================================================================================================")

#------- DELETE REQUEST -------#
url="http://gall.dcinside.com/forms/delete_submit"

cookies = {'PHPSESSID':sessionID,'ci_c':csrfToken,'notice_no':noticeNUM}
headers = {'X-Requested-With':'XMLHttpRequest'}

con = requests.post(url, data=payload, cookies=cookies, headers=headers)
print con
