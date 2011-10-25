
from models import *
from shopply import settings

from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

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
    paramDic = defaultDictionary(request)
    response = HttpResponse()
    jsonString = simplejson.dumps( ['word1', 'word2', 'word3', str(datetime.datetime.today())] )
    response.write(jsonString)

    return response
