import pygame
import math
import sys

pygame.init()

# Okno - fullscreen
width, height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("The Labyrinth")
clock = pygame.time.Clock()

# Font pro zobrazení souřadnic 
font = pygame.font.SysFont(None, 30)

# Kostka
x = 100
y = 100     
size = 50
color = (102, 94, 58)

# Zdi
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

    # Vyčistit obrazovku
    screen.fill((93, 153, 37))

    # Nakreslení zdí
    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)
    
    # Nakreslení kostky
    pygame.draw.rect(screen, color, (int(x), int(y), size, size))

    # Zobrazení souřadnic vlevo nahoře
    player_text = f"Player: {int(x)}, {int(y)}"
    player_surf = font.render(player_text, True, (255, 255, 255))
    bg_width = player_surf.get_width() + 10
    bg_height = player_surf.get_height() + 10
    text_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    text_bg.fill((0, 0, 0, 180))
    screen.blit(text_bg, (10, 10))
    screen.blit(player_surf, (15, 13))

    pygame.display.flip()
    
    # fps limit
    clock.tick(60)

# Ukončení Hry přes klávesu ESC
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
pygame.quit()