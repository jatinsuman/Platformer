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

sprite_sheet_image = pygame.image.load("MainCharacter.png").convert_alpha()
spikes = pygame.image.load("Spikes.png").convert_alpha()

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, height, width, scale, color, action_num):
        self.action_num = action_num
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), (self.action_num * 36) , width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image

sprite_sheet = SpriteSheet(sprite_sheet_image)
spike_sheet = SpriteSheet(spikes)

animation_list = []
spikes_list = []
framey = 0
animation_steps = 7
last_update = pygame.time.get_ticks()
frame = 0
dis = 0
high = 0

def animation(speed, action, blitimage, cooldown, jump, steps):
    global dis, last_update, frame, high
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= cooldown:
        frame += 1
        last_update = current_time
        dis += speed
        if sprite_sheet.action_num == 2:
            high += jump
        if frame >= steps:
            frame = 1           
            high = 0
    for thing in animation_list:
        animation_list.remove(thing)
    for x in range(animation_steps):
        animation_list.append(sprite_sheet.get_image(x, 36, 49, 1.5, (0, 0, 0), action))
    screen.blit(blitimage, (0 + dis, 30 - high))
    

left = 0
end_position = 0
rectangles = []

low_width = 100
high_width = 250

low_height = 30
high_height = 350

choice = 0
right = 0
n = 0

for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(x, 36, 49, 1.5, (0, 0, 0), 0))

for i in range(5):
    spikes_list.append(spike_sheet.get_image(i, 135, 140, 0.1, (0, 0, 0), 0))

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

        key_down_event_list = pygame.event.get(pygame.KEYDOWN)

    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT] and scroll < 0:
        scroll += 5
        for rect in buildings:
            rect.move_ip(5)
        for thing in moving_platforms:
            thing.move_ip(5)
    
    if key[pygame.K_DOWN] and bg_y > -144:
        bg_y -= 3

    blit()

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= 100:
        framey += 1
        last_update = current_time
    if framey >= 5:
        framey = 1

    for x in range(0, 5000, 14):
        screen.blit(spikes_list[framey], (x + scroll, 587))

    buildings.update() 
    buildings.draw(screen)
    moving_platforms.draw(screen)

       
    for platfroms in moving_platforms:
        platfroms.move()
    
    if key[pygame.K_w] and scroll > -3850:
        scroll -= 5
        for rect in buildings:
            rect.move_ip(-5)
        for thing in moving_platforms:
            thing.move_ip(-5)
        if key[pygame.K_SPACE] == False:
            animation(4, 1, animation_list[frame], 90, 0, 7) 
    
    elif key[pygame.K_w] == False and key[pygame.K_SPACE] == False and key[pygame.K_s] == False\
        and key[pygame.K_v] == False and key[pygame.K_d] == False and key[pygame.K_b] == False:
        animation(0, 0, animation_list[frame], 90, 0, 7)
    
    if key[pygame.K_SPACE] and key[pygame.K_w]:
        animation(4, 2, animation_list[frame], 90, 8, 7)
    
    if key[pygame.K_s]:
        image_flip = pygame.transform.flip(animation_list[frame], True, False)
        image_flip.set_colorkey((0, 0, 0))
        dis -= 2
        animation(0, 1, image_flip, 90, 0, 7) 
    
    if key[pygame.K_SPACE]:
        animation(0, 2, animation_list[frame], 90, 8, 7)

    if key[pygame.K_v]:
        animation(0, 7, animation_list[frame], 130, 2, 7)
    
    if key[pygame.K_b]:      
        animation(1, 6, animation_list[frame], 200, 0, 7)
    
    if key[pygame.K_d]:
        animation(10, 3, animation_list[frame], 200, 0, 7)
    
    if left <= 5000:
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

    if high_height > low_height + 5:
        high_height = height_add + 50

    if left <= 5000:
        left += width_add

    pygame.display.update()

pygame.quit()
sys.exit()


