from math import inf as infinity
from random import choice
import platform, pygame, time, os
from os import system

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,100'

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Tic-Tac-Toe')

letterX = pygame.image.load(os.path.join('res', 'X.png'))
letterO = pygame.image.load(os.path.join('res', 'O.png'))


HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def evaluate(state):
    """
   Sprawdzenie kazdego ruchu i przypisanie odpowiedniej wartosci, w zaleznosci, kto wedlug algorytmu min max wygral dana sekwencje
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    Sprawdzenie kombinacji wygrywajacych
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
  Jak skonczysz grac to wysietla sie odpowiednia komenda
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
   Tworzy liste wolnych miejsc
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    Funkcja do sprawdzenia czy miejsce jest wolne
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
 Jesli wybrales jakies miejsce, to wywoluje funkcje do sprawdzenia czy to miejsce jest wolne, a jesli jest wolne to ustawia tam dany znak
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
  Fajny algorytm do  wyliczenia najbardziej optymalnego ruchu komputera
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Czyszczenie konsoli
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Wysiwetlanie pola kolko i krzyzyk w terminalu
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def get_mouse(): #przechwytywanie myszki
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < 200:
                        return (pos[0] // 200) + 1
                    if 200 <= pos[1] <= 400:
                        return (pos[0] // 200) + 4
                    if pos[1] > 400:
                        return (pos[0] // 200) + 7


def ai_turn(c_choice, h_choice):
    """

    Ruch komputera, funkcja do wywolania algorytm min max etc
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')

    #DEBUG
    #render(board, c_choice, h_choice)



    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)

    screen.fill((0, 0, 0))
    draw(screen, board, c_choice, h_choice)
    pygame.display.flip()

def human_turn(c_choice, h_choice):
    """
    Funkcja do oblusgi gracza(czlowieka)
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dostepne ruchy
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')

   #DEBUG
   # render(board, c_choice, h_choice)
   #render to wysiwetlanie pola kolka i krzyzyk w  terminalu

    screen.fill((0, 0, 0))
    draw(screen, board, c_choice, h_choice)
    pygame.display.flip()

    while move < 1 or move > 9:
        try:
            # move = int(input('Use numpad (1..9): '))
            move = int(get_mouse())
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def draw(screen, state, c_choice, h_choice): #rysowanie w oknie
    grid_lines = [((0, 200), (600, 200)),
                       ((0, 400), (600, 400)),
                       ((200, 0), (200, 600)),
                       ((400, 0), (400, 600))]

    # grid = [[0 for x in range(3)] for y in range(3)]

    for line in grid_lines:
        pygame.draw.line(screen, (200, 200, 200), line[0], line[1], 2)

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }

    i = 0
    j = 0

    for row in state:
        for cell in row:
            symbol = chars[cell]
            if symbol == 'X':
                screen.blit(letterX, (i * 200, j * 200))
            elif symbol == 'O':
                screen.blit(letterO, (i * 200, j * 200))
            i += 1
        j += 1
        i = 0


