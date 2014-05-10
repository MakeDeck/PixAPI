"""
@brief Class to hold versions
"""

class PixVersion(object):
  """
  @brief Creates a version object from a string
  """
  def __init__(self, str):
    self.version = self.version_from_string(str)
    
  def version_from_string(self, str):
    l = str.rsplit('.', 2)
    if len(l) < 3:
      raise ValueError
    return (int(l[0]), int(l[1]), int(l[2]))
    
  def __lt__(self, other):
    for id, o_id in zip(self.version, other.version):
      if o_id < id:
        return True
      elif o_id > id:
        return False
    return False
    
  def __le__(self, other):
    for id, o_id in zip(self.version, other.version):
      if o_id < id:
        return True
      elif o_id > id:
        return False
    return True
    
  def __eq__(self, other):
    return self.version == other.version
    
  def __ne__(self, other):
    return self.version != other.version
    
  def __gt__(self, other):
    for id, o_id in zip(self.version, other.version):
      if o_id < id:
        return False
      elif o_id > id:
        return True
    return False
    
  def __ge__(self, other):
    for id, o_id in zip(self.version, other.version):
      if o_id < id:
        return False
      elif o_id > id:
        return True
    return True
