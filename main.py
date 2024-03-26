import pygame
import sys

clock = pygame.time.Clock()

HEIGHT = 600
WIDTH = 900

bgY = 0

scroll = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_images = []

for i in range(0, 4):
    bg_image = pygame.image.load(f"drawingl{i}.png").convert_alpha()
    bg_images.append(bg_image)


def blit():
    for x in range(5):
        speed = 1
        for image in bg_images:
            screen.blit(image, ((x * 950) + scroll * speed , bgY))
            speed += 0.08


running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll < 0 :
        scroll += 5
    if key[pygame.K_RIGHT]and scroll > -3850:
        scroll -= 5

    
    blit()
    
    
    pygame.display.update()

pygame.quit()
sys.exit()
