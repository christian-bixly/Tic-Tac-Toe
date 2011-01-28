from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html', {
        'rows': range(3),
        'cols': range(3)
    })

# TODO:
# First make game playable, with random AI
# Generate moves DB
# Make AI query moves DB
# Profit
