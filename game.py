import os, pygame, grid




pygame.init()


"""
Implementacja algorytmu min max dla gry kolko i krzyzyk
"""



def main():
    """
    Glowna funkcja wywolujaca pozostlae funkcje
    """
    grid.clean()
    h_choice = 'X'  # X or O
    c_choice = 'O'  # X or O
    first = 'Y'  # gracz jest pierwszy

    # glowna petla programu
    while len(grid.empty_cells(grid.board)) > 0 and not grid.game_over(grid.board):
        if first == 'N':
            grid.ai_turn(c_choice, h_choice)
            first = ''

        grid.human_turn(c_choice, h_choice)

        grid.ai_turn(c_choice, h_choice)

    # wiadomosc na koniec gry
    if grid.wins(grid.board, grid.HUMAN):
        grid.clean()
        print(f'Human turn [{h_choice}]')
       # grid.render(grid.board, c_choice, h_choice)
        print('YOU WIN!')
    elif grid.wins(grid.board, grid.COMP):
        grid.clean()
        print(f'Computer turn [{c_choice}]')
        #grid.render(grid.board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        grid.clean()
        #grid.render(grid.board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
