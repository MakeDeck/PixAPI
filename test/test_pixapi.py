"""
@brief This is the main test for pixapi
@author Sean Sill
@file test_pixapi.py

"""

import unittest
import pixapi

GOOD_INPUT_JSON = u"""
{
  "version":"1.0.0",
  "encoding":"UTF-8",
  "width":400,
  "height":512,
  "text":[
    {
      "text":"Here is some text",
      "x":100,
      "y":100
    },
    {
      "text":"Here is some more text",
      "x":50,
      "y":50
    }
  ]
}
"""

INVALID_FORMAT_JSON = u"""
{
  "version":"1.0.0",
  "encoding":"UTF-8",
  "width":400,
  "height":512,
  "format":"RGB"
  "text":[
    {
      "text":"Here is some text",
      "x":100,
      "y":100
    },
    {
      "text":"Here is some more text",
      "x":50,
      "y":50
    }
  ]
}
"""

INVALID_JSON = u"{[}"

# Verify TextItem does not modify internal contents

# Verfify ImageItem does not modify internal contents

# Verify how pixapi behaves with correct and incorrect json

# Test that you get an image back

# Possibly test with test images to compare against

# Test with UTF-8 and ascii

class PixApiTestCase(unittest.TestCase):
    
  def runTest(self):
    print "Here is a test"
    print pixapi
    
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()