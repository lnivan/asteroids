import pygame
import time
import random
import math

gameLength = 800
gameWidth = 800

white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode([gameLength, gameWidth])

class Sprite:
    #Definicion de variables del objeto
    def __init__(self, position, polarPoints, size, width):

        self.polarPoints = polarPoints
        for polarPoint in self.polarPoints:
            polarPoint[1] = polarPoint[1] * size
        self.width = width
        self.position = position
        self.rotation = 0

    #Dibujar objeto
    def draw(self):

        #Obtencion de coordenadas cartesianas a partir de las polares para poder dibujarlo (Pygame usa cartesianas)
        cartesianPoints = []
        for polarPoint in self.polarPoints:
            xPosition = math.sin(math.radians(polarPoint[0])) * polarPoint[1]
            yPosition = math.cos(math.radians(polarPoint[0])) * polarPoint[1]
            cartesianPoint = [xPosition + self.position[0] , yPosition + self.position[1]]
            cartesianPoints.append(cartesianPoint)

        #A partir de los puntos que hemos obtenido podemos dibujar el objeto
        pygame.draw.polygon(screen, black, cartesianPoints, self.width)

    #Girar el objeto los angulos deseados
    def turn(self, degree):
        for polarPoint in self.polarPoints:
            polarPoint[0] = polarPoint[0] + degree
        self.rotation = self.rotation + degree




def pythagoras(cathets):
    return(math.sqrt(math.pow(cathets[0], 2) + math.pow(cathets[1], 2)))



class Missile:
    def __init__(self, position, degree, initialSpeed):
        speed = 300
        self.position = position
        xSpeed = math.sin(math.radians(degree + 180)) * speed
        ySpeed = math.cos(math.radians(degree + 180)) * speed
        self.speed = [initialSpeed[0] + xSpeed, initialSpeed[1] + ySpeed]
        self.timeLast = time.time()
        self.lifeTimer = time.time()
    
    def update(self):
    
        if time.time() - self.lifeTimer >= 2:
            missileArray.remove(self)

        deltaTime = time.time() - self.timeLast
        self.timeLast = time.time()

        self.position[0], self.position[1] = self.position[0] + self.speed[0] * deltaTime, self.position[1] + self.speed[1] * deltaTime 
        if self.position[0] > gameLength:
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = gameLength
        if self.position[1] > gameWidth:
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = gameWidth

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), self.position, 2, 0)







class Ship(Sprite):
    def __init__(self):

        super().__init__([int(gameLength / 2), int(gameWidth / 2)], [[45, 0.707], [315, 0.707], [180, 1]], 10, 2)
        self.speed = [0, 0]
        self.lifes = 3
        self.acceleration = 0
        self.turnDirecction = 0
        self.speedCap = 300
        self.timeLast = time.time()
    
    def update(self):
        for asteroid in asteroidArray:
            if pythagoras([self.position[0] - asteroid.position[0], self.position[1] - asteroid.position[1]]) <= asteroid.size * 20:
                if self.lifes > 0:
                    self.lifes = self.lifes - 1
                    self.speed = [0, 0]
                    self.acceleration = 0
                    self.turn(-self.rotation)
                    self.position = [gameLength / 2, gameWidth / 2]
                

        deltaTime = time.time() - self.timeLast
        self.timeLast = time.time()

        self.turn(self.turnDirecction * deltaTime)
        
        acceleration = [-math.sin(math.radians(self.rotation)) * self.acceleration, -math.cos(math.radians(self.rotation)) * self.acceleration]

        self.speed[0], self.speed[1] = self.speed[0] + acceleration[0] * deltaTime, self.speed[1] + acceleration[1] * deltaTime
        if pythagoras(self.speed) > self.speedCap:
            ratio = self.speedCap / pythagoras(self.speed)
            self.speed[0], self.speed[1] = self.speed[0] * ratio, self.speed[1] * ratio

        self.position[0], self.position[1] = self.position[0] + self.speed[0] * deltaTime, self.position[1] + self.speed[1] * deltaTime
        if self.position[0] > gameLength:
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = gameLength
        if self.position[1] > gameWidth:
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = gameWidth
        
    def shoot(self):
        return(Missile(self.position[:], self.rotation, self.speed[:]))







class Asteroid(Sprite):
    def __init__(self, size, position):
        
        meteorShapes = [[[0, 0.30], [45, 0.80], [90, 0.65], [135, 0.45], [180, 1], [225, 0.94], [270, 0.68], [315, 0.92]], 
                        [[0, 0.27], [45, 0.77], [90, 0.54], [135, 0.95], [180, 1], [225, 0.62], [270, 0.78], [315, 0.48]],
                        [[0, 0.28], [45, 0.45], [90, 0.76], [135, 0.64], [180, 1], [225, 0.84], [270, 0.46], [315, 0.70]]]

        super().__init__(position, random.choice(meteorShapes), size * 20, 2)
        self.size = size
        self.speed = [random.randint(-100, 100), random.randint(-100, 100)]
        self.turnDirecction = random.randint(0, 90)
        self.timeLast = time.time()
    
    def update(self):
        for missile in missileArray:
            if pythagoras([missile.position[0] - self.position[0], missile.position[1] - self.position[1]]) <= self.size * 20:
                if self.size > 1:
                    asteroidArray.remove(self)
                    missileArray.remove(missile)
                    for i in range(3):
                        asteroidArray.append(Asteroid(self.size - 1, self.position[: ]))
                else:
                    asteroidArray.remove(self)
                    missileArray.remove(missile)

        deltaTime = time.time() - self.timeLast
        self.timeLast = time.time()

        self.turn(self.turnDirecction * deltaTime)

        self.position[0], self.position[1] = self.position[0] + self.speed[0] * deltaTime, self.position[1] + self.speed[1] * deltaTime
        if self.position[0] > gameLength:
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = gameLength
        if self.position[1] > gameWidth:
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = gameWidth


ship = Ship()


asteroidArray = []
for i in range(5):
    asteroidArray.append(Asteroid(3, [random.randint(0, gameLength), random.randint(0, gameWidth)]))

missileArray = []


#Activo hasta que deje de correr (borreme  3)
running = True
while running == True:

    #Comprobar cada evento
    for event in pygame.event.get():

        #Si el evento es salir, se cierra la aplicacion
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d:
                ship.turnDirecction = -180

            if event.key == pygame.K_a:
                ship.turnDirecction = 180

            if event.key == pygame.K_w:
               ship.acceleration = 300

            if event.key == pygame.K_s:
                ship.acceleration = -300

            if event.key == pygame.K_SPACE:
                missileArray.append(ship.shoot())

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w or event.key == pygame.K_s:
                ship.acceleration = 0

            if event.key == pygame.K_a or event.key == pygame.K_d:
                ship.turnDirecction = 0               


    screen.fill(white)

    if ship.lifes != 0:
        ship.update()
        ship.draw()

    for asteroid in asteroidArray:
        asteroid.update()
        asteroid.draw()

    for missile in missileArray:
        missile.update()
        missile.draw()

    pygame.display.flip()






