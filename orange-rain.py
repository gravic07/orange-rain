#!/Users/gravic/.local/share/virtualenvs/orange-rain-foR5V4Is/bin/python
import pygame
import sys
import random

pygame.init()
pygame.font.init()

black = 0, 0, 0
green = 0, 255, 70
orange = 254, 153, 0
orangeHighlight = 250, 200, 70
greenHighlight = 70, 255, 70

size = width, height = 1280, 720
symbolSize = 21
fontFace = "NotoSansCJK-Medium.ttc"
currentColor = orange
currentHighlight = orangeHighlight

screen = pygame.display.set_mode(size)
screen.fill(black)
pygame.display.set_caption("Orange Rain")
clock = pygame.time.Clock()
font = pygame.font.Font(fontFace, symbolSize)
frameCnt = 0


class Symbol:
    def __init__(self, x, y, speed, isFirst):
        self.x = x
        self.y = y
        self.value = ""
        self.speed = speed
        self.isFirst = isFirst
        self.changeInterval = random.randint(4, 21)

    def setRandomValue(self):
        if frameCnt % self.changeInterval == 0:
            charType = random.randint(0, 5)
            if charType > 1:
                # set to a katakana character
                uniChar = 0x30A0 + random.randint(0, 95)
                self.value = chr(uniChar)
            else:
                # set to number
                self.value = str(random.randint(0, 9))

    def render(self):
        if self.isFirst:
            textSurface = font.render(self.value, True, currentHighlight)
        else:
            textSurface = font.render(self.value, True, currentColor)
        textRect = textSurface.get_rect()
        textRect.center = (self.x, self.y)
        screen.blit(textSurface, textRect)
        self.fall()

    def fall(self):
        if self.y > height:
            self.setRandomValue()
            self.y = 0
        else:
            self.y += self.speed

    def adjustSpeed(self, direction):
        if direction == "up":
            self.speed += 1
        elif direction == "down":
            self.speed -= 1
        else:
            pass


class Stream:
    def __init__(self):
        self.symbols = []
        self.symbolCnt = random.randint(2, 12)
        self.speed = random.randint(2, 5)

    def generateSymbols(self, x, y):
        isFirst = True if random.randint(0, 4) == 1 else False
        for s in range(self.symbolCnt):
            sym = Symbol(x, y, self.speed, isFirst)
            sym.setRandomValue()
            self.symbols.append(sym)
            y -= symbolSize
            isFirst = False

    def render(self):
        for sym in self.symbols:
            sym.render()
            sym.setRandomValue()
            sym.fall()


streams = []
y = 0
while y < width:
    stream = Stream()
    stream.generateSymbols(y, random.randint(-200, -5))
    streams.append(stream)
    y += symbolSize


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.K_ESCAPE:
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sys.exit()
            if e.key == pygame.K_SPACE:
                if currentColor == orange:
                    currentColor = green
                    currentHighlight = greenHighlight
                else:
                    currentColor = orange
                    currentHighlight = orangeHighlight
            if e.key == pygame.K_UP:
                for stream in streams:
                    for symbol in stream.symbols:
                        symbol.adjustSpeed("up")
            if e.key == pygame.K_DOWN:
                for stream in streams:
                    for symbol in stream.symbols:
                        symbol.adjustSpeed("down")

    fauxScreen = pygame.Surface((width, height))
    fauxScreen.set_alpha(125)
    fauxScreen.fill(black)
    screen.blit(fauxScreen, (0, 0))
    for stream in streams:
        stream.render()

    # pressed = pygame.key.get_pressed()
    # if pressed[pygame.K_ESCAPE]:
    #     sys.exit()

    pygame.display.flip()

    frameCnt += 1

# pygame.quit()
# quit()
