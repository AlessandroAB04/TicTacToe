import pygame
import sys
import time

import tictactoe as ttt

# Inizializza Pygame
pygame.init()
size = width, height = 600, 400

# Colori
black = (0, 0, 0)
white = (255, 255, 255)

# Crea la finestra di gioco
screen = pygame.display.set_mode(size)

# Carica i font per il testo
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

# Variabili per il giocatore e lo stato della griglia
user = None
board = ttt.initial_state()  # Stato iniziale della griglia
ai_turn = False  # Indica se è il turno dell'AI

# Ciclo principale del gioco
while True:

    # Gestisce gli eventi Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Esce dal programma se si chiude la finestra

    # Riempie lo schermo di nero
    screen.fill(black)

    # Consente all'utente di scegliere un giocatore.
    if user is None:

        # Disegna il titolo
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Disegna i pulsanti
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Controlla se un pulsante è stato cliccato
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)  # Pausa per evitare clic ripetuti
                user = ttt.X  # Imposta l'utente come X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)  # Pausa per evitare clic ripetuti
                user = ttt.O  # Imposta l'utente come O

    else:
        # Disegna la griglia di gioco
        tile_size = 80  # Dimensione delle celle
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []  # Lista per contenere le celle della griglia
        for i in range(3):
            row = []  # Lista per una riga della griglia
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)  # Disegna il contorno della cella

                # Disegna il segno (X o O) nella cella
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)  # Controlla se il gioco è finito
        player = ttt.player(board)  # Ottieni il giocatore corrente

        # Mostra il titolo
        if game_over:
            winner = ttt.winner(board)  # Ottieni il vincitore
            if winner is None:
                title = f"Game Over: Tie."  # Se c'è un pareggio
            else:
                title = f"Game Over: {winner} wins."  # Annuncia il vincitore
        elif user == player:
            title = f"Play as {user}"  # Indica a chi è il turno
        else:
            title = f"Computer thinking..."  # Indica che è il turno dell'AI
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Controlla il movimento dell'AI
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)  # Pausa per simulare il pensiero dell'AI
                move = ttt.minimax(board)  # Calcola la mossa ottimale per l'AI
                board = ttt.result(board, move)  # Aggiorna la griglia con la mossa dell'AI
                ai_turn = False  # Cambia turno
            else:
                ai_turn = True  # Indica che l'AI ha il turno

        # Controlla il movimento dell'utente
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    # Controlla se l'utente ha cliccato su una cella vuota
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))  # Aggiorna la griglia con la mossa dell'utente

        # Se il gioco è finito, mostra il pulsante per ricominciare
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                # Controlla se il pulsante "Play Again" è stato cliccato
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)  # Pausa per evitare clic ripetuti
                    user = None  # Resetta l'utente
                    board = ttt.initial_state()  # Resetta la griglia
                    ai_turn = False  # Resetta il turno dell'AI

    pygame.display.flip()  # Aggiorna il display
