import pygame
import os
from random import randint
import random
import time

mainloop = True
pygame.init()

Clock = pygame.time.Clock()


WIDTH = 640
HEIGHT = 480
WORD_SPEED = 1
FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT)) # Set screen size of pygame window
background = pygame.Surface(screen.get_size())  # Create empty pygame surface
background.fill((255,255,255))# Fill the background white color (red,green,blue)
background = background.convert()  # Convert Surface to make blitting faster

myfont = pygame.font.SysFont("freesansbold", 30)
screen.blit(background, (0, 0))

words = []
words_to_display = []
res_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'resources')
f = open(os.path.join(res_dir, 'words.txt'))
try:
    for line in f.readlines():
        words.append(line.rstrip())
finally:
    f.close()

SPAWN_WORD_EVENT, t, trail = pygame.USEREVENT+1, 700, []
pygame.time.set_timer(SPAWN_WORD_EVENT, t)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

user_input = ""
lives = 5

while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if pygame.key.name(event.key) in letters:
                user_input += pygame.key.name(event.key).lower()
            if pygame.key.name(event.key) == 'backspace':
                user_input = user_input[:-1]
            if pygame.key.name(event.key).lower() == 'return':
                words_to_display[:] = [ word for word in words_to_display if user_input != word[0] ]
                user_input = ""
        if event.type == SPAWN_WORD_EVENT:
            word_x_y = [random.choice(words), randint(0, WIDTH - 20), 0]
            words_to_display.append(word_x_y)

    background.fill((255,255,255))# Fill the background white color (red,green,blue)
    screen.blit(background, (0, 0))

    lives_text = myfont.render(str(lives), False, (0,0,0))
    screen.blit(lives_text, ( 10, 10 ))

    words_to_display_len = len(words_to_display)
    words_to_display[:] = [ word for word in words_to_display if word[2] < HEIGHT ]
    words_list_len_difference = words_to_display_len - len(words_to_display)
    if words_list_len_difference > 0: lives -= words_list_len_difference

    if lives == 0: mainloop = False
 
    for word in words_to_display:
        word[2] += WORD_SPEED
        textsurface = myfont.render(word[0], False, (0,0,0))
        screen.blit(textsurface, (word[1] , word[2]))

    user_input_text = myfont.render(user_input, False, (255,0,0))
    screen.blit(user_input_text, ( WIDTH / 2, HEIGHT - 100 ))

    Clock.tick(FPS)
    pygame.display.update() 

