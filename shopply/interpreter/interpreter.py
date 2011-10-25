
from models import *
from shopply import settings
import xml.parsers.expat
import re

import pdb


#Decided to implement a naive parser because the python built in XML parsers
# error out on any invalid XML
# This may not be perfect but at least it will get through the text

#normally I would have tested some open source 3rd party solutions but the test
#seemed to frown upon that
class XMLParser(object):
  StartElementHandler = None
  EndElementHandler = None
  CharacterDataHandler = None

  tag_stack = []


  def push_element(self, element_name, attrs, token):

    self.tag_stack.append((element_name, attrs, token))
    self.StartElementHandler(self, element_name, attrs)


  def pop_element(self, element_name, token):

    index = len(self.tag_stack) - 1
    delList = []
    match = False
    #pop off elements until we find a matching tag
    while self.tag_stack:
      tup = self.tag_stack.pop()
      delList.append(tup)
      if tup[0] == element_name:
        match = True
        break

    #indicates that there was no matching element
    #assume current token is an error and restore the tag_list
    if not match:
      self.tag_stack = delList.reverse()
      #may want to pass error along
    else:
      self.EndElementHandler(self, element_name )


  def process_element(self, token, element_name):
    #TODO parse the rest of the tokens for attributes
    attrs = {}
    self.push_element(element_name, attrs, token)

  def process_end_element(self, token, element_name):
    #may want to do further processing to ensure validity
    self.pop_element(element_name, token)

  def process_invalid_data(self, token):
    #TODO pass along to allow delegate to handle
    pass

  def process_data(self, token):
    self.CharacterDataHandler(self, token)
  
  def parse(self, xmlData):
    self.tokens = re.split("(<[^>]+>)", xmlData)
    self.token_pos = 0
    for token in self.tokens:
      if not token.strip():
        continue #empty string 

      regexRes = re.search("<\s*([a-zA-Z0-9]+)", token.strip())
      if regexRes:
        self.process_element(token, regexRes.groups()[0])
        continue

      regexRes = re.search("<\s*/\s*([a-zA-Z0-9]+)", token.strip())
      if regexRes:
        self.process_end_element(token, regexRes.groups()[0])
        continue

      if re.search("<|>", token.strip()):
        self.process_invalid_data(token)
        continue

      self.process_data(token)
      self.token_pos += 1
      

class Interpreter(object):
  xmlString  = None
  current_element = None
  ignore_data = False

  def start_element(self, parser,  element, attrs):
    self.current_element = element
    if element in ['link', 'script', 'style']:
      self.ignore_data = True
    print "start %s %s" % (str(element), str(attrs))

  def end_element(self,  parser, element):
    self.ignore_data = False
    print "end %s" % (str(element),)

  def handle_data(self,  parser, data):
    if self.ignore_data:
        return
    
    print "Data %s" % (str(data),)

  def __init__(self,  *args, **kwargs):

    self.parser = XMLParser()
#    self.parser.returns_unicode = True
    self.parser.StartElementHandler = self.start_element
    self.parser.EndElementHandler = self.end_element
    self.parser.CharacterDataHandler = self.handle_data

    return super(Interpreter, self).__init__(*args, **kwargs)

  def processXML(self, xmlData):
    try:
      xmlData = xmlData.encode('ascii','ignore')
      self.parser.parse(xmlData)
    except Exception, e:
      print e