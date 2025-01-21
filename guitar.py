import os
import pygame


pygame.mixer.init()

class Guitar():
    limit = 100
    guitar_num = 2

    def __init__(self, path):
        self.turn = 0
        self.files = []
        self.sounds = []
        self.channels = []

        self.folder_path = path
        self.find_all_files()
        self.load_wav()

        pygame.mixer.set_num_channels(self.limit * self.guitar_num)

        for i in range(self.limit):
            self.channels.append(pygame.mixer.Channel(i))

    def find_all_files(self):
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                self.files.append(os.path.join(root, file))

    def load_wav(self):
        for file in self.files:
            sound = pygame.mixer.Sound(file)
            self.sounds.append(sound)

    def play(self, i):
        try:
            self.turn = (self.turn + 1) % self.limit
            self.channels[self.turn].stop()
            self.channels[self.turn].play(self.sounds[i])
        except:
            print("Error: Guitar.play()")
