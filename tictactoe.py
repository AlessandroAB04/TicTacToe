"""
Giocatore Tic Tac Toe
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Restituisce lo stato iniziale della griglia di gioco.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Restituisce il giocatore che ha il prossimo turno sulla griglia.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    """
    Restituisce l'insieme di tutte le azioni possibili (i, j) disponibili sulla griglia.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
                
    return possible_actions


def result(board, action):
    """
    Restituisce la griglia risultante dal movimento (i, j) eseguito sulla griglia attuale.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Azione non valida: la cella non è vuota.")
    # Crea una copia profonda della griglia per evitare modifiche alla griglia originale
    new_board = copy.deepcopy(board)
    # Assegna la mossa al giocatore corrente
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Restituisce il vincitore della partita, se c'è.
    """
    for i in range(3):
        # Controlla la riga i
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        # Controlla la colonna i
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
    # Controlla le diagonali per trovare un vincitore
    # Diagonale principale
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    # Diagonale secondaria
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    # Se non c'è un vincitore, restituisce None
    return None


def terminal(board):
    """
    Restituisce True se la partita è terminata, False altrimenti.
    """
    # Controlla se c'è un vincitore
    if winner(board) is not None:
        return True
    
    # Controlla se tutte le celle sono riempite
    for row in board:
        if EMPTY in row:
            return False  # La partita è ancora in corso se c'è una cella vuota
    
    # Se non c'è un vincitore e non ci sono celle vuote, la partita è finita (pareggio)
    return True


def utility(board):
    """
    Restituisce 1 se X ha vinto la partita, -1 se O ha vinto, 0 altrimenti.
    """
    win = winner(board)
    
    # Restituisce il valore di utilità appropriato in base al vincitore
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Restituisce l'azione ottimale per il giocatore corrente sulla griglia.
    """
     # Se la partita è finita, restituisce None
    if terminal(board):
        return None
    
    # Determina il giocatore corrente
    current_player = player(board)
    
    # Definisce le funzioni max_value e min_value per la valutazione ricorsiva
    def max_value(board):
        # Se la partita è finita, restituisce il valore di utilità
        if terminal(board):
            return utility(board)
        
        v = -math.inf
        # Cerca l'azione che massimizza il valore per X
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v
    
    def min_value(board):
        # Se la partita è finita, restituisce il valore di utilità
        if terminal(board):
            return utility(board)
        
        v = math.inf
        # Cerca l'azione che minimizza il valore per O
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
    
    # Trova l'azione ottimale in base al giocatore corrente
    best_action = None
    if current_player == X:
        best_value = -math.inf
        # X cerca di massimizzare il valore
        for action in actions(board):
            action_value = min_value(result(board, action))
            if action_value > best_value:
                best_value = action_value
                best_action = action
    else:
        best_value = math.inf
        # O cerca di minimizzare il valore
        for action in actions(board):
            action_value = max_value(result(board, action))
            if action_value < best_value:
                best_value = action_value
                best_action = action
    
    return best_action
