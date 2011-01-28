from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^(?:.*/)?(?P<path>(css|img|js)/.+)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^$', 'tictactoe.views.index'),
    (r'^tictactoe/', include('tictactoe.urls')),
    (r'^admin/', include(admin.site.urls)),
)
