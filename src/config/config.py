import os
import pygame

from sound import Sound
from theme import Theme


class Config:

    def __init__(self):
        self.add_themes()

        self.themes = []
        self.index = 0
        self.theme = self.themes[self.index] #change to self.current_theme

        self.move_sound 

    def change_theme(self):
        pass

    def add_theme(self):
        pass