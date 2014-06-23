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
# Eventually I'd like to move to this kind of format
# http://www.jsonrpc.org/specification#error_object - We should really have
# everything work like this
#

import webapp2
import logging
from google.appengine.api import users
from pixapi import PixRender, ImageStore
from pixapi import VersionError, ImageFormatError, MissingRequiredKey
# Add authentication library
# from themakedeck import auth

imageStore = ImageStore()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Pix API')

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
          # Check for correct headers here as well, application/json
          # Write the dispatch code here
          # Get the image, height, text, font and other things from the request
          logging.info("Received new request for an image")
          # Check Auth here
          if self.request.headers['content_type'] != 'application/json':
            logging.error('Invalid header received, expected content_type == '
                          'application/json got: %s', self.request.headers['content_type'])
            self.response.set_status(500)
            self.response.write('Invalid headers, expected content_type =='
                                ' application/json')
            return
          json_text = self.request.body
          try:
            render = PixRender(json_text, imageStore)
          except ValueError as e:
            logging.error("Invalid json received, %s", e)
            self.response.set_status(500)
            self.response.write("Invalid json")
            return
          except MissingRequiredKey as e:
            logging.error("A required key was missing, %s", e)
            self.response.set_status(500)
            self.response.write("Invalid json, Error Message: ")
            self.response.write(str(e))
            return
          except VersionError as e:
            logging.error("Value recieved is greater than we support %s", e)
            self.response.set_status(500)
            self.response.write("Version greater than supported version!")
            return
          except ImageFormatError as e:
            logging.error("Image format unsupported! %s", e)
            self.response.set_status(500)
            self.response.write("Image format unspported! Error Message: ")
            self.response.write(str(e))
            return
          data, content_type = render.render_image()
          self.response.content_type = content_type
          self.response.write(data)
          logging.info("Image rendered")
        
class ManagementHandler(webapp2.RequestHandler):
    def get(self):
        """
        Serve the Api Key management service
        """
        user = users.get_current_user()
        if user:
            self.response.write('Place Holder')
        else:
            self.redirect(users.create_login_url(self.request.uri))
        return
    
    def post(self):
        """
        Post a request for a new key
        """
        user = users.get_current_user()
        if user:
            self.response.write('Place Holder')
        else:
          self.response.set_status(500)
          self.response.write("Invalid User")
        return

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/image', ImageHandler),
    ('/manage', ManagementHandler)
], debug=True)
