
from models import *
from shopply import settings

from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from interpreter import  Interpreter

import datetime
import pdb  


def defaultDictionary(request):
    paramDic = {'MEDIA_URL': settings.MEDIA_URL,
#                'current_user' : request.user,
                'current_url' : request.path,
                'today': datetime.datetime.today(),
                }
    

    return paramDic


def index(request):

    response = HttpResponse()
    try:
      active_xml = request.POST.get('activexml')

      if not active_xml:
        response.write("Failure - Please post with valid XML string to process.")
        return response
      interp = Interpreter()
      interp.processXML(active_xml)
      interpList = interp.topPhraseList(count = 3)

      outputList = [interp.word_count]
      for tup in interpList:
        outputList.append({'keyPhrase':tup[0], "iCount" : tup[1], "weight":tup[2]})

      jsonString = simplejson.dumps( outputList )
      print outputList
      response.write(jsonString)

      return response

    except Exception, e:
      print e
      response.write(str(e))
      return response
