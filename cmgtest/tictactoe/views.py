from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import TTTSession
import json
import re

x_char = 'X'
o_char = 'O'

def index(request):
    return render_to_response('index.html', {
        'x_char': x_char,
        'o_char': o_char,
        'rows': range(3),
        'cols': range(3)
    })

def start_game(request):
    # Generate new session
    ttt_session = TTTSession.new_session()
    
    return HttpResponse(json.dumps({'session': ttt_session.session}))

def end_game(request):
    try:
        ttt_session = TTTSession.objects.get(session=request.POST.get('session'))
    except TTTSession.DoesNotExist:
        return HttpResponse(json.dumps('dup'))
    else:
        ttt_session.delete()
        
        return HttpResponse(json.dumps('ok'))

def char_move_order(board):
    n_x = 0
    n_o = 0
    
    for row in board:
        for cell in row:
            if cell == x_char:
                n_x = n_x + 1
            elif cell == o_char:
                n_o = n_o + 1
    
    if n_x == n_o:
        return x_char, o_char
    else:
        return o_char, x_char
        
def board_winner(board):
    # Check horizontals
    for row in board:
        ch = row[0]
        
        if ch is None:
            continue
        
        if ch == row[1] and ch == row[2]:
            return ch
    
    # Check verticals
    for i in range(3):
        ch = board[0][i]
        
        if ch is None:
            continue
        
        if ch == board[1][i] and ch == board[2][i]:
            return ch
    
    
    # Check left diagonal
    ch = board[0][0]
    
    if ch is not None:
        if ch == board[1][1] and ch == board[2][2]:
            return ch
    
    # Check right diagonal
    ch = board[0][2]
    
    if ch is not None:
        if ch == board[1][1] and ch == board[2][0]:
            return ch
    
    # No winner
    return None

def board_has_move(board):
    for row in board:
        for cell in row:
            if cell is None:
                return True
    
    return False

def board_value(board, cur_char, next_char, alpha, beta):
    winner = board_winner(board)
    
    if winner is not None:
        return {x_char: -1, o_char: 1}[winner]
    
    if not board_has_move(board):
        return 0
    
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                board[i][j] = cur_char
                value = board_value(board, next_char, cur_char, alpha, beta)
                board[i][j] = None
                
                if cur_char == o_char:
                    # maximize
                    if value > alpha:
                        alpha = value
                        
                    if alpha >= beta:
                        return beta
                else:
                    # minimize
                    if value < beta:
                        beta = value
                    
                    if beta <= alpha:
                        return alpha
    
    return {o_char: alpha, x_char: beta}[cur_char]

def stringify_board(board):
    return "".join([str(item) if item is not None else ' ' for sublist in board for item in sublist])

def ai_move(request):
    # Load the session
    session = request.POST.get('session')
    
    try:
        ttt_session = TTTSession.objects.get(session=session)
    except TTTSession.DoesNotExist:
        return HttpResponse(json.dumps({'success': False, 'error': 'invalid session'}))
    
    board = json.loads(request.POST.get('board'))
    
    # Validate board before proceeding
    str_board = stringify_board(board)
    
    if re.match('.*[^%s%s ]' % (x_char, o_char), str_board) is not None:
        return HttpResponse(json.dumps({'success': False, 'error': 'invalid board char'}))
    
    if not ttt_session.validate_against(str_board):
        return HttpResponse(json.dumps({'success': False, 'error': 'invalid board state'}))
    
    ai_char, player_char = char_move_order(board)
    
    if ai_char == o_char:
        best_value = -2 # Lower than lowest possible value
        compare = cmp
    else:
        best_value = 2 # Higher than highest possible value
        compare = lambda x, y: cmp(y, x)
    best_move = None
    
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                move = {'row': i, 'col': j}
                
                board[i][j] = ai_char
                
                if(board_winner(board) == ai_char):
                    # We've won, make this move
                    ttt_session.board = stringify_board(board)
                    ttt_session.save()
                    
                    return HttpResponse(json.dumps({'success': True, 'move': move}))
                    
                value = board_value(board, player_char, ai_char, -2, 2) # Lower and higher than min and max possible values
                board[i][j] = None
                
                if compare(value, best_value) > 0:
                    best_value = value
                    best_move = move
    
    # Update board stored with session
    board[best_move['row']][best_move['col']] = ai_char
    ttt_session.board = stringify_board(board)
    ttt_session.save()
    
    return HttpResponse(json.dumps({'success': True, 'move': best_move}))
