"""
Author: Sean Sill
File: jsonparser.py
"""

# Notes
# Eventually I'd like to move to this kind of format
# http://www.jsonrpc.org/specification#error_object - We should really have
# everything work like this

import json
import logging
import struct
from pixversion import PixVersion
from PIL import Image, ImageDraw, ImageFont


__version__ = PixVersion("1.0.0")

FORMAT_WIF = 'wif'
FORMAT_RGB = 'RGB'
FORMAT_1BIT = "1"
VALID_FORMAT_TYPES = [FORMAT_WIF]
JSON_ENCODING = 'UTF-8'
    
def is_valid_format(format):
  """
  @brief A helper function used to determine if a str is a valid image format
  """
  if format in VALID_FORMAT_TYPES:
    return True
  else:
    return False

class RenderItem(object):
  """
  @brief Container class used by the json parser to output Image an object from
  the API
  """
  background="white"
  format=FORMAT_WIF
  _text_items = []
  
  def __init__(self, size):
    self.size = size
    self._text_items = []

  def __repr__(self):
    return ''.join(("RenderItem with size: ", str(self.size), self.background))
    
  def width(self):
    return self.size[1]
    
  def height(self):
    return self.size[0]
  
  def add_text(self, text_item):
    self._text_items.append(text_item) 
    
  def text_items(self):
    return self._text_items

    
class TextItem(object):
  """
  @brief Container class used by the json parser to output text objects found
  in the json
  """
  text = ''
  pos = (0,0)
  color = 'black'
  font = ''
  font_url = ''
  size = 12
  content_type = 'RGB'
  
  def __init__(self, text, pos):
    self.text = text
    self.pos = pos
    
  def __repr__(self):
    return ''.join(("TextItem with text: ", self.text, str(self.pos)))
 
 
class VersionError(Exception):
  pass

class ImageFormatError(Exception):
  pass
  
class MissingRequiredKey(Exception):
  pass
  

class PixRender(object):
  """
  @brief: This object exists solely to separate the image rendering and json
  parsing from the Web Interface so that it can be tested separately
  """
  def __init__(self, input_json):
    """
    @brief Constructor requires json to initialize
    """
    self.render_item = self.parse_json(input_json)
    
  def parse_json(self, json_str):
    """
    @brief Takes in a UTF-8 string of json and returns an image object, and
    multiple text objects to render in the image
    @param json_str is a utf-8 or ascii string that shall be parsed
    @return a tuple of (RenderItem, list of TextItem)
    @note Will raise LookupError if required json keys are not found
    """
    logging.info("JSON input: %s", json_str)
    json_dict = json.loads(json_str)
    
    # Check the version
    if json_dict.has_key('version') == False:
      raise MissingRequiredKey(" 'version' is a required key, 'x.y.z' ")
    
    if PixVersion(json_dict['version']) > __version__:
      raise VersionError("Incoming version is higher than our own!")
    
    # Check the encoding
    if json_dict.has_key('encoding'):
      if json_dict['encoding'] != JSON_ENCODING:
        raise ValueError("Invalid encoding")
    else:
      raise MissingRequiredKey(" 'encoding' required key is missing")
    
    # Check the requested output format
    if json_dict.has_key('format'):
      if is_valid_format(json_dict['format']):
        self.format = json_dict['format']
      else:
        raise ImageFormatError("Unsupported Image Format")
    else:
      raise MissingRequiredKey(" 'format' required key is missing")
    
    logging.info("type of json_dict %s", type(json_dict))
    if json_dict.has_key('text') == False:
      raise MissingRequiredKey("Missing 'text' key which should be a list of"
                               " json objects")
    
    # Check for required height, and width key
    if json_dict.has_key('height') and json_dict.has_key('width'):
      render_item = RenderItem((int(json_dict['height']),
                              int(json_dict['width'])))
    else:
      raise MissingRequiredKey("No height(int), or width(int) keys found. Both are"
                               " required.")
    
    if json_dict.has_key('format') and is_valid_format(json_dict['format']):
      render_item.format = json_dict['format']

    # Text is not a required key
    if json_dict.has_key('text'):
      text_list = json_dict['text']      
      for text_item in text_list:
        if text_item.has_key('x') and text_item.has_key('y') and \
           text_item.has_key('text'):
          new_item = TextItem(text_item['text'], (text_item['x'], text_item['y']))
          # Add optional items here with a if has key statement
          # text_item_list.append(new_item)
          render_item.add_text(new_item)
        else:
          raise LookupError(
              "Text item does not have all required keys,"
              "A text item must have keys - x(int), y(int), text(string)!")
    return render_item
    

  def _convert_to_wif_blob(self, input_im):
    """
    Expects the input to be an RGB image
    @param RGB PIL Image instance
    @return A base64 encoded string of data representing a wif file
    @note Based on code found here:
    http://wyolum.com/introducing-wif-the-wyolum-image-format/
    """
    # This changes to monochrome first
    im = Image.new("L", input_im.size)
    im = input_im.convert("L")
    # Convert to a 1 bit bitmap
    im = im.convert("1") 
    w, h = im.size
    data = ''.join(('', struct.pack('HH', h, w)))
    for j in range(h):
        for i in range(0, w, 8):
            byte = 0
            for bit_i in range(8):
                try:
                    bit = im.getpixel((i + bit_i, j)) < 255
                except:
                    bit = False
                # logging.log(' X'[bit])
                byte |= bit << bit_i
            data = ''.join((data, struct.pack('B', byte)))
    return data.encode('base64', 'strict')

  def render_image(self):
    """
    @brief Renders the image
    @return a base 64 encoded string of the image
    """
    logging.info("Attempting to create new Image")
    im = Image.new("RGB", self.render_item.size, self.render_item.background)
    draw = ImageDraw.Draw(im)
    for text_item in self.render_item.text_items():
      self.text_to_image(text_item, draw)
    data, content_type = self.convert(im)
    return data, content_type

  def convert(self, im):
    """
    @brief Converts a PIL image to wif
    @return a string of data
    """
    # Here is where we check for the output type of the
    # we should probably break any thing related to http from this...
    if self.render_item.format == FORMAT_WIF:
      return self._convert_to_wif_blob(im),  'application/wif'
    elif self.render_item.format == FORMAT_RGB:
      return self._convert_to_bmp(im), 'image/bmp'
    else:
      raise ImageFormatError("Unsupported Format")
      
  def text_to_image(self, text_item, draw):
    """
    @brief
    """
    logging.info("Attempting to draw new text")
    logging.info("Text: " + text_item.text)
    myfont = self.get_font(text_item)
    draw.text(text_item.pos, text_item.text, font=myfont, fill=text_item.color)
    
  def get_font(self, text_item):
    if text_item.font_url != '':
      # Here we need to check to see if the font file is already downloaded
      raise NotImplementedError("Font Urls are not yet supported")
    elif text_item.font != '':
      raise NotImplementedError(
          "Fonts other than the default are not supported")
    return ImageFont.load_default()
