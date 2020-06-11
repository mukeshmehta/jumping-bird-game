import pygame
import random
import sys

from pygame.locals import *

# Global variables

FPS = 32
SCREEN_WIDTH = 404
SCREEN_HEIGHT = 650
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND = SCREEN_HEIGHT * 0.85
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2 # to display bird in center and not to go out of screen
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # to quit the game
                pygame.quit()
                sys.exit()

            elif(event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                # to exit welcome screen and start the game
                return

            else:
                #blit following images at mentioned coordinates
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['message'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUND))
                pygame.display.update() # screen will not change until this function is called
                FPSCLOCK.tick(FPS)  # control max FPS

def mainGame():
    score = 0
    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_WIDTH/2)
    basex = 0

    # Create 2 random pipes
    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    #List of upper pipes
    upperPipes = [
        {'x': SCREEN_WIDTH + 200, 'y': pipe1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2), 'y': pipe2[0]['y']}
    ]
    # list of lower pipes
    lowerPipes = [
        {'x': SCREEN_WIDTH + 200, 'y': pipe1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2), 'y': pipe2[1]['y']}
    ]

    pipeSpeedX = -4

    playerSpeedY = -9
    playerMaxSpeedY = 10
    playerAccY = 1

    playerFlapSpeed = -8    # speed of player while flapping
    playerFlapped = False # is playing flying ?

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # to quit the game
                pygame.quit()
                sys.exit()

            if(event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                # to exit game
                if playery > 0:
                    playerSpeedY = playerFlapSpeed
                    playerFlapped = True
                    #GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"Your Score is {score}")
                GAME_SOUNDS['point'].play()

        if playerSpeedY < playerMaxSpeedY and not playerFlapped:
            playerSpeedY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerSpeedY, GROUND - playery - playerHeight)

        # pipe movement

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeSpeedX
            lowerPipe['x'] += pipeSpeedX

        # add new pipe, when first pipe is about to out of screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # remove pipes if out of screen

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # blit sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        xOffset = (SCREEN_WIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xOffset, SCREEN_HEIGHT*0.12))
            xOffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUND-80 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    # Generate positions of lower pipe and upper inverted pipe
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    delta = SCREEN_HEIGHT/3
    y2 = delta + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * delta))
    pipex = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + delta
    pipe = [
        {'x' : pipex, 'y': -y1},    #upper pipe
        {'x' : pipex, 'y': y2}      #lower pipe
    ]
    return pipe


if __name__=="__main__":
    pygame.init()   # initialize pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('JumpingBird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )   # convert_alpha optimizes the images to render according to game screen

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
         )

    #GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert()

    while True:
        welcomeScreen()     #Welcome screen until screen is touched
        mainGame()