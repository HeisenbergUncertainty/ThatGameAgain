import pygame
import os
import random

pygame.init() 
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
V = 100

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image
      
class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface([50, 10])
        self.image.fill((100, 100, 100))
        self.rect = pygame.Rect(*pos, 50, 10)

class Character(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(20, 100, 20, 20)
        self.flag = True
    
    def update(self):
        if not pygame.sprite.spritecollideany(self, platform):
            self.rect.y += V / FPS
            self.a = self.rect.y
        else:
            if self.a + self.rect.y <= 30:
                v = V * 2
                c.rect.y -=  v / FPS
                
        

    def teleport(self, event):
        self.rect.x = event.pos[0]
        self.rect.y = event.pos[1]
        
                                    
platform = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
running = True
flag = True
c = Character(all_sprites)
for i in range(10):
    Platform((i * 50, 490), platform)
    

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Platform(event.pos, platform)
            if event.button == 3:
                c.teleport(event)
                
    #if pygame.sprite.spritecollideany(c, platform):
    #if pygame.key.get_pressed()[pygame.K_UP]:
     #   v = V * 2
      #  c.rect.y -=  v / FPS
                
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if c.rect.x > 0:
            c.rect.x -= 2
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if c.rect.x  <= width - 20:
            c.rect.x += 2

    
    clock.tick(FPS)
    screen.fill((255, 255, 255))
    platform.draw(screen)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
