from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

  (r'^admin/', include(admin.site.urls)),
    # pass all urls to interpreter
   (r'', include('shopply.interpreter.urls')),
)
