'''
    Scene module contains base class scene definition, includes basic functions 
    that need to be overridden for more specific scenes required. This scene 
    module includes all scenes utilized for the snake game
'''
import math
import pygame

from player import Player, Food
from scores import Scores
class Scene:
    '''Base class Scene'''
    def __init__(self):
        self.next = self
    def handle_input(self, events):
        ''' handles pygame events, which includes keyboard, mouse or joysticks'''
        print("OVERRIDE handle_input function")
    def update(self):
        ''' Scenes can have different types of updates based on the time passed '''
        print("OVERRIDE handle_input function")
    def draw(self, screen):
        ''' Scenes will be able to draw to the pygame screen via this function '''
        print("OVERRIDE handle_input function")
    def change_scene(self, next_scene):
        ''' Easily transition into another scene with this function '''
        self.next = next_scene
    def end_scene(self):
        ''' Destroy this scene '''
        self.change_scene(None)

class TitleScene(Scene):
    ''' First scene presented when program is launched '''
    def __init__(self):
        Scene.__init__(self)
        self.title = 'That Snake Game'
        self._title_size = 72
        self._d_x = 0.12
        self._d_r = 0.01
        self._d_g = 0.02
        self._d_b = 0.03
        self._x = 0
        self._r = 0
        self._g = 0
        self._b = 0
        self._title_color = (0, 0, 0)
        self.title_font = pygame.font.SysFont(None, self._title_size)
        self.title_img = self.title_font.render('TitleScene', True, (self._r, self._g, self._b))
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.change_scene(RulesScene())
    def update(self):
        self._x += self._d_x % (2 * math.pi)
        self._title_size = 72 + int(4*math.cos(self._x))
        self._r += self._d_r % (255)
        self._g += self._d_g % (255)
        self._b += self._d_b % (255)

        title_r = int(255/2*(math.cos(self._r) + 1))
        title_g = int(255/2*(math.cos(self._g) + 1))
        title_b = int(255/2*(math.cos(self._b) + 1))
        self._title_color = (title_r, title_g, title_b)

        self.title_font = pygame.font.SysFont(None, self._title_size)
        self.title_img = self.title_font.render(self.title, True, self._title_color)
    def draw(self, screen):
        # RED SCREEN
        screen.fill((100, 204, 178))

        (screen_w, screen_h) = screen.get_size()
        screen.blit(self.title_img, self.title_img.get_rect(center=(screen_w/2, screen_h/2)))

        text_font = pygame.font.SysFont(None, 24)
        text_img = text_font.render('Press Enter To Continue...', True, (0, 0, 0))
        screen.blit(text_img, text_img.get_rect(center=(screen_w/2, screen_h-50)))

class GameScene(Scene):
    ''' 
        Includes player, food and game time. These objects constantly interact with each other
        as this is how the snake game works, once the player collides with food the score increases,
        also the score increases when the timer reaches the three second threshold.
    '''
    def __init__(self):
        Scene.__init__(self)
        self._player = Player()
        self._food = Food()
        self._game_time = pygame.time.get_ticks()
    def handle_input(self, events):
        for event in events:
            self._player.handle_input(event)
    def update(self):
        self._player.update()
        if self._player.collides(self._food):
            self._player.increment_score()
            self._food.update()
        if not self._player.alive():
            self.change_scene(GameOverScene(self._player.get_score()))

    def draw(self, screen):
        # WHITE SCREEN
        screen.fill((100, 204, 178))
        font = pygame.font.SysFont(None, 24)
        time_elapsed = (pygame.time.get_ticks() - self._game_time) / 1000

        self._player.draw(screen)
        self._food.draw(screen)
        img_str = 'Score:  {}    Time:  {}'.format(self._player.get_score(), int(time_elapsed))
        img = font.render(img_str, True, (0, 0, 0))
        screen.blit(img, (50, 50))

class GameOverScene(Scene):
    ''' 
        This scene is displayed once the player has died and will create a scores object in order
        to print scores saved to the scores.json file.
    '''
    def __init__(self, ending_score=0):
        Scene.__init__(self)
        self.title_font = pygame.font.SysFont(None, 72)
        self.title_img = self.title_font.render('GAME OVER', True, (0, 0, 0))

        self.text_font = pygame.font.SysFont(None, 24)
        self.text_img = self.text_font.render('Press Enter to Try Again...', True, (0, 0, 0))

        self._scores = Scores(ending_score)

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._scores.save_scores()
                self.change_scene(GameScene())
    def update(self):
        pass
    def draw(self, screen):
        # WHITE SCREEN
        screen.fill((100, 204, 178))
        (screen_w, screen_h) = screen.get_size()
        screen.blit(self.text_img, self.text_img.get_rect(center=(screen_w/2, screen_h-50)))
        screen.blit(self.title_img, self.title_img.get_rect(center=(screen_w/2, 50)))
        self._scores.draw(screen)
    def end_scene(self):
        self._scores.save_scores()
        self.change_scene(None)

class RulesScene(Scene):
    ''' Simple scene that loads after the title scene which displays the game rules with an image '''
    def __init__(self):
        Scene.__init__(self)
        self.title_font = pygame.font.SysFont(None, 72)
        self.title_img = self.title_font.render('RULES', True, (0, 0, 0))

        self._rules = ''
        self.rules_font = pygame.font.SysFont(None, 24)
        self.rules_img = self.rules_font.render('Press Enter to\n Try Again...', True, (0, 0, 0))

        self._image = pygame.image.load('images/Rules.png')
    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.change_scene(GameScene())
    def update(self):
        pass
    def draw(self, screen):
        # WHITE SCREEN
        screen.fill((100, 204, 178))
        (screen_w, screen_h) = screen.get_size()
        screen.blit(self.title_img, self.title_img.get_rect(center=(screen_w/2, 50)))
        screen.blit(self.rules_img, self.rules_img.get_rect(center=(screen_w/2, screen_h-50)))
        screen.blit(self._image, (0, 0))
