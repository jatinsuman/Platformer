import pygame
import sys
import random

clock = pygame.time.Clock()

HEIGHT = 600
WIDTH = 900

bgY = -144

scroll = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_images = []

for i in range(0, 4):
    bg_image = pygame.image.load(f"drawingl{i}.png").convert_alpha()
    bg_images.append(bg_image)


def blit():
    for x in range(20):
        speed = 1
        for image in bg_images:
            screen.blit(image, ((x * 950) + scroll * speed , bgY))
            speed += 0.08
        

left = 0
rectangles = []

lowWidth = 20
highWidth = 250

lowHeight = 20
highHeight = 250

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll < 0 :
        scroll += 5
        for rect in rectangles:
            rect.move_ip(5, 0)
    if key[pygame.K_RIGHT]and scroll > -3850:
        scroll -= 5
        for rect in rectangles:
            rect.move_ip(-5, 0)
    if key[pygame.K_DOWN] and bgY > -144:
        bgY -= 3

    if left <=  900 - scroll:
        widthadd = random.randrange(lowWidth, highWidth)
        heightadd = random.randrange(lowHeight, highHeight)
        rectangles.append(pygame.Rect(left, HEIGHT - heightadd, widthadd, heightadd))
        highHeight = heightadd + 60


    blit()    


    for rect in rectangles:
        pygame.draw.rect(screen, (0, 0, 0), rect)

    if left <=  900 - scroll:
        left += widthadd/2    
        
    pygame.display.update()

pygame.quit()
sys.exit()
