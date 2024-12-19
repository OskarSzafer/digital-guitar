import os
import pygame

# class Guitar():

#     folder_path = ''
#     files = []
#     sounds = []
#     channels = []

#     def __init__(self, path):
#         self.folder_path = path
#         pygame.mixer.init()
#         self.find_all_files()
#         self.load_wav()

#         pygame.mixer.set_num_channels(len(self.sounds))

#         for i in range(len(self.sounds)):
#             self.channels.append(pygame.mixer.Channel(i))

#     def find_all_files(self):
#         for root, dirs, files in os.walk(self.folder_path):
#             for file in files:
#                 self.files.append(os.path.join(root, file))

#     def load_wav(self):
#         for file in self.files:
#             sound = pygame.mixer.Sound(file)
#             self.sounds.append(sound)

#     def play(self, i):
#         # self.channels[i].stop()
#         self.channels[i].play(self.sounds[i])

class Guitar():

    folder_path = ''
    files = []
    sounds = []
    channels = []

    turn = 0
    limit = 100

    def __init__(self, path):
        self.folder_path = path
        pygame.mixer.init()
        self.find_all_files()
        self.load_wav()

        pygame.mixer.set_num_channels(self.limit)

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
        self.turn = (self.turn + 1) % self.limit
        self.channels[self.turn].stop()
        self.channels[self.turn].play(self.sounds[i])
