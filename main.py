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
import os
import uuid
import webapp2
import logging
from sharded_counter import GeneralCounterShard
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from pixapi import PixRender, ImageStore
from pixapi import VersionError, ImageFormatError, MissingRequiredKey
import json
# Add authentication library
# from themakedeck import auth

QUOTA_LIMIT = 3000 # Number of requests in a given time.
imageStore = ImageStore()

class ApiKeyModel(GeneralCounterShard):
    user = ndb.UserProperty()
    key = ndb.StringProperty(indexed=True)
    
    @classmethod
    def query_get_keys_by_user(cls, user):
        return cls.query(cls.user == user)
   
    def query_get_key_by_key(cls, key):
        return cls.query(cls.key == key)
        
    def get_quota(self):
        return self.get_count('quota')

class ApiKey(object):
    _key = ''
    _user = ''
    _quota = 0
    
    @property
    def key(self):
        return self._key
      
    @property
    def user(self):
        return self._user
    
    @property
    def quota(self):
        return self._quota
        
    @classmethod
    def from_model(cls, model):
        key = ApiKey()
        key._key = model.key
        key._user = model.user
        key._quota = model.get_quota()
        return key
    
class KeyStore(object):
    """
    Used to find a key in the datastore and update its quota
    """
    _limit = 0
    
    def __init__(self, quota_limit):
        self._limit = quota_limit

    def find_key_by_user(self, user_id):
        key_models = ApiKeyModel.query_get_key_by_user(user_id)
        if len(key_models) > 0:
            return ApiKey.from_model(key_models[0])
        return None
        
    def find_keys_by_user(self, user_id):
        key_models = ApiKeyModel.query_get_key_by_user(user_id)
        if len(key_models) > 0:
            keys = []
            for key_model in key_models:
                keys.append(ApiKey.from_model(key_model))
            return keys
        return None

    def find_key_by_key(self, key):
        key_model = ApiKeyModel.query_get_key_by_key(key)
        # Check for multiples here
        return ApiKey.from_model(key_model)
        
    def insert_new_key(self, user_id):
        api_keys = ApiKey.query_get_key_by_user(user).fetch()
        if len(api_keys) == 0:
            new_key = uuid.uuid4()
            api_key = ApiKey(user=user, key=str(new_key))
            api_key.put()
            return 
        return None
        
    def update_key_quota(self, key):
        return 0
        
    def reset_key_quota(self, key):
        return 0
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Pix API')

class AuthorizationError(Exception):
  pass
  
def IncrementQuota(headers):
    if headers.has_key('Authorization'):
        auth_value = headers['Authorization']
        basic, sep, key = auth_value.partition(' ')
        if basic == 'Basic'
        return True
    else:
        raise AuthorizationError('Invalid Authorization Headers')

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
          # Check for correct headers here as well, application/json
          # Write the dispatch code here
          # Get the image, height, text, font and other things from the request
          logging.info("Received new request for an image")
          
          try:
            IncrementQuota(self.request.headers)
          except AuthorizationError as e:
            self.response.set_status(401)
            self.response.write(e)
          except Exception as e:
            self.response.write(e)
          
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
            key_store = KeyStore(QUOTA_LIMIT)
            keys = key_store.get_keys_by_user(user)
            template_values = {'keys':[]}
            for key in keys:
                template_values['keys'].append(key.key)
            path = os.path.join(os.path.dirname(__file__), 'html', 'manage.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
    
    def post(self):
        """
        Post a request for a new key
        """
        user = users.get_current_user()
        if user:
            self.response.write(user.nickname() + 'Place Holder')
        else:
          self.response.set_status(500)
          self.response.write("Invalid User")
        return

class KeyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            key_store = KeyStore(QUOTA_LIMIT)
            self.response.headers['content_type'] = 'application/json'
            keys = key_store.get_keys_by_user(user)
            json_obj = {}
            json_obj['api_keys'] = []
            for key in keys:
                json_obj['api_keys'].append(key.key)
            json.dump(json_obj, self.response)
        else:
            self.response.set_status(500)
            self.response.write("Invalid User")
        return
    
    def post(self):
        key_store = KeyStore(QUOTA_LIMIT)
        user = users.get_current_user()
        if user:
            new_key = key_store.insert_new_key(user)
            if new_key != None:
                json_obj = {}
                json_obj['Status'] = 'Success'
                json.dump(json_obj, self.response)
                return
            else:
                json_obj = {}
                json_obj['Status'] = 'Error'
                json_obj['Value'] = 'Only one key allowed'
                json.dump(json_obj, self.response)            
        else:
            self.response.set_status(500)
            self.response.write("Invalid User")
        return

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/image', ImageHandler),
    ('/manage', ManagementHandler),
    ('/key', KeyHandler)
], debug=True)
