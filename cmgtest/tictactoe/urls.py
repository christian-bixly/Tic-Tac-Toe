from django.conf.urls.defaults import *

urlpatterns = patterns('tictactoe.views',
    (r'^$', 'index'),
    url(r'^ai_move$', 'ai_move', name='ai_move'),
)
