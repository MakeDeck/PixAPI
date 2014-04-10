"""
Author: Sean Sill
File: jsonparser.py
"""

import json
import logging
from PIL import Image, ImageDraw, ImageFont


FORMAT_WIF = 'wif'
FORMAT_TYPES = [FORMAT_WIF]


def IsValidFormat(format):
  """
  @brief A helper function used to determine if a str is a valid image format
  """
  if format in FORMAT_TYPES:
    return True
  else:
    return False

class ImageItem(object):
  """
  @brief Container class used by the json parser to output Image an object from
  the API
  """
  background="white"
  format=FORMAT_WIF
  
  def __init__(self, size):
    self.size = size

  def __repr__(self):
    return ''.join(("ImageItem with size: ", str(self.size), self.background))
    
  def width(self):
    return self.size[1]
    
  def height(self):
    return self.size[0]

    
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
   
  def __init__(self, text, pos):
    self.text = text
    self.pos = pos
    
  def __repr__(self):
    return ''.join(("TextItem with text: ", self.text, str(self.pos)))
  
class PixRender(object):
  """
  @brief: This object exists solely to separate the image rendering and json
  parsing from the Web Interface so that it can be tested separately
  """
  def __init__(self, input_json):
    """
    @brief Constructor requires json to initialize
    """
    self.image_item, self.text_items = self.parse_json(input_json)
    
  def parse_json(self, json_str):
    """
    @brief Takes in a UTF-8 string of json and returns an image object, and
    multiple text objects to render in the image
    @param json_str is a utf-8 or ascii string that shall be parsed
    @return a tuple of (ImageItem, list of TextItem)
    @note Will raise LookupError if required json keys are not found
    """
    logging.debug("JSON input: %s", json_str)
    json_dict = json.loads(json_str)
    
    # We need to check for versioning here, if we get a higher version than we
    # parse we should raise an error
    
    text_list = json_dict['text']
    if json_dict.has_key('height') and json_dict.has_key('width'):
      image_item = ImageItem((int(json_dict['height']),
                              int(json_dict['width'])))
    else:
      raise LookupError("No height, or width keys found")
    
    if json_dict.has_key('format') and IsValidFormat(json_dict['format']):
      image_item.format = json_dict['format']
      
    text_item_list = []
    for text_item in text_list:
      if text_item.has_key('x') and text_item.has_key('y') and \
         text_item.has_key('text'):
        new_item = TextItem(text_item['text'], (text_item['x'], text_item['y']))
        # Add optional items here with a if has key statement
        text_item_list.append(new_item)
      else:
        raise LookupError(
            "Text item does not have all required keys, x, y, text!")
      if text_item.has_key('font_url'):
        logging.debug("Found font_url key")
    return (image_item, text_item_list)
    
    
  def render_image(self):
    """
    @brief Renders the image
    @return Returns an PIL.Image
    """
    logging.info("Attempting to create new Image")
    im = Image.new("RGB", self.image_item.size, self.image_item.background)
    draw = ImageDraw.Draw(im)
    for text_item in self.text_items:
      self.text_to_image(draw, text_item)
    # Check output type
    im = im.convert("1") # Convert to a 1 bit bitmap
    return im
    
  def text_to_image(self, draw, text_item):
    logging.info("Attempting to draw new text")
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