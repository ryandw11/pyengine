import pygame
import threading
import sys

scr = ""

deltaTime = 0.0

pressedkeys = []

class PYEngine:
    def __init__(self, pybuilder):
        pygame.init()
        self.screen = sc = pygame.display.set_mode((pybuilder.size[0], pybuilder.size[1]))
        sc.fill(pybuilder.background)
        pygame.display.set_caption(pybuilder.title)
        self.builder = pybuilder

    def start(self):
        self.begin()

    def begin(self):
        import pygame
        global scr
        global deltaTime
        scr = self.screen
        clock = pygame.time.Clock()
        playing_game = True
        getTicksLastFrame = 0
        while playing_game:
            clock.tick(self.builder.speed)

            t = pygame.time.get_ticks()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    EventHandler.triggerHandler("KeyDownEvent", [event.key])
                    if event.key not in pressedkeys:
                        pressedkeys.append(event.key)
                elif event.type == pygame.KEYUP:
                    pressedkeys.remove(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    EventHandler.triggerHandler("MouseDownEvent", [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
            self.screen.fill(self.builder.background)
            for go in gameobjects:
                go.draw()
            pygame.display.update()
            # Trigger the update event
            EventHandler.triggerHandler("UpdateEvent", [])
        pygame.quit()

    def stop(self):
        pygame.quit()
        sys.exit()

    @staticmethod
    def getScreen():
        return scr

class PYEngineBuilder:
    def __init__(self, size):
        self.size = size
        self.title = "A PyEngine Game"
        self.background = (255, 255, 255)
        self.speed = 45

    def setTitle(self, title):
        self.title = title
        return self

    def setBackground(self, background):
        self.background = background
        return self

    def setSpeed(self, speed):
        self.speed = speed
        return self

    def build(self):
        return PYEngine(self)

gameobjects = []

class GameObjectManager:
    def __init__(self):
        pass
    @staticmethod
    def add(obj):
        gameobjects.append(obj)

    @staticmethod
    def remove(obj):
        gameobjects.remove(obj)


class Rectangle:
    def __init__(self):
        self.size = [50, 50]
        self.position = [0, 0]
        self.color = (255, 0, 0)

    def setSize(self, size):
        self.size = size
        return self

    def setPosition(self, pos):
        self.position = pos
        return self

    def setColor(self, color):
        self.color = color
        return self

    def translate(self, pos):
        newpos = []
        newpos.append(self.position[0] + pos[0])
        newpos.append(self.position[1] + pos[1])
        self.position = newpos

    def draw(self):
        rect = pygame.Rect((self.position[0], self.position[1], self.size[0], self.size[1]))
        pygame.draw.rect(scr, self.color, rect)
        return rect

class Text:
    font = "freesansbold.ttf"
    size = 40
    def __init_(self):
        self.size = 40
        self.color = (0, 0, 0)
        self.font = 'freesansbold.ttf'
        self.text = 'Text'
        self.position = [0, 0]

    def setTextSize(self, size):
        self.size = size
        return self

    def setColor(self, color):
        self.color = color
        return self

    def setFont(self, font):
        self.font = font
        return self

    def setText(self, text):
        self.text = text
        return self

    def setPosition(self, pos):
        self.position = pos
        return self

    def draw(self):
        fonts = pygame.font.Font(self.font, self.size)
        text = fonts.render(self.text, True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.position[0], self.position[1])
        scr.blit(text, textRect)


class Circle:
    def __init__(self):
        self.radius = 0
        self.position = [0, 0]
        self.color = (255, 0, 0)

    def setRadius(self, radius):
        self.radius = radius
        return self

    def setPosition(self, pos):
        self.position = pos
        return self

    def setColor(self, color):
        self.color = color
        return self

    def translate(self, pos):
        newpos = []
        newpos.append(self.position[0] + pos[0])
        newpos.append(self.position[1] + pos[1])
        self.position = newpos

    def draw(self):
        rect = pygame.draw.circle(scr, self.color, self.position, self.radius)
        return rect

class Sprite:
    def __init__(self):
        self.image = "example.png"
        self.position = [0, 0]

    def setImage(self, image):
        self.image = image
        return self

    def setPosition(self, pos):
        self.position = pos
        return self


    def translate(self, pos):
        newpos = []
        newpos.append(self.position[0] + pos[0])
        newpos.append(self.position[1] + pos[1])
        self.position = newpos

    def draw(self):
        img = pygame.image.load(self.image)
        scr.blit(img, self.position)
        return img.get_rect()


class KeyHandler:
    @staticmethod
    def isKeyPressed(key):
        if key in pressedkeys: return True
        return False

listeners = []

class EventHandler:
    @staticmethod
    def addHandler(handlerclass, function):
        listeners.append([handlerclass, function])

    @staticmethod
    def triggerHandler(handlerclass, triggers):
        for l in listeners:
            obj = "UpdateEvent"
            if handlerclass == "UpdateEvent":
                if l[0] == "UpdateEvent":
                    obj = UpdateEvent
                else:
                    continue
            elif handlerclass == "KeyDownEvent":
                if l[0] == "KeyDownEvent":
                    obj = KeyDownEvent(triggers[0])
                else:
                    continue
            elif handlerclass == "MouseDownEvent":
                if l[0] == "MouseDownEvent":
                    obj = MouseDownEvent(triggers[0], triggers[1])
                else:
                    continue
            if type(obj) == "string":
                continue
            l[1](obj)


class UpdateEvent:
    def __init__(self):
        pass

    def getDeltaTime(self):
        return deltaTime

class KeyDownEvent:
    def __init__(self, key):
        self.key = key

    def getKey(self):
        return self.key

class KeyPressendEvent:
    def __init__(self, key):
        self.key = key

    def getKey(self):
        return self.key

class MouseDownEvent:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def getPosition(self):
        return [self.pos1, self.pos2]


class CollisionManager:
    @staticmethod
    def isColliding(obj1, obj2):
        rect = obj1.draw()
        rect2 = obj2.draw()
        return rect.colliderect(rect2)

    @staticmethod
    def collidePoint(obj1, point):
        return obj1.draw().collidepoint(point)

class Sound:
    def __init__(self, sound):
        self.sound = pygame.mixer.Sound(sound)

    def play(self):
        pygame.mixer.Sound.play(self.sound)

class Music:
    @staticmethod
    def set(music):
        pygame.mixer.music.load(music)

    @staticmethod
    def play(loops):
        pygame.mixer.music.play(loops)

    @staticmethod
    def pause():
        pygame.mixer.music.pause()

    @staticmethod
    def unpause():
        pygame.mixer.music.unpause()