import pygame
import sys
import random

pygame.init()

clock = pygame.time.Clock()

HEIGHT = 600
WIDTH = 900

bg_y = -144
scroll = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_images = []

for i in range(0, 4):
    bg_image = pygame.image.load(f"drawingl{i}.png").convert_alpha()
    bg_images.append(bg_image)

left = 0
end_position = 0
rectangles = []

low_width = 100
high_width = 250

low_height = 30
high_height = 350

choice = 0
right = 0


def blit():
    for x in range(20):
        speed = 1
        for image in bg_images:
            screen.blit(image, ((x * 950) + scroll * speed, bg_y))
            speed += 0.08


class Platforms(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
    
    def move_ip(self, dir):
        self.rect.move_ip(dir, 0)

class MovingPlatforms(Platforms):
    def __init__(self, x, y, height, width, end_pos):
        super().__init__(x, y, height, width)
        self.end_pos = end_pos
        self.direction = 3
    
    def move(self):
        self.rect.x += self.direction
        for rects in buildings:
            if self.rect.colliderect(rects):
                self.direction = self.direction * -1
        for rects in moving_platforms:
            if self.rect.colliderect(rects):
                if self.rect != rects:
                    self.direction = self.direction * -1

moving_platforms = pygame.sprite.Group()
buildings = pygame.sprite.Group()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll < 0:
        scroll += 5
        for rect in buildings:
            rect.move_ip(5)
        for thing in moving_platforms:
            thing.move_ip(5)
    if key[pygame.K_RIGHT] and scroll > -3850:
        scroll -= 5
        for rect in buildings:
            rect.move_ip(-5)
        for thing in moving_platforms:
            thing.move_ip(-5)
    if key[pygame.K_DOWN] and bg_y > -144:
        bg_y -= 3

    if left <= 4750:
        width_add = random.randrange(low_width, high_width)
        height_add = random.randrange(low_height, high_height)
        choice = random.choice([1, 2, 1])
        if choice == 1:
            building = Platforms(left + 10, (600 - height_add), height_add, width_add)
            buildings.add(building)
        elif choice == 2:

            mbuilding = MovingPlatforms(left + 10, 600 - high_height + 50, 30, width_add/2,\
                                         end_position)
            moving_platforms.add(mbuilding)                   
        
    blit()

    buildings.update()
    buildings.draw(screen)
    moving_platforms.draw(screen)
    
    for thingses in moving_platforms:
        thingses.move()

    if high_height > low_height + 5:
        high_height = height_add + 50

    if left <= 4750:
        left += width_add

    pygame.display.update()

pygame.quit()
sys.exit()


