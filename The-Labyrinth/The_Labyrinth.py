import pygame
import math
import sys

pygame.init()

# Okno - fullscreen
width, height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("The Labyrinth")
clock = pygame.time.Clock()

# Kostka
x = 100
y = 100
size = 50
color = (102, 94, 58)

# Walls
walls = [
    pygame.Rect(300, 200, 20, 200),
    pygame.Rect(500, 100, 200, 20),
    pygame.Rect(100, 400, 20, 200),
    pygame.Rect(700, 300, 20, 200),
    pygame.Rect(200, 500, 300, 20),
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Vyplnění pozadí
    screen.fill((38, 153, 83))
    
    # Získání pozice myši
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Pohyb kostky směrem k myši s kontrolou kolize
    dx = mouse_x - (x + size / 2)
    dy = mouse_y - (y + size / 2)
    distance = math.hypot(dx, dy)
    if distance > 0:
        speed = 5
        new_x = x + (dx / distance) * speed
        new_y = y + (dy / distance) * speed
        
        # Kontrola kolize se zdmi
        cube_rect = pygame.Rect(new_x, new_y, size, size)
        collision = False
        for wall in walls:
            if cube_rect.colliderect(wall):
                collision = True
                break
        if not collision:
            x, y = new_x, new_y
    
    # Nakreslení zdí
    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)
    
    # Nakreslení kostky
    pygame.draw.rect(screen, color, (x, y, size, size))


    pygame.display.flip()
    
    # fps limit
    clock.tick(60)

# Ukončení Hry
pygame.quit()
