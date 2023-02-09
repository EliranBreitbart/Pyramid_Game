import math
import pygame

# initialize pygame and create a window
pygame.init()
size2 = 600
screen = pygame.display.set_mode((size2, size2))
pygame.display.set_caption("Tic-Tac-Pyramid - By Eliran Breitbart")

#gloal variables
global size         # board size
global curr_player  # current player 0 or 1
global scores       # [p0 score, p1 score]
global gameTable    # 2d array
global rects        # the rects of the circles on the boards
global lines        # the lines for completed row/diagonal
global radius       # the radius of the circles (in case its needed to be changed later)


# prints the board in the terminal - for use in debugging if needed
def print_game_table():
    width = len(', '.join(map(str, gameTable[size - 1])))
    for i in range(size):
        print(', '.join(map(str, gameTable[i][0:i + 1])).center(width, ' '))


# disable the right part of the board
def disable_blocks():
    for row in range(size):
        for col in range(row + 1, size):
            gameTable[row][col] = -1


# initialize / reset the board
def initialize_data():
    global size, curr_player, scores, gameTable, rects, lines
    curr_player = 0
    scores = [0, 0]
    gameTable = [[0 for i in range(size)] for j in range(size)]
    disable_blocks()
    rects = []
    lines = []
    for row in range(size):
        curr = []
        for col in range(row + 1):
            curr.append("")
        rects.append(curr)


# check if we have completed a horizontal line, return points, add line to draw over
def completed_horizontal(row):
    for row_col in gameTable[row]:
        if row_col == 0:
            return 0
    for col in range(row + 1):
        gameTable[row][col] = -1
    lines.append([(rects[row][0].x - radius, rects[row][0].y + radius),
                  (rects[row][row].x + 3 * radius, rects[row][row].y + radius)])
    return row + 1


# check if we have completed a diagonal right-to-left, return points, add line to draw over
def completed_right_left(col):
    for row in range(size):
        if gameTable[row][col] == 0:
            return 0
    for row in range(size):
        gameTable[row][col] = -1
    lines.append([(rects[col][col].x + radius * (0.5 + math.sqrt(2)), rects[col][0].y + radius * (1 - math.sqrt(2))), (
    rects[size - 1][col].x + radius * (-1.25 + math.sqrt(2)), rects[size - 1][col].y + radius * (1 + math.sqrt(2)))])
    return size - col  # size = length + 1


# check if we have completed diagonal left-to-right, return points, add line to draw over
def completed_left_right(row, col):
    points = 0
    n_row = row - col
    n_col = 0
    for i in range(size - row + col):
        if gameTable[n_row][n_col] == 0:
            return 0
        n_row += 1
        n_col += 1
    n_row = row - col
    n_col = 0
    for i in range(size - row + col):
        gameTable[n_row][n_col] = -1
        n_row += 1
        n_col += 1
        points += 1
    lines.append(
        [(rects[row - col][0].x + radius * (1.5 - math.sqrt(2)), rects[row - col][0].y + radius * (1 - math.sqrt(2))), (
        rects[size - 1][size - row + col - 1].x + radius * (0.5 + math.sqrt(2)),
        rects[size - 1][size - row + col - 1].y + radius * (1 + math.sqrt(2)))])
    return points


# returns all the points earned by filling circle (row,col)
def check_for_completed_lines(row, col):
    return completed_horizontal(row) + completed_right_left(col) + completed_left_right(row, col)


# checks if the game has ended by calculating total points.
def check_game_ended():
    total_aqc_points = 3 * ((size * (size + 1)) // 2)
    if scores[0] + scores[1] == total_aqc_points:
        return True
    return False


# updates the board when an available circle is chosen
def choose_point(row, col):
    global curr_player
    if gameTable[row][col] == 0:
        gameTable[row][col] = 1
        scores[curr_player] += check_for_completed_lines(row, col)
        curr_player = abs(curr_player - 1)
        print_game_table()
    else:
        print("player {}, you cannot fill this spot, try again".format(curr_player))


# draws all the lines
def draw_lines(lines):
    for coord in lines:
        pygame.draw.line(screen, (255, 255, 255), coord[0], coord[1], 3)


# main game loop
def start_game():
    global rects
    global size
    global lines
    global radius
    clock = pygame.time.Clock()
    lines = []
    size = 10
    pygame.font.init()
    initialize_data()
    font = pygame.font.SysFont(None, 30)
    font2 = pygame.font.SysFont("comicsansms", 20)
    font3 = pygame.font.SysFont("comicsansms", 15)
    text_surface = font.render(
        "player1 score: {0}, player2 score: {1}, Current Player: {2}".format(scores[0], scores[1], curr_player + 1),
        False, (255, 255, 255))
    texts = list(map(lambda x: font2.render(x, False, (255, 255, 255)),
                     ["r : restart", "- : smaller board", "+ : bigger board"]))
    # game loop
    running = True
    radius = 25
    start = (size2 / 2, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    initialize_data()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    if size + 1 <= 10:
                        size += 1
                        initialize_data()
                if event.key == pygame.K_MINUS:
                    if size - 1 >= 3:
                        size -= 1
                        initialize_data()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for row in range(len(rects)):
                    for col in range(len(rects[row])):
                        rect = rects[row][col]
                        if rect.collidepoint(event.pos):
                            choose_point(row, col)
        # clear the screen
        screen.fill((0, 0, 0))
        # draw the game board
        for row in range(size):
            for col in range(row + 1):
                rects[row][col] = pygame.draw.circle(screen,
                                                     (255, 0, 0) if gameTable[row][col] != 0 else (255, 255, 255),
                                                     (start[0] + col * 55 - row * 27.5, start[1] + row * 47), 25)
                if gameTable[row][col] == 0 and rects[row][col].collidepoint(pygame.mouse.get_pos()):
                    rects[row][col] = pygame.draw.circle(screen, (0, 0, 255),
                                                         (start[0] + col * 55 - row * 27.5, start[1] + row * 47), 25)
        text_surface = font.render(
            "player1 score: {0}, player2 score: {1}, Current Player: {2}".format(scores[0], scores[1], curr_player + 1),
            False, (255, 255, 255))
        screen.blit(text_surface, (size2 / 2 - font.size(
            "player1 score: {0}, player2 score: {1}, Current Player: {2}".format(scores[0], scores[1],
                                                                                 curr_player + 1))[0] / 2,
                                   rects[size - 1][0].y + 70))
        draw_lines(lines)
        for idx, text in enumerate(texts):
            screen.blit(text, (10, idx * 22))
        if check_game_ended():
            text_surface = font.render("Game Ended, player {} wins".format(1 if scores[0] > scores[1] else 2), False,
                                       (255, 255, 255))
            screen.blit(text_surface, (size2 / 2 - text_surface.get_size()[0] / 2, rects[size - 1][0].y + 100))
        pygame.display.update()
        clock.tick(30)


start_game()
