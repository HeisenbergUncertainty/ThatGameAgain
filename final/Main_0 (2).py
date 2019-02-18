import pygame
import os
from Cheats import cheat
from random import randrange, choice

pygame.init()
Size = Width, Height = 600, 600
screen = pygame.display.set_mode(Size)
clock = pygame.time.Clock()
FPS = 40
GRAVITY = 1
V = 15
screen_rect = (0, 0, Width, Height)


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


FON = pygame.transform.scale(load_image('death2.jpg'), (Width, Height))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in range(5, 21, 4):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class Platform(pygame.sprite.Sprite):
    sizes = [width, height] = [100, 40]
    image = load_image('hleb2.png')

    def __init__(self, pos, group):
        super().__init__(group)
        self.speed = 2
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class UsualPlatform(Platform):
    def __init__(self, pos, group):
        self.color = (100, 100, 100)
        super().__init__(pos, group)


class XMovePlatform(Platform):
    def __init__(self, pos, group, dx=0, n=1):
        self.color = (0, 100, 0)
        super().__init__(pos, group)
        self.speed *= n
        self.dx = dx

    def update(self):
        self.rect.x += self.speed
        self.dx += self.speed

        next_x = self.rect.x + self.speed
        if abs(self.dx) > 2 * self.width \
                or Width - self.width < next_x or 0 > next_x:
            self.speed *= -1


class YMovePlatform(Platform):
    def __init__(self, pos, group):
        self.color = (0, 0, 100)
        super().__init__(pos, group)
        self.dy = 0

    def update(self):
        self.rect.y += self.speed
        self.dy += self.speed

        if abs(self.dy) >= 2 * self.width:
            self.speed *= -1


class SpeedUp(pygame.sprite.Sprite):
    sizes = [width, height] = [20, 30]

    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface(SpeedUp.sizes)
        self.image.fill((200, 200, 0))
        self.rect = pygame.Rect(*pos, *SpeedUp.sizes)


