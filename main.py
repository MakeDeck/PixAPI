#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import logging
from pixapi import PixRender
# Add authentication library
# from themakedeck import auth

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Electric Imp!')

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
        # Write the dispatch code here
        # Get the image, height, text, font and other things from the request
        json_text = "{
              "version":"1.0.0",
              "encoding":"UTF-8",
              "width":512
              "height":512
              "text":[
                {
                  "text":"Here is some text",
                  "x":100,
                  "y":100
                }
              ]
         }")
        try:
          render = PixRender(json_text)
          im = render.render_image()
          self.response.content_type = "application/wif"
          self.response.write(im.tostring())
        except:
          # Return an error in the http response as well
          logging.error("Error in incoming message, add more to this message")
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/image', ImageHandler)
], debug=True)
