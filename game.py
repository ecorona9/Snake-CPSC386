'''
    Game module controls and initalizes pygame, loads, manages and draws scenes,
    monitors events from keyboard and calls scene updates.
'''
import sys
import pygame
from scene import TitleScene
def run_game():
    ''' run_game contains the main loop calling for scene updates '''
    if not pygame.font:
        print("WARNING FONTS DISABLED")
        sys.exit()
    if not pygame.mixer:
        print("WARNING SOUND DISABLED")
        sys.exit()

    width = 800
    height = 800
    fps = 60

    pygame.init()
    pygame.display.set_caption('That Snake Game by Eric Corona')
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    current_scene = TitleScene()
    while current_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # event handling
        filtered_events = []
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_scene.end_scene()
                sys.exit()
            elif event.type == pygame.QUIT:
                current_scene.end_scene()
                sys.exit()
            else:
                filtered_events.append(event)

        current_scene.handle_input(filtered_events)
        current_scene.update()
        current_scene.draw(screen)

        current_scene = current_scene.next

        pygame.display.flip() #updates the full display surface of the screen
        clock.tick(fps)
