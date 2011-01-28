from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

def index(request):
    return render_to_response('index.html', {
        'rows': range(3),
        'cols': range(3)
    })

def ai_move(request):
    board = json.loads(request.POST.get('board'))
    
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                return HttpResponse(json.dumps({'row': i, 'col': j}))
    
# TODO:
# First make game playable, with random AI
# Generate moves DB
# Make AI query moves DB
# Profit
