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

# Font pro health
health_font = pygame.font.SysFont(None, 50)

# Kostka
x = 100
y = 100     
size = 50
color = (102, 94, 58)

# Enemy
enemy_x = 650
enemy_y = 650
enemy_size = 50
enemy_color = (161, 163, 145)
enemy_speed = 3

# Player health
player_health = 5

# Scalování mapy (zvětšení)
scale = 2.0 

# Kamera
zoom = 0.5 

camera_x = x - (width / 2) / zoom
camera_y = y - (height / 2) / zoom

# Kamera se pohybuje jen když je hráč blízko okraje
deadzone = 300 

# Zdi
walls = [
    pygame.Rect(int(300 * scale), int(200 * scale), int(20 * scale), int(200 * scale)),
    pygame.Rect(int(500 * scale), int(100 * scale), int(200 * scale), int(20 * scale)),
    pygame.Rect(int(100 * scale), int(400 * scale), int(20 * scale), int(200 * scale)),
    pygame.Rect(int(700 * scale), int(300 * scale), int(20 * scale), int(200 * scale)),
    pygame.Rect(int(200 * scale), int(500 * scale), int(300 * scale), int(20 * scale)),
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    # Získání pozice myši v okně (screen koordináty)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Převod pozice myši do světových souřadnic
    world_mouse_x = camera_x + mouse_x / zoom
    world_mouse_y = camera_y + mouse_y / zoom

    # Pohyb kostky směrem k myši (světové souřadnice) s kontrolou kolize
    dx = world_mouse_x - (x + size / 2)
    dy = world_mouse_y - (y + size / 2)
    distance = math.hypot(dx, dy)
    if distance > 0:
        speed = min(5, distance)  # Omezit rychlost, aby se nepřestřelilo přes cíl
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

    # Enemy pohyb k hráči
    dx_enemy = x - enemy_x
    dy_enemy = y - enemy_y
    distance_enemy = math.hypot(dx_enemy, dy_enemy)
    if distance_enemy > 0:
        speed_enemy = min(enemy_speed, distance_enemy)
        new_enemy_x = enemy_x + (dx_enemy / distance_enemy) * speed_enemy
        new_enemy_y = enemy_y + (dy_enemy / distance_enemy) * speed_enemy

        # Kontrola kolize se zdmi pro enemy
        enemy_rect = pygame.Rect(new_enemy_x, new_enemy_y, enemy_size, enemy_size)
        collision_enemy = False

        for wall in walls:
            if enemy_rect.colliderect(wall):
                collision_enemy = True
                break
        if not collision_enemy:
            enemy_x, enemy_y = new_enemy_x, new_enemy_y

    # Kolize s enemy
    if pygame.Rect(x, y, size, size).colliderect(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)):
        player_health = max(0, player_health - 1)
        # Reset enemy position
        enemy_x = 650
        enemy_y = 650
        if player_health == 0:

            # Respawn player
            player_health = 5
            x = 100
            y = 100
            enemy_x = 650
            enemy_y = 650

    # Kamera: posouvá se jen pokud je hráč blízko okraje
    player_screen_x = (x - camera_x) * zoom
    player_screen_y = (y - camera_y) * zoom

    left = deadzone
    right = width - deadzone
    top = deadzone
    bottom = height - deadzone

    if player_screen_x < left:
        camera_x = x - left / zoom
    elif player_screen_x > right:
        camera_x = x - right / zoom

    if player_screen_y < top:
        camera_y = y - top / zoom
    elif player_screen_y > bottom:
        camera_y = y - bottom / zoom

    # Vyčistit obrazovku
    screen.fill((93, 153, 37))

    # Nakreslení zdí
    for wall in walls:
        draw_x = (wall.x - camera_x) * zoom
        draw_y = (wall.y - camera_y) * zoom
        draw_width = wall.width * zoom
        draw_height = wall.height * zoom
        pygame.draw.rect(screen, (100, 100, 100), (int(draw_x), int(draw_y), int(draw_width), int(draw_height)))
    
    # Nakreslení kostky
    draw_x = (x - camera_x) * zoom
    draw_y = (y - camera_y) * zoom
    draw_size = size * zoom
    pygame.draw.rect(screen, color, (int(draw_x), int(draw_y), int(draw_size), int(draw_size)))

    # Nakreslení enemy
    enemy_draw_x = (enemy_x - camera_x) * zoom
    enemy_draw_y = (enemy_y - camera_y) * zoom
    enemy_draw_size = enemy_size * zoom
    pygame.draw.rect(screen, enemy_color, (int(enemy_draw_x), int(enemy_draw_y), int(enemy_draw_size), int(enemy_draw_size)))

    # Zobrazení souřadnic vlevo nahoře
    player_text = f"Player: {int(x)}, {int(y)}"
    player_surf = font.render(player_text, True, (255, 255, 255))

    bg_width = player_surf.get_width() + 10
    bg_height = player_surf.get_height() + 10

    text_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    text_bg.fill((0, 0, 0, 180))

    screen.blit(text_bg, (10, 10))
    screen.blit(player_surf, (15, 13))

    # Health display at bottom left
    health_text = f"Health: {'♥' * player_health}"
    health_surf = health_font.render(health_text, True, (255, 0, 0))
    health_bg = pygame.Surface((health_surf.get_width() + 10, health_surf.get_height() + 10), pygame.SRCALPHA)
    health_bg.fill((0, 0, 0, 180))
    screen.blit(health_bg, (10, height - health_bg.get_height() - 10))
    screen.blit(health_surf, (15, height - health_surf.get_height() - 8))

    pygame.display.flip()
    
    # fps limit
    clock.tick(60)

# Ukončení Hry přes klávesu ESC
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
pygame.quit()