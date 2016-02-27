from django.conf.urls import patterns, include, url

import app


urlpatterns = patterns('',
                       url(r'^', include(app.urls)),
                       url(r'^docs/', include('rest_framework_swagger.urls')),
                       )
