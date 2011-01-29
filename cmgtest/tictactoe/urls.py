from django.conf.urls.defaults import *

urlpatterns = patterns('tictactoe.views',
    (r'^$', 'index'),
    url(r'^start_game$', 'start_game', name='start_game'),
    url(r'^end_game$', 'end_game', name='end_game'),
    url(r'^ai_move$', 'ai_move', name='ai_move'),
)
