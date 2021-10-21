''' 
    Entity module defines a base class which will easily define player, player body and food.
'''
import random
import pygame

class Entity:
    ''' Base class with simple attributes which any entity could have within the game '''
    def __init__(self, x=0, y=0, w=0, h=0):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
    def get_x(self):
        ''' Returns x coordinate '''
        return self._x
    def get_y(self):
        ''' Return y coordinate '''
        return self._y
    def __str__(self):
        ''' Function docstring '''
        print("OVERRIDE str function")
    def handle_input(self, event):
        ''' Entities can also handle inputs similar to scenes '''
        print("OVERRIDE handle_input function")
    def update(self):
        ''' Entities will have their own update calls '''
        print("OVERRIDE update function")
    def draw(self, screen):
        ''' Entities can also draw to the screen like a scene '''
        print("OVERRIDE draw function")
    def collides(self, entity):
        ''' All entities can have a collision function '''
        print("OVERRIDE collides function")


class Player(Entity):
    ''' 
        Player class inherits from Entity as it posses more specific attributes, such as
        score, color, speed, etc.
    '''
    def __init__(self, x=400, y=400):
        Entity.__init__(self, x, y, 50, 50)
        self._color = (191, 81, 73)
        self._score = 0
        self._d_x = 0
        self._d_y = 0
        self._speed = 50
        self._timer_start = pygame.time.get_ticks()
        self._timer_score = pygame.time.get_ticks()
        self._alive = True
        self._move_time = 0.2
        self._body = []
        self._prev_key = None
    def __str__(self):
        pass
    def move_faster(self):
        ''' Lowers the movement time threshold by one percent '''
        self._move_time *= 0.99
    def alive(self):
        ''' Returns wether the player is alive or not '''
        return self._alive
    def increment_score(self):
        ''' Increases the score by one, increases snake size and increases snake movement speed '''
        self._score += 1
        self.increment_body()
        self.move_faster()
    def increment_body(self):
        ''' 
            Depending on the direction of the head or last body part of the snake, the new body 
            part will have to spawn in from the body at certain coordinates
        '''
        if len(self._body) > 0:
            last_body = self._body[len(self._body) - 1]
            data = last_body.get_player_data()
            if self._d_x > 0: #GOING EAST
                self._body.append(PlayerBody(data[0] - 50, data[1], data[2]))
            if self._d_x < 0: #GOING WEST
                self._body.append(PlayerBody(data[0] + 50, data[1], data[2]))
            if self._d_y > 0: #GOING SOUTH
                self._body.append(PlayerBody(data[0], data[1] - 50, data[2]))
            if self._d_y < 0: #GOING NORTH
                self._body.append(PlayerBody(data[0], data[1] + 50, data[2]))
        else:
            if self._d_x > 0: #GOING EAST
                self._body.append(PlayerBody(self._x - 50, self._y, 'E'))
            if self._d_x < 0: #GOING WEST
                self._body.append(PlayerBody(self._x + 50, self._y, 'W'))
            if self._d_y > 0: #GOING SOUTH
                self._body.append(PlayerBody(self._x, self._y - 50, 'S'))
            if self._d_y < 0: #GOING NORTH
                self._body.append(PlayerBody(self._x, self._y + 50, 'N'))
    def get_direction(self):
        ''' Determines player current direction '''
        if self._d_x > 0: #GOING EAST
            return 'E'
        elif self._d_x < 0: #GOING WEST
            return 'W'
        elif self._d_y > 0: #GOING SOUTH
            return 'S'
        else: #GOING NORTH
            return 'N'
    def get_score(self):
        ''' Returns players current score '''
        return self._score
    def handle_input(self, event):
        ''' Establishes how the user can interact with the player within the game scene '''
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w and self._prev_key is not pygame.K_s:
            self._d_y = -self._speed
            self._d_x = 0
            self._prev_key = event.key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a and self._prev_key is not pygame.K_d:
            self._d_x = -self._speed
            self._d_y = 0
            self._prev_key = event.key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and self._prev_key is not pygame.K_w:
            self._d_y = self._speed
            self._d_x = 0
            self._prev_key = event.key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d and self._prev_key is not pygame.K_a:
            self._d_x = self._speed
            self._d_y = 0
            self._prev_key = event.key
    def update(self):
        movement_elapsed = (pygame.time.get_ticks() - self._timer_start) / 1000
        score_elapsed = (pygame.time.get_ticks() - self._timer_score) / 1000
        for body_part in self._body:
            if self.collides(body_part):
                self._alive = False
        if self._x < 0 or self._x > 750 or self._y < 0 or self._y > 750:
            self._alive = False
        if score_elapsed > 3:
            self._score += 1
            self._timer_score = pygame.time.get_ticks()
            self.move_faster()
        if movement_elapsed > self._move_time:
            i = len(self._body) - 1
            while i > 0:
                new_data = self._body[i-1].get_player_data()
                self._body[i].update(new_data)
                i -= 1
            if len(self._body) > 0:
                self._body[0].update((self._x, self._y, self.get_direction()))

            self._x += self._d_x
            self._y += self._d_y

            self._timer_start = pygame.time.get_ticks()

    def draw(self, screen):
        ''' How the player is drawn onto the pygame screen '''
        pygame.draw.rect(screen, self._color, pygame.Rect(self._x, self._y, self._w, self._h))
        for player_body in self._body:
            player_body.draw(screen)
    def collides(self, entity):
        ''' 
            Player class must override the collision function as each entity can have its specific 
            collision interests
        '''
        return self._x == entity.get_x() and self._y == entity.get_y()


class PlayerBody(Entity):
    ''' 
        Player body is similar to player however it simply represents the additional body parts of the 
        snake
    '''
    def __init__(self, x=0, y=0, d='N'):
        Entity.__init__(self, x, y, 50, 50)
        self._color = (191, 81, 73)
        self._direction = d
    def __str__(self):
        pass
    def handle_input(self, event):
        pass
    def get_player_data(self):
        ''' Return player coordinates and direction as a tuple '''
        return (self._x, self._y, self._direction)
    def update(self, data):
        self._x = data[0]
        self._y = data[1]
        self._direction = data[2]
    def draw(self, screen):
        pygame.draw.rect(screen, self._color, pygame.Rect(self._x, self._y, self._w, self._h))
    def collides(self, entity):
        return self._x == entity.get_x() and self._y == entity.get_y()



class Food(Entity):
    ''' 
        Food class is how the player grows its body, with random pieces of food spawning in the
        game scene
    ''' 
    def __init__(self):
        width = 50
        random_x = int(random.randint(0, 750) / width) * width
        random_y = int(random.randint(0, 750) / width) * width
        Entity.__init__(self, random_x, random_y, width, width)
        self._color = (230, 179, 41)
    def __str__(self):
        pass
    def handle_input(self, event):
        pass
    def update(self):
        self._x = int(random.randint(0, 750) / self._w) * self._w
        self._y = int(random.randint(0, 750) / self._w) * self._w
    def draw(self, screen):
        pygame.draw.rect(screen, self._color, pygame.Rect(self._x, self._y, self._w, self._h))
