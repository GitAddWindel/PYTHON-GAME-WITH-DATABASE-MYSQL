import pygame
import sys

pygame.init()

score = 0
width = 1550
height = 800
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stack Game")
clock = pygame.time.Clock()

background = (23, 32, 42)
white = (236, 240, 241)

color = [(120, 40, 31), (148, 49, 38), (176, 58, 46), (203, 67, 53),
         (231, 76, 60), (236, 112, 99), (241, 148, 138),
         (245, 183, 177), (250, 219, 216), (253, 237, 236),
         (254, 249, 231), (252, 243, 207), (249, 231, 159),
         (247, 220, 111), (244, 208, 63), (241, 196, 15),
         (212, 172, 13), (183, 149, 11), (154, 125, 10), (125, 102, 8),
         (126, 81, 9), (156, 100, 12), (185, 119, 14), (202, 111, 30),
         (214, 137, 16), (243, 156, 18), (245, 176, 65),
         (248, 196, 113), (250, 215, 160), (253, 235, 208), (254, 245, 231),
         (232, 246, 243), (162, 217, 206), (162, 217, 206),
         (115, 198, 182), (69, 179, 157), (22, 160, 133),
         (19, 141, 117), (17, 122, 101), (14, 102, 85),
         (11, 83, 69),
         (21, 67, 96), (26, 82, 118), (31, 97, 141),
         (36, 113, 163), (41, 128, 185), (84, 153, 199),
         (127, 179, 213), (169, 204, 227), (212, 230, 241),
         (234, 242, 248),
         (251, 238, 230), (246, 221, 204), (237, 187, 153),
         (229, 152, 102), (220, 118, 51), (211, 84, 0),
         (186, 74, 0), (160, 64, 0), (135, 54, 0),
         (110, 44, 0)
         ]

colorIndex = 0

brickH = 700
brickW = 1000

score = 0
speed = 3

# Define the Brick class
class Brick:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.w = brickW
        self.h = brickH
        self.color = color
        self.speed = speed

    def draw(self):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))

    def move(self):
        self.x += self.speed
        if self.x > width or self.x + self.w < 0:
            self.speed *= -1

# Define the Stack class
class Stack:
    def __init__(self):
        global colorIndex
        self.stack = []
        self.initSize = 25
        for i in range(self.initSize):
            newBrick = Brick(width / 2 - brickW / 2, height - 1 - (i + 1) * brickH, color[colorIndex], 0)
            colorIndex += 1
            self.stack.append(newBrick)

    def show(self):
        for i in range(self.initSize):
            self.stack[i].draw()

    def move(self):
        for i in range(self.initSize):
            self.stack[i].move()

    def add_new_brick(self):
        global colorIndex, speed

        if colorIndex >= len(color):
            colorIndex = 0

        y = self.peek().y
        if score > 50:
            speed += 0
        elif score % 5 == 0:
            speed += 1

        newBrick = Brick(width, y - brickH, color[colorIndex], speed)
        colorIndex += 1
        self.initSize += 1
        self.stack.append(newBrick)

    def peek(self):
        return self.stack[self.initSize - 1]

    def push_to_stack(self):
        global brickW, score
        b = self.stack[self.initSize - 2]
        b2 = self.stack[self.initSize - 1]
        if b2.x <= b.x and not (b2.x + b2.w < b.x):
            self.stack[self.initSize - 1].w = self.stack[self.initSize - 1].x = self.stack[self.initSize - 1].w - b.x
            self.stack[self.initSize - 1].x = b.x
            if self.stack[self.initSize - 1].w > b.w:
                self.stack[self.initSize - 1].w = b.w
            self.stack[self.initSize - 1].speed = 0
            score += 1
        elif b.x <= b2.x <= b.x + b.w:
            self.stack[self.initSize - 1].w = b.x + b.w - b2.x
            self.stack[self.initSize - 1].speed = 0
            score += 1
        else:
            game_over()
        for i in range(self.initSize):
            self.stack[i].y += brickH

        brickW = self.stack[self.initSize - 1].w

# Function to get the username from the player
def get_username():
    username = ""
    exit_game = False
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(650, 350, 200, 35)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ""
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_RETURN:
                    # Assign the value of the input text to the username variable
                    username = text
                    return username, exit_game
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False

                color = color_active if active else color_inactive

        display.fill(background)

        game_over_font = pygame.font.Font(None, 100)
        game_over_text = game_over_font.render('Game Over!', True, (255, 255, 255))
        display.blit(game_over_text, (545, 150))

        # Render "Enter your username" text
        intro_font = pygame.font.Font(None, 36)
        intro_text = intro_font.render("Enter your username:", True, (255, 255, 255))
        display.blit(intro_text, (375, 353))

        score_font = pygame.font.Font(None, 66)
        score_text = score_font.render("SCORE: " + str(score), True, white)
        display.blit(score_text, (645, 453))  # Adjusted position for the second input box

        pygame.draw.rect(display, color, input_box, 2)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() - 10)
        input_box.w = width
        display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        clock.tick(30)


# Function to handle game over state
def game_over():
    loop = True

    font = pygame.font.SysFont('Agency Fb', 100)
    text = font.render('Game Over!', True, white)

    text_rect = text.get_rect()
    text_rect.center = (width / 2, height / 2 - 170)

    retry_font = pygame.font.Font(None, 36)
    retry_text = retry_font.render('Press R to retry', True, white)
    retry_rect = retry_text.get_rect()
    retry_rect.center = (width / 2, height / 2)

    quit_font = pygame.font.Font(None, 36)
    quit_text = quit_font.render('Press Q to quit', True, white)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (width / 2, height / 2 + 50)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    username, exit_game = get_username()
                    print("Username:", username)
                    if exit_game:
                        close()
                    else:
                        game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                username, exit_game = get_username()
                print("Username:", username)
                if exit_game:
                    close()
                else:
                    game_loop()

        display.blit(text, text_rect)
        display.blit(retry_text, retry_rect)
        display.blit(quit_text, quit_rect)
        pygame.display.update()
        clock.tick()

# Function to display the player's score
def show_score():
    font = pygame.font.SysFont('Forte', 45)
    text = font.render('Score: ' + str(score), True, white)
    display.blit(text, (10, 10))

# Function to close the game
def close():
    pygame.quit()
    sys.exit()

# Main game loop
def game_loop():
    global brickW, brickH, score, colorIndex, speed
    loop = True

    brickH = 10
    brickW = 100
    colorIndex = 0
    speed = 3

    score = 0

    stack = Stack()
    stack.add_new_brick()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                stack.push_to_stack()
                stack.add_new_brick()

        display.fill(background)

        stack.move()
        stack.show()

        show_score()

        pygame.display.update()
        clock.tick(60)

# Start the game loop
game_loop()
