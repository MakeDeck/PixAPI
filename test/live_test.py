import urllib2
import json
import testutils
from PIL import Image
from StringIO import StringIO

url = "http://1-1-test.imp-pix-api.appspot.com/image"
# url = "http://imp-pix-api.appspot.com/image"
# url = "http://192.168.0.5:8080/image"
#url = "http://127.0.0.1:8080/image"


GOOD_INPUT_JSON = u"""
{
  "version":"1.0.0",
  "encoding":"UTF-8",
  "width":100,
  "height":100,
  "format":"wif",
  "text":[
    {
      "text":"Here is some text",
      "x":1,
      "y":1
    },
    {
      "text":"Here is some more text",
      "x":2,
      "y":10
    }
  ]
}
"""

GOOD_INPUT_IMAGE_JSON = u"""
{
  "version":"1.0.0",
  "encoding":"UTF-8",
  "width":100,
  "height":100,
  "format":"wif",
  "image":[
    {
      "url":"http://cdn.shopify.com/s/files/1/0370/6457/t/4/assets/logo.png",
      "x":10,
      "y":10
    }
  ]
}
"""

BAD_VERSION_INPUT_JSON = u"""
{
  "version":"1.x.0",
  "encoding":"UTF-8",
  "width":100,
  "height":100,
  "format":"wif",
  "text":[
    {
      "text":"Here is some text",
      "x":1,
      "y":1
    },
    {
      "text":"Here is some more text",
      "x":2,
      "y":10
    }
  ]
}
"""
request = urllib2.Request(url, data=GOOD_INPUT_IMAGE_JSON, headers={"content-type":"application/json"})
print "HELLO", request.get_method()
response = urllib2.urlopen(request)
print response
data = ''
for line in response:
  data = ''.join((data, line))
data = data.decode('base64', 'strict')
print data.encode('hex')
print len(data)
im = Image.fromstring("1", (100, 100), data)
testutils.SimpleShow(im)