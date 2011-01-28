from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

x_char = 'X'
o_char = 'O'

def index(request):
    return render_to_response('index.html', {
        'x_char': x_char,
        'o_char': o_char,
        'rows': range(3),
        'cols': range(3)
    })

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

def ai_move(request):
    board = json.loads(request.POST.get('board'))
    
    ai_char, player_char = char_move_order(board)
    
    best_value = -2 # Lower than lowest possible value
    best_move = None
    
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                move = {'row': i, 'col': j}
                
                board[i][j] = ai_char
                
                if(board_winner(board) == ai_char):
                    # We've won, make this move
                    return HttpResponse(json.dumps(move))
                    
                value = board_value(board, player_char, ai_char, -2, 2) # Lower and higher than min and max possible values
                board[i][j] = None
                
                if value > best_value:
                    best_value = value
                    best_move = move
    
    return HttpResponse(json.dumps(best_move))
    
# TODO:
# Implement ability to choose player's piece
# Fix up UI
