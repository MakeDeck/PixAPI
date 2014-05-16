import pixapi
import json
import test.testutils
from PIL import Image
from StringIO import StringIO


GOOD_INPUT_JSON = u"""
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

if __name__ == '__main__':
  imageStore = pixapi.ImageStore()
  render = pixapi.PixRender(GOOD_INPUT_JSON, imageStore)
  test.testutils.SimpleShow(render.render_image())