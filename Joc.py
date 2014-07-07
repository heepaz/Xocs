import pygame


class Quadrat (pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, vx=0, vy=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy

    def update(self, dt, joc):
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        self.rect.x %= joc.amplada
        self.rect.y %= joc.alçada


class QuadratR (Quadrat):
    def __init__(self, x=0, y=0, vx=0, vy=0):
        Quadrat.__init__(self, 'Imatges/Roja.png', x, y, vx, vy)
        self.imatge_roig = self.image
        self.imatge_blau = pygame.image.load('Imatges/Blava.png')


class QuadratV (Quadrat):
    def __init__(self, x=0, y=0, vx=0, vy=0):
        Quadrat.__init__(self, 'Imatges/Verda.png', x, y, vx, vy)

    def update(self, dt, joc):
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        self.rect.x %= joc.amplada
        self.rect.y %= joc.alçada

        # Mirem amb quins quadrats hem xocat del grup enemics
        ll_sprites = pygame.sprite.spritecollide(self, joc.grup_enemics, False)
        # A tot el grup d'enemics els posem la imatge vermella
        for sprite in joc.grup_enemics:
            sprite.image = sprite.imatge_roig
        # Als que estan xocant amb nosaltres els posem la blava
        for sprite in ll_sprites:
            sprite.image = sprite.imatge_blau


class Joc (object):
    def main(self, pantalla):
        self.amplada, self.alçada = pantalla.get_size()
        self.surt = False

        rellotge = pygame.time.Clock()

        self.quadrat = QuadratV(10, 20, 11, 17)
        self.grup_jugador = pygame.sprite.GroupSingle(self.quadrat)

        self.quadrat2 = QuadratR(20, 20, -5, 10)
        self.quadrat3 = QuadratR(200, 200, -5, 10)
        self.quadrat4 = QuadratR(300, 250, 5, -10)
        self.quadrat5 = QuadratR(400, 500, 5, -7)
        self.grup_enemics = pygame.sprite.Group()
        self.quadrat2.add(self.grup_enemics)
        self.quadrat3.add(self.grup_enemics)
        self.quadrat4.add(self.grup_enemics)
        self.quadrat5.add(self.grup_enemics)

        while not self.surt:
            dt = rellotge.tick(30)
            self.gestiona_esdeveniment()
            self.update(dt/100)
            self.draw(pantalla)

    def gestiona_esdeveniment(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.surt = True

    def update(self, dt):
        self.grup_jugador.update(dt, self)
        self.grup_enemics.update(dt, self)

    def draw(self, pantalla):
        pantalla.blit(pygame.Surface((self.amplada, self.alçada)), (0, 0))
        self.grup_jugador.draw(pantalla)
        self.grup_enemics.draw(pantalla)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    amplada = 800
    alçada = 600
    pantalla = pygame.display.set_mode((amplada, alçada))
    Joc().main(pantalla)
    pygame.quit()