class Character(pygame.sprite.Sprite):
    sizes = [width, height] = [50, 50]
    image = load_image('cupcake4.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Character.image
        self.rect = self.image.get_rect()
        self.rect.x = Width // 2
        self.rect.y = Height - self.height
        self.flow = Height
        self.xspeed = 3
        self.speed = 0
        self.acceleration = 0.5
        self.speed_flag = True

    def update(self):

        if pygame.sprite.spritecollideany(self, speedup):
            self.speed -= 0.5
            self.speed_flag = False

        if (pygame.sprite.spritecollideany(self,
                                           platform) or pygame.sprite.spritecollideany(
            self, moveplatform) or pygame.sprite.spritecollideany(self,
                                                                  safeplatforms)) and self.speed > 0:
            self.speed = max(self.speed * 0.9, V) * (-1)

        else:
            if self.speed_flag:
                self.speed += self.acceleration

            if abs(self.speed) > V:
                direction = 1 if self.speed >= 0 else -1
                self.speed = V * direction
                self.speed_flag = False
            else:
                self.speed_flag = True

            self.flow = self.rect.y

        self.rect.y += int(self.speed)
        create_particles((self.rect.x + 25, self.rect.y + 60))

    def change_x(self, k):
        self.rect.x += self.xspeed * k
        if self.rect.x <= -Character.width // 2:
            self.rect.x = Width - Character.width
        elif self.rect.x > Width - Character.width // 2:
            self.rect.x = 0


class ButtonStart(pygame.sprite.Sprite):
    image = load_image('start2.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = ButtonStart.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Camera:
    def __init__(self):
        self.restart()

    def restart(self):
        self.nado = 0
        self.y = Height
        self.dy = 0

    def update(self, target):
        if target.rect.y < Height - Height * 0.3:
            self.dy = Height - Height * 0.3 - target.rect.y
            self.change_ys(ALL)
            # if flags[1]:
            #     self.dy *= -1
            #     self.change_ys([safeplatforms])

        elif flags[0]:
            if target.rect.y >= Height - 30 and self.y > Height - 30:
                self.dy = Height - 30 - target.rect.y

            self.change_ys(ALL)

        else:
            if target.rect.y >= Height + 20:
                self.dy = 0
                return True

        for object in safeplatforms:
            if not flags[1]:
                break
            object.rect.y = self.y

        self.y += self.dy
        self.dy = 0
        return False

    def change_ys(self, groups):
        self.y += self.dy
        self.nado += self.dy

        for group in groups:
            for object in group:
                # if
                object.rect.y += self.dy

    def new_platforms(self, score):
        if self.nado >= Height // 5:
            palki(-UsualPlatform.height, score)
            self.nado = 0


def create_particles(position):
    particle_count = 1
    numbers = range(-5, 5)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


def start_screen():
    flags = [False, False, False]
    button = pygame.sprite.Group()
    ButtonStart(button)
    fon = FON
    screen.blit(fon, (0, 0))
    button.draw(screen)
    pygame.display.flip()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == 2:
                flags = cheat(keys, flags)
            if event.type == pygame.QUIT:
                return False, flags
            elif event.type == 5:
                return True, flags


def pause(flags):
    pause_flag = True

    surface = pygame.Surface(Size)
    surface.fill((200, 200, 200))
    surface.set_alpha(150)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    while pause_flag:
        clock.tick(FPS)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == 2:
                flags = cheat(keys, flags)

            if event.type == pygame.QUIT:
                return False, flags
            elif keys[27]:
                pause_flag = False

    return True, flags


def death(flags, score):
    fon = pygame.transform.scale(load_image('go2.png'), (Width, Height))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 100)
    text = font.render(str(score), 1, (255, 255, 255))
    text_x = (Width - text.get_width()) // 2
    screen.blit(text, (text_x, Height // 2))

    pygame.display.flip()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == 2:
                flags = cheat(keys, flags)
            if event.type == pygame.QUIT:
                return False, flags
            elif event.type == 2:
                flags = cheat(keys, flags)
                camera.restart()
                player.rect.x = Width // 2 - 50
                player.rect.y = Height - player.height
                make_safezone()
                make_starter_palki()

                pygame.mixer.music.load(START_SONG)
                pygame.mixer.music.play(-1)
                return True, flags


def palki(high, score):
    all_count = choice([2, 3])
    x_count = 0

    if randrange(0, 200) < int(min(1, score / 1000) * 100):
        all_count -= 1

    if randrange(0, 100) < int(min(1, score / 1000) * 100):
        x_count = min(score // 100, all_count)

    for j in range(all_count - x_count):
        UsualPlatform((randrange(0, Width - Platform.width), high),
                      safeplatforms)

    for j in range(x_count):
        XMovePlatform((randrange(0, Width - Platform.width), high),
                      moveplatform,
                      randrange(-Platform.width, Platform.width),
                      choice([1, -1]))


def make_safezone():
    for i in range(Width // Platform.width + 1):
        UsualPlatform((i * Platform.width, Height - Platform.height),
                      safeplatforms)


def make_starter_palki():
    for i in range(0, Height + UsualPlatform.height, Height // 5 + 1):
        palki(i, 0)


def cleaner(all, total):
    for data in all:
        for object in data:
            if object.rect.y > 30000 or total:
                object.kill()


platform = pygame.sprite.Group()
safeplatforms = pygame.sprite.Group()
moveplatform = pygame.sprite.Group()
speedup = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Character(all_sprites)
START_SONG = os.path.join('data', 'Shooting-Stars.mp3')
END_SONG = os.path.join('data', 'go-on.mp3')
pygame.mixer.music.load(START_SONG)

ALL = [platform, safeplatforms, moveplatform, speedup, all_sprites]

make_safezone()
camera = Camera()
running, flags = start_screen()

make_starter_palki()

pygame.mixer.music.play(-1)
while running:
    clock.tick(FPS)
    score = int(camera.y - Height) // 100
    cleaner(ALL[:~0], False)

    for event in pygame.event.get():
        if event.type == 12:
            running = False

        if pygame.key.get_pressed()[27]:
            running, flags = pause(flags)

        if event.type == 5:
            if event.button == 1:
                UsualPlatform(event.pos, platform)
            if event.button == 3:
                SpeedUp(event.pos, speedup)

        if event.type == 2:
            keys = pygame.key.get_pressed()

            if keys[120]:
                XMovePlatform(pygame.mouse.get_pos(), moveplatform)
            if keys[121]:
                YMovePlatform(pygame.mouse.get_pos(), moveplatform)

            flags = cheat(keys, flags)

    for obj in moveplatform:
        obj.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[97]:
        player.change_x(-1)
    if keys[pygame.K_RIGHT] or keys[100]:
        player.change_x(1)

    all_sprites.update()
    death_flag = camera.update(player)
    camera.new_platforms(score)

    if flags[0] and death_flag:
        death_flag = False

    if death_flag:
        cleaner(ALL[:~0], True)
        pygame.mixer.music.load(END_SONG)
        pygame.mixer.music.play()
        running, flags = death(flags, score)

    screen.blit(FON, (0, 0))

    font = pygame.font.Font(None, 50)
    text = font.render(str(score), 1, (255, 255, 255))
    screen.blit(text, (0, 0))
    for group in ALL:
        group.draw(screen)

    pygame.display.flip()
pygame.quit()
