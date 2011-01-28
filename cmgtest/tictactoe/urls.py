from django.conf.urls.defaults import *

urlpatterns = patterns('tictactoe.views',
    (r'^$', 'index'),
)
