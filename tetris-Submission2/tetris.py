from tetrisscanner import TetrisLexer
from tetrisparser import TetrisParser
import pygame
import random

blockindices = []

ROWS = 10
COLUMNS = 30
ORIGIN = 0
MUSIC = 1
SPEED = 10
NEXTQ = 1

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

RIGHT = pygame.K_RIGHT
LEFT = pygame.K_LEFT
ROTATELEFT = pygame.K_UP
ROTATERIGHT = pygame.K_RSHIFT
SOFTDROP = pygame.K_DOWN 
HARDDROP = pygame.K_SPACE
PAUSE = pygame.K_p

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        # print(x)
        self.y = y
        # self.type = random.randint(0, len(self.figures) - 1)
        self.type = random.choice(blockindices)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width,speed):
        self.height = height
        self.width = width
        self.level = speed
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self,origin):
        self.figure = Figure(origin, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self,origin):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze(origin)

    def go_down(self,origin):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze(origin)

    def freeze(self,origin):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure(origin)
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

def main():
    lexer = TetrisLexer()
    parser = TetrisParser()
    program = open('program.tet','r')
    text = program.readlines()
    # print(len(text))
    for string in text:
        tokens = lexer.tokenize(string) # Creates a generator of tokens
        # for tok in tokens:
        #     print(tok)
            # print('type=%r, value=%r' % (tok.type, tok.value))
        # print(tokens)
        parser.parse(tokens)
    # print(parser.names)
    # print(parser.blocktable)
    # print(parser.colortable)
    # return

    if "ROWS" in parser.names:
        ROWS=parser.names["ROWS"]
        if(ROWS<4):
            print("Error: ROWS cannot be less than 4.")
            return
        print("ROWS updated")
    else:
        print("default value assigned for ROWS")

    if "COLUMNS" in parser.names:
        COLUMNS=parser.names["COLUMNS"]
        if(COLUMNS<4):
            print("Error: COLUMNS cannot be less than 4.")
            return
        print("COLUMNS updated")
    else:
        print("default value assigned for COLUMNS")

    if "ORIGIN" in parser.names:
        ORIGIN=parser.names["ORIGIN"]
        if(ORIGIN<0 or ORIGIN+3>=COLUMNS):
            print("Error: ORIGIN cannot be less than 0 or greater than COLUMNS-4.")
            return
        print("ORIGIN updated")
    else:
        print("default value assigned for ORIGIN")

    # print(ORIGIN)

    if "MUSIC" in parser.names:
        MUSIC=parser.names["MUSIC"]
        if(MUSIC<0 or MUSIC>2):
            print("Error: MUSIC cannot be less than 0 or greater than 2.")
            return
        print("MUSIC updated")
    else:
        print("default value assigned for MUSIC")

    if "SPEED" in parser.names:
        SPEED=parser.names["SPEED"]
        if(SPEED<0 or SPEED>10):
            print("Error: SPEED cannot be less than 0 or greater than 10.")
            return
        print("SPEED updated")
        # print(SPEED)
    else:
        print("default value assigned for SPEED")
    
    for i in range(7):
        if(parser.blocktable[i]==True):
            blockindices.append(i)
    if(len(blockindices)==0):
        print("Error: Atleast one block type has to be allowed")
        return

    if "RIGHT" in parser.names:
        RIGHT=parser.names["RIGHT"]
        print("RIGHT updated")
    else:
        print("default value assigned for RIGHT")
    
    if "LEFT" in parser.names:
        LEFT=parser.names["LEFT"]
        print("LEFT updated")
    else:
        print("default value assigned for LEFT")
    
    if "ROTATELEFT" in parser.names:
        ROTATELEFT=parser.names["ROTATELEFT"]
        print("ROTATELEFT updated")
    else:
        print("default value assigned for ROTATELEFT")
    
    if "ROTATERIGHT" in parser.names:
        ROTATERIGHT=parser.names["ROTATERIGHT"]
        print("ROTATERIGHT updated")
    else:
        print("default value assigned for ROTATERIGHT")

    if "SOFTDROP" in parser.names:
        SOFTDROP=parser.names["SOFTDROP"]
        print("SOFTDROP updated")
    else:
        print("default value assigned for SOFTDROP")
    
    if "HARDDROP" in parser.names:
        HARDDROP=parser.names["HARDDROP"]
        print("HARDDROP updated")
    else:
        print("default value assigned for HARDDROP")
    
    if "PAUSE" in parser.names:
        PAUSE=parser.names["PAUSE"]
        print("PAUSE updated")
    else:
        print("default value assigned for PAUSE")

    # Initialize the game engine
    pygame.init()

    #playing music
    if MUSIC == 1:
        pygame.mixer.music.load("TetrisOriginal.mp3")
        pygame.mixer.music.play(-1)
    if MUSIC == 2:
        pygame.mixer.music.load("RickRoll.mp3")
        pygame.mixer.music.play(-1)

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    
    game = Tetris(ROWS, COLUMNS, SPEED)

    # print(game.level)

    size = (max(2*game.x+COLUMNS+1+COLUMNS*game.zoom,500), max(2*game.y +ROWS+1+ ROWS*game.zoom,500))
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    fps = 25
    
    counter = 0

    pressing_down = False

    

    while not done:
        if game.figure is None:
            game.new_figure(ORIGIN)
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down(ORIGIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == ROTATELEFT:
                    game.rotate()
                if event.key == SOFTDROP:
                    pressing_down = True
                if event.key == LEFT:
                    game.go_side(-1)
                if event.key == RIGHT:
                    game.go_side(1)
                if event.key == HARDDROP:
                    game.go_space(ORIGIN)
                if event.key == pygame.K_ESCAPE:
                    game.__init__(ROWS, COLUMNS, SPEED)

            if event.type == pygame.KEYUP:
                if event.key == SOFTDROP:
                    pressing_down = False

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                        [game.x + game.zoom * (j + game.figure.x) + 1,
                                        game.y + game.zoom * (i + game.figure.y) + 1,
                                        game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [0, 0])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()