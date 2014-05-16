"""
@brief This is the main test for pixapi
@author Sean Sill
@file test_pixapi.py

"""

import unittest
import pixapi
from testutils import TestCase

# Verify TextItem does not modify internal contents

# Verfify ImageItem does not modify internal contents

# Verify how pixapi behaves with correct and incorrect json

# Test that you get an image back

# Possibly test with test images to compare against

# Test with UTF-8 and ascii

class MockImageStore():
  def FetchImageFromURL(url):
    return

class PixApiGeneralTest(TestCase):
  """
  @brief Check how PixAPI responds to known good json!
  """
  input_json = u"""
{
  "version":"1.0.0",
  "encoding":"UTF-8",
  "width":400,
  "height":512,
  "format":"wif",
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
  def runTest(self):
    render = pixapi.PixRender(self.input_json, MockImageStore())
    print pixapi
    
  def tearDown(self):
    pass
    
    
class PixApiBadJsonTest(TestCase):
  """
  @brief Check how PixAPI responds to invalid json
  """
  INVALID_JSON = u"{[}"
  def runTest(self):
    self.assertRaises(ValueError, pixapi.PixRender, self.INVALID_JSON,
                      MockImageStore())

    
class PixApiBadFormatJsonTest(TestCase):
  """
  @brief Check how PixAPI responds to an invalid image format
  """
  input_json = u"""
{
  "version":"1.0.0",
  "encoding":"UTF-8",
  "width":10,
  "height":10,
  "format":"xxx",
  "text":[
    {
      "text":"x",
      "x":1,
      "y":1
    }
  ]
}
"""
  def runTest(self):
    self.assertRaises(pixapi.ImageFormatError, pixapi.PixRender,
                      self.input_json, MockImageStore())

if __name__ == '__main__':
  unittest.main()
