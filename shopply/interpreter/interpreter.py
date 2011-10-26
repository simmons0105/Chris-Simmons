
from models import *
from shopply import settings
import xml.parsers.expat
import re
import string

import pdb


class WordNode(object):
  word = None
  fEdges = {}
  nEdges = {}
  locations = []

  def __init__(self,  *args, **kwargs):
    self.word = None
    self.fEdges = {}
    self.nEdges = {}
    self.locations = []
    self.total_weight = 0
    return super(WordNode, self).__init__(*args, **kwargs)

  def calculate_weight(self):
    self.total_weight = 0
    for tup in self.locations:
      self.total_weight += tup[1]
    return self.total_weight


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
    element_name = element_name.upper()
    self.tag_stack.append((element_name, attrs, token))
    self.StartElementHandler(self, element_name, attrs)


  def pop_element(self, element_name, token):

    element_name = element_name.upper()
    index = len(self.tag_stack) - 1
    delList = []
    match = False

    #make sure that we have an available match before we actually do anything
    for tup in reversed(self.tag_stack):
      if tup[0] == element_name:
        match = True
        break

    #pop off elements until we find a matching tag
    if match:
      while self.tag_stack:
        tup = self.tag_stack.pop()
        self.EndElementHandler(self, tup[0])
        if tup[0] == element_name:
          break



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
  current_tag = None

  min_word_size = 4
  wb_size = 8 #word buffer size
  word_count = 0

  text_buffer = "" #keeps buffer of current text... flushes on certain tags
  word_buffer = [] #list of last n words
  tag_dic = {}
  G = {}

  def flushBuffers(self):
    self.text_buffer = ""
    self.word_buffer = []

  def update_current_tag(self, element):
    if element:
      self.current_tag = self.tag_dic.get(element, {'name':element,'is_block':False, 'weight':1.0})
    else:
      self.current_tag = {}

  def start_element(self, parser,  element, attrs):
    self.update_current_tag(element)

    if self.current_tag['is_block']:
      self.flushBuffers()

  def end_element(self,  parser, element):
    if self.current_tag['name'] == element and self.current_tag['is_block']:
      self.flushBuffers()

    if parser.tag_stack:
      tup = parser.tag_stack[-1]
      self.update_current_tag(tup[0])
    else:
      self.update_current_tag(None)

  def updateNode(self, node):
    node.locations.append((self.word_count, self.current_tag['weight']))

    #for each word in the current buffer we create two edges in the Graph
    #a negative edge from the current word to the previous nodes
    #and a positive edge from the previous nodes to the current node
    for idx in range(1,len(self.word_buffer)):
      pNode = self.word_buffer[idx]
      nEdge = (self.word_count,-idx )
      curEdges = node.nEdges.get(pNode.word, [])
      curEdges.append(nEdge)
      node.nEdges[pNode.word] = curEdges

      fEdge = (self.word_count, idx)
      fEdges = pNode.fEdges.get(node.word, [])
      fEdges.append(fEdge)
      pNode.fEdges[node.word] = fEdges

  def process_word(self, word):
    if (len(word) < self.min_word_size and word != word.upper()):
      return

    lword = word.lower()

    self.word_count += 1
    wNode = self.G.get(lword)
    if not wNode:
      wNode = WordNode()
      wNode.word = lword
      self.G[lword] = wNode

    self.word_buffer.insert(0,wNode)
    if len(self.word_buffer) > self.wb_size:
      self.word_buffer.pop()

    self.updateNode(wNode)



  def handle_data(self,  parser, data):
    if not self.current_tag['weight']:
        return

    #remove all special characters such as &amp; and &nbsp;
    data = re.sub('&\w+;', "" , data)
    self.text_buffer += data
    word_data = re.split("[^a-zA-Z0-9']+", data)

    #cycle through each word and add to the graph
    for word in word_data:
      if word.strip():
        self.process_word(word)

  def __init__(self,  *args, **kwargs):

    self.parser = XMLParser()

    self.parser.StartElementHandler = self.start_element
    self.parser.EndElementHandler = self.end_element
    self.parser.CharacterDataHandler = self.handle_data

    #TODO - cache this so we are not making this call for every request
    tagList = TagElement.objects.all().values("name", "is_block", "weight")
    for t in tagList:
      self.tag_dic[t['name']] = t

    return super(Interpreter, self).__init__(*args, **kwargs)

  def processXML(self, xmlData):
    try:
      xmlData = xmlData.encode('ascii','ignore')
      self.parser.parse(xmlData)

      for node in self.G.values():
        w = node.calculate_weight()
        print node.word + " " + str(w)
    except Exception, e:
      print e