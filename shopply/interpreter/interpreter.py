__author__ = 'chrissimmons'


from models import *
from shopply import settings

import pdb


class Interpreter(object):
  url = None
  def __init__(self, url, *args, **kwargs):
    self.url = url
    return super(Interpreter, self).__init__(*args, **kwargs)
  