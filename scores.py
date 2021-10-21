''' 
    Scores module is in charge loading scores.json and turning it into a dictionary,
    this way python is able to append new scores from game sessions. It also instructs
    how to draw the scores to a pygame screen. Scores is able to save new scores into
    the json file and will sort it from highest score to lowest.
'''
import json
import datetime
from operator import itemgetter
import pygame


class Scores:
    ''' Scores first loads the json file and makes a class variable dictionary '''
    def __init__(self, score):
        self._date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self._score = score

        in_file = open('scores.json')
        self._scores_data = json.load(in_file)
        self._scores_data['scores'].append({"date":self._date, "score":self._score})
        self._scores_data['scores'].sort(key=itemgetter("score", "date"), reverse=True)
        in_file.close()

        self.text_font = pygame.font.SysFont(None, 15)

    def draw(self, screen):
        ''' Neatly draws scores from dictionary onto pygame screen '''
        (screen_w, screen_h) = screen.get_size()
        text_y = 100
        text_img = self.text_font.render('DATE                   SCORE', True, (0, 0, 0))
        screen.blit(text_img, text_img.get_rect(center=(screen_w/2, text_y)))
        for i in self._scores_data['scores']:
            text_y += 20
            text_img = self.text_font.render(i['date'], True, (0, 0, 0))
            screen.blit(text_img, text_img.get_rect(center=(screen_w/2-50, text_y)))

            text_img = self.text_font.render(str(i['score']), True, (0, 0, 0))
            screen.blit(text_img, text_img.get_rect(center=(screen_w/2+42, text_y)))

    def save_scores(self):
        ''' Only called once GameScene has ended, will load new score into json file'''
        out_file = open("scores.json", "w")
        json.dump(self._scores_data, out_file, indent=4)
        out_file.close()
