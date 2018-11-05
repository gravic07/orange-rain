import pygame, sys, random

pygame.init()
pygame.font.init()

size = width, height = 600, 400
symbolSize = 21
black = 0, 0, 0
color = 0, 255, 70
lightColor = 250, 255, 250

screen = pygame.display.set_mode(size, pygame.SRCALPHA)
pygame.display.set_caption("Orange Rain")
clock = pygame.time.Clock()
font = pygame.font.Font("NotoSansCJK-Medium.ttc", symbolSize)
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
        if  frameCnt % self.changeInterval == 0:
            charType = random.randint(0, 5)
            if charType > 1:
                # set to a katakana character
                uniChar = 0x30A0 + random.randint(0, 96)
                self.value = chr(uniChar)
            else:
                # set to number
                self.value = str(random.randint(0,9))
	
    def render(self):
        if self.isFirst:
            textSurface = font.render(self.value, True, lightColor)
            print('LIGHT')
        else:
            textSurface = font.render(self.value, True, color)
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


class Stream:
    def __init__(self):
        self.symbols = []
        self.symbolCnt = random.randint(2, 12)
        self.speed = random.randint(3, 9)

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
            # TODO Can't I just call sym.render() here instead?
            #textSurface = font.render(sym.value, True, color)
            #textRect = textSurface.get_rect()
            #textRect.center = (sym.x, sym.y)
            #screen.blit(textSurface, textRect)
            sym.render()
            sym.setRandomValue()
            sym.fall()


streams = []
y = 0
while y < width:
    stream = Stream()
    stream.generateSymbols(y, 0)
    streams.append(stream)
    y += symbolSize



while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    for stream in streams:
        stream.render()
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        color = 254, 153, 0

    if pressed[pygame.K_LEFT]:
        thrust += -1

    if pressed[pygame.K_RIGHT]:
        thrust += 1


    pygame.display.flip()

    frameCnt += 1

# pygame.quit()
# quit()
