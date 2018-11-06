import pygame
from pygame.locals import *
import os
import random
import sys

SCR_RECT = Rect(0, 0, 640, 480)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"InvaderGame")

if __name__ == "__main__":
    main()
