import pygame as pg
import os
from random import randint
import random
import time
from settings import *

class Game:
    game_running = True
    clock = None
    screen = None
    background = None
    myfont = None
    words = []
    words_displayed = []
    SPAWN_WORD_EVENT = None
    lives = 5
    user_input = ""

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.background = pg.Surface(self.screen.get_size())
        self.myfont = pg.font.SysFont("freesansbold", 30)
        self.words = self.get_words_list()
        self.set_word_spawn_event()
        self.set_word_spawn_event_timer(700)


    def draw_background(self, color):
        self.background.fill(color)
        self.background = self.background.convert()
        self.screen.blit(self.background, (0,0))

    def draw_text_on_screen(self, text, color, x, y):
        to_render = self.myfont.render(text, False, color)
        self.screen.blit(to_render, ( x, y ))

    def get_words_list(self):
        words = []
        res_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'resources')
        f = open(os.path.join(res_dir, 'words.txt'))
        try:
            for line in f.readlines():
                words.append(line.rstrip())
        finally:
            f.close()
        return words

    def set_word_spawn_event(self):
        self.SPAWN_WORD_EVENT = pg.USEREVENT + 1

    def set_word_spawn_event_timer(self, t):
        pg.time.set_timer(self.SPAWN_WORD_EVENT, t)

    def remove_words_from_screen(self):
        words_displayed_length = len(self.words_displayed)
        self.words_displayed[:] = [ word for word in self.words_displayed if word[2] < HEIGHT ]
        words_displayed_count_diff = words_displayed_length - len(self.words_displayed)
        if words_displayed_count_diff > 0: self.lives -= words_displayed_count_diff 

    def game_over_if_no_lives(self):
        if self.lives == 0: self.game_running = False 

    def get_key_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.game_running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.game_running = False
                if pg.key.name(e.key).lower().isalpha() and len(pg.key.name(e.key)) == 1:
                    self.user_input += pg.key.name(e.key).lower()
                if pg.key.name(e.key) == 'backspace':
                    self.user_input = self.user_input[:-1]
                if pg.key.name(e.key).lower() == 'return':
                    print self.user_input
                    self.words_displayed[:] = [ word for word in self.words_displayed if self.user_input != word[0] ]
                    self.user_input = ""
            if e.type == self.SPAWN_WORD_EVENT:
                word_x_y = [random.choice(self.words), randint(0, WIDTH - 20), 0]
                self.words_displayed.append(word_x_y)

    def update(self):
        for word in self.words_displayed:
            word[2] += WORD_SPEED
            self.draw_text_on_screen(word[0], (0,0,0), word[1], word[2])
        self.draw_text_on_screen(self.user_input, (255,0,0), WIDTH / 2, HEIGHT / 2)

    def draw(self):
        self.clock.tick(FPS)
        pg.display.update() 


    def game_loop(self):
        while self.game_running:
            self.get_key_events()
            self.draw_background((255, 255, 255))
            self.draw_text_on_screen(str(self.lives), (0,0,0), 10, 10)
            self.remove_words_from_screen()
            self.game_over_if_no_lives()
            self.update()
            self.draw()

game = Game()
game.game_loop()
