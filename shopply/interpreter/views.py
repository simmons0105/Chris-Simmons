
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

    active_xml = request.POST.get('activexml')

    response = HttpResponse()
    if not active_xml:
      response.write("Failure - Please post with valid XML string to process.")
      return response

    interp = Interpreter()
    interp.processXML(active_xml)


    jsonString = simplejson.dumps( [{'keyPhrase':'phrase1', 'iCount':45,'weight':94.456,},
                                    {'keyPhrase':'phrase2', 'iCount':30,'weight':81.4436,},
                                    {'keyPhrase':'phrase3', 'iCount':29,'weight':79.827,},
                                    str(datetime.datetime.today()),
                                    ] )
    response.write(jsonString)

    return response
