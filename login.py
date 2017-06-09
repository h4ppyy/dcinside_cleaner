import urllib
import urllib2
import requests
from bs4 import BeautifulSoup

#------------ INIT ------------#
payload = {} 
fullpayload = ""

#------------ DEBUG ------------#
#print(soup.prettify())
#ci_t = link[4]
#id = link[5]
#no = link[6]
#key = link[7]
#dcc_key = link[8]
#print link[nn]
#print link[28]
#print strlink[lastindex+13:lastindex+96]
#print payload

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

#------------ INPUT URL ------------#
print ("==================================================================================================")
url="http://gall.dcinside.com/board/delete/?id=japanese&no=231721"

#------------ GET FORM DATA ------------#

realcookie = "'" + cookie[10:42] + "'"

#print realcookie

cookies = {'PHPSESSID':'tppd5m525urdfl5ufks81qmda1','ci_c':'5f89d862ed21f8bec46f296cc5f574b8','notice_no':'231721'}
con = requests.get(url, data=data, cookies=cookies).text 
soup = BeautifulSoup(con, "lxml")
link = soup.find_all("input")

for kk in range(3,len(link)):
    print link[kk]

print ("==================================================================================================")

for nn in range(4,len(link)-1):
    try:
        tmp = link[nn]
        print "{}={}".format(tmp['name'], tmp['value'])
        payload[tmp['name']] = tmp['value']
    except BaseException:
        print "{}=".format(tmp['name'])

link = soup.find_all("script")

strlink = str(link[28])
lastindex = strlink.find('formData += "&')
print strlink[lastindex+14:lastindex+95]

#------------ MAKE PAYLOAD ------------#
print ("==================================================================================================")

jsform = strlink[lastindex+14:lastindex+95]
jsformKey = strlink[lastindex+14:lastindex+54]
jsformVal = strlink[lastindex+55:lastindex+95]

#print jsform
#print jsformKey
#print jsformVal

payload[jsformKey] = jsformVal

print payload
print ("==================================================================================================")

#------- DELETE REQUEST -------#
url="http://gall.dcinside.com/forms/delete_submit"

cookies = {'PHPSESSID':'tppd5m525urdfl5ufks81qmda1','ci_c':'5f89d862ed21f8bec46f296cc5f574b8','notice_no':'231721'}
#cookies = {'PHPSESSID':'tppd5m525urdfl5ufks81qmda1'}
headers = {'X-Requested-With':'XMLHttpRequest'}
"""
cookies = {
    'PHPSESSID':'tppd5m525urdfl5ufks81qmda1',
    '__utma':'118540316.646550753.1497001972.1497001972.1497001972.1',
    '__utmb':'118540316.39.10.1497001972',
    '__utmc':'118540316',
    '__utmz':'118540316.1497001972.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'unicro_id':'ZXhhbXBsZTBeMzE2MzA3MQ%3D%3D',
    'dc_check':'7fed8368b7866fe83feb8ffb44827d',
    'gn39adc':'39adc022b0df6df43baac4b110dd7128a7cf55a726ba6ce9c2ed',
    'dc_event':'ZXhhbXBsZTA7MzE2MzA3MTt0ZXN0OzIwMTctMDYtMDkgMTg6NTM6MDM%3D',
    'gn_cookie':'28a5d12bf5de3df6358bf386228a766d30f8ec39e4e0bf1f76902c5e222ff85037',
    'mc_enc':'28a5d12bf5de3df6',
    'ci_c':'5f89d862ed21f8bec46f296cc5f574b8',
    'service_code':'21ac6e96ad152e8f15a05b7350a24759b5606fa191c17e042e4d0175735f4d6eac761557a237c669c0d0e45298a725d20a30fe92e8659b4a16d371d58e380d127d177ae6f87536515dec54861bcf0b5c6685aeef78942029407f2d1920d5ae4a88f7cae49da1bf9f6288e9cbd6bc5e65af101c16b4734d94939848f1ded6b1456e8868e7d4f59c4545527a41776aef19fc148586ee016b7dbec621b16c87d196fb5dfb6eb18b5371d2',
    'notice_no':'231721',
    'lately_cookie':'japanese%7C%uC77C%uC5B4%7C9',
    'gallRecom':'MjAxNy0wNi0wOSAxOTo0MTozOC80YWQ5MjExZDE4NGI3OGE1ODU3ZDIxN2E0ZTM1Y2RmZGI1YTBkYzI2ZDUyMWNlNjk2MTlmOTUxZjYxZGZkY2Fm',
    'siteUniqId':'STU_593a759b9wRQVMgg',
}
"""
con = requests.post(url, data=payload, cookies=cookies, headers=headers)
print con
