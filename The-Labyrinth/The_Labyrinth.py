import pygame
import math
import sys
import random

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


# Mnohem větší Labyrinth Mapa (W = Zed', P = Hráč, E = Nepřítel, mezera = cesta)
maze_layout = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W P   W       W           W            W",
    "W WWW W WWWWW W WWWWWWWWW W WWWWWWWWWW W",
    "W W   W   W   W         W W W        W W",
    "W W WWWWW W WWWWWWWWWWW W W W WWWWWW W W",
    "W W     W W   W       W   W W W    W W W",
    "W WWWWW W WWW W WWWWW WWWWW W W WW W W W",
    "W     W W     W     W   W   W W W  W W W",
    "WWWWW W WWWWWWWWWWW WWW W WWW W WWWW W W",
    "W   W W           W   W W   W W      W W",
    "W W W WWWWWWWWWWW WWW W WWW W WWWWWWWW W",
    "W W W       W     W   W   W W W      W W",
    "W W WWWWWWW W WWWWW WWWWW W W W WWWW W W",
    "W W       W W W   W     W W W W W    W W",
    "W WWWWWWW W W W W WWWWW W W W W W WWWW W",
    "W W     W W W   W   W   W W   W W W  W W",
    "W W WWW W W WWWWWWW W WWW WWWWW W W  W W",
    "W   W   W W       W W   W       W    W W",
    "WWWWWWWWW WWWWWWW W WWW WWWWWWWWWWWW W W",
    "W       W       W W   W          W   W W",
    "WWWWWWW WWWWWWW W WWW WWWWWWWWWW W WWW W",
    "W     W       W W W       W      W   W W",
    "W WWW WWWWWWW W W W WWWWW W WWWWWWWW W W",
    "W   W       W   W   W     W          E W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# Player config
size = 50
color = (102, 94, 58)

# Enemy config
enemy_size = 50
enemy_color = (161, 163, 145)
enemy_speed = 3

# Player health
player_health = 5

# Zvětšení mapy
scale = 4.5 

block_size = int(50 * scale)
walls = []

# Default values just in case
start_x, start_y = 100, 100
start_enemy_x, start_enemy_y = 650, 650

for row_idx, row in enumerate(maze_layout):
    for col_idx, cell in enumerate(row):
        rect = pygame.Rect(
            int(col_idx * block_size), 
            int(row_idx * block_size), 
            block_size, 
            block_size
        )
        if cell == "W":
            walls.append(rect)
        elif cell == "P":
            start_x = int(col_idx * block_size + (block_size - size) / 2)
            start_y = int(row_idx * block_size + (block_size - size) / 2)
        elif cell == "E":
            start_enemy_x = int(col_idx * block_size + (block_size - enemy_size) / 2)
            start_enemy_y = int(row_idx * block_size + (block_size - enemy_size) / 2)

x, y = start_x, start_y
enemy_x, enemy_y = start_enemy_x, start_enemy_y

# Kamera
zoom = 0.5

camera_x = x - (width / 2) / zoom
camera_y = y - (height / 2) / zoom

# Kamera se pohybuje jen když je hráč blízko okraje
deadzone = 300 


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
 # Myš

    ## Získání pozice myši v okně
    mouse_x, mouse_y = pygame.mouse.get_pos()

    ## Převod pozice myši do světových souřadnic
    world_mouse_x = camera_x + mouse_x / zoom
    world_mouse_y = camera_y + mouse_y / zoom

    ## Pohyb kostky směrem k myši s kontrolou kolize
    dx = world_mouse_x - (x + size / 2)
    dy = world_mouse_y - (y + size / 2)
    distance = math.hypot(dx, dy)
    if distance > 0:
        speed = min(5, distance)
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

# Kolize s enemy

        ## Kontrola kolize se zdmi pro enemy
        enemy_rect = pygame.Rect(new_enemy_x, new_enemy_y, enemy_size, enemy_size)
        collision_enemy = False

        for wall in walls:
            if enemy_rect.colliderect(wall):
                collision_enemy = True
                break
        if not collision_enemy:
            enemy_x, enemy_y = new_enemy_x, new_enemy_y

    ## Kontrola kolize mezi hráčem a enemy
    if pygame.Rect(x, y, size, size).colliderect(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)):
        player_health = max(0, player_health - 1)

        ## Reset enemy pozici po zásahu
        enemy_x = start_enemy_x
        enemy_y = start_enemy_y
        if player_health == 0:
            death_messages = [
                "Death can have me, when it earns me.",
                "Wasted!",
                "Your adventure is done.",
                "The Labyrinth claims another victim.",
                "You Died",
                "Quit the game already",
                "You didn't survive."
            ]
            dead_text = random.choice(death_messages)
            dead_surf = font.render(dead_text, True, (200, 0, 0))
            dead_bg = pygame.Surface((dead_surf.get_width() + 20, dead_surf.get_height() + 20), pygame.SRCALPHA)
            dead_bg.fill((0, 0, 0, 200))
            screen.blit(dead_bg, ((width - dead_bg.get_width()) // 2, (height - dead_bg.get_height()) // 2))
            screen.blit(dead_surf, ((width - dead_surf.get_width()) // 2, (height - dead_surf.get_height()) // 2 + 10))
            pygame.display.flip()
            pygame.time.delay(2000)


            # Respawn player
            player_health = 5
            x = start_x
            y = start_y
            enemy_x = start_enemy_x
            enemy_y = start_enemy_y

    # Kamera se posouvá jen pokud je player blízko kraje
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

    # vyplnění obrazovky
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


    # --- FOG OF WAR (Zorné pole) ---
    vision_radius = 1200
    ray_step = 2  # Každé 2 stupně pro dobrý výkon a tvar
    
    fog_surf = pygame.Surface((width, height))
    fog_surf.fill((0, 0, 0)) # Černé pozadí zakrývající vše

    player_center_world_x = x + size / 2
    player_center_world_y = y + size / 2

    polygon_points = []
    
    # Filtrace zdí, které jsou dostatečně blízko
    walls_in_range = []
    for wall in walls:
        wall_center_x = wall.x + wall.width / 2
        wall_center_y = wall.y + wall.height / 2
        dist = math.hypot(player_center_world_x - wall_center_x, player_center_world_y - wall_center_y)
        if dist < vision_radius + wall.width:
            walls_in_range.append(wall)

    for angle in range(0, 360, ray_step):
        rad = math.radians(angle)
        end_x = player_center_world_x + math.cos(rad) * vision_radius
        end_y = player_center_world_y + math.sin(rad) * vision_radius
        
        ray_line = ((player_center_world_x, player_center_world_y), (end_x, end_y))
        
        closest_point = (end_x, end_y)
        closest_dist = vision_radius
        
        for wall in walls_in_range:
            clipped = wall.clipline(*ray_line)
            if clipped:
                point = clipped[0]
                dist = math.hypot(point[0] - player_center_world_x, point[1] - player_center_world_y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_point = point
                    
        # Pokud paprsek narazil do zdi, posuneme bod kousek dovnitř zdi,
        # aby byla vidět její přední strana, ale ne zem za ní.
        if closest_dist < vision_radius:
            if closest_dist > 0:
                dir_x = (closest_point[0] - player_center_world_x) / closest_dist
                dir_y = (closest_point[1] - player_center_world_y) / closest_dist
                push_amount = min(150, vision_radius - closest_dist)
                closest_point = (closest_point[0] + dir_x * push_amount, closest_point[1] + dir_y * push_amount)

        # Převod do souřadnic obrazovky
        screen_p_x = (closest_point[0] - camera_x) * zoom
        screen_p_y = (closest_point[1] - camera_y) * zoom
        polygon_points.append((screen_p_x, screen_p_y))

    if len(polygon_points) > 2:
        pygame.draw.polygon(fog_surf, (255, 255, 255), polygon_points)
        fog_surf.set_colorkey((255, 255, 255)) # Udělá bílou průhlednou
        
    # Nastavení průhlednosti mlhy (200 = tmavá, ale neúplně černá)
    fog_surf.set_alpha(200)

    screen.blit(fog_surf, (0, 0))
    # --- KONEC FOG OF WAR ---

    # Zobrazení souřadnic vlevo nahoře
    player_text = f"Player: {int(x)}, {int(y)}"
    player_surf = font.render(player_text, True, (255, 255, 255))

    bg_width = player_surf.get_width() + 10
    bg_height = player_surf.get_height() + 10

    text_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    text_bg.fill((0, 0, 0, 180))

    screen.blit(text_bg, (10, 10))
    screen.blit(player_surf, (15, 13))

    # Health display
    health_text = f"Health: {'♥ ' * player_health}"
    health_surf = health_font.render(health_text, True, (255, 0, 0))
    health_bg = pygame.Surface((health_surf.get_width() + 10, health_surf.get_height() + 10), pygame.SRCALPHA)
    health_bg.fill((0, 0, 0, 180))
    screen.blit(health_bg, (10, height - health_bg.get_height() - 10))
    screen.blit(health_surf, (15, height - health_surf.get_height() - 8))

#
    pygame.display.flip()
    
    # fps limit
    clock.tick(60)

# Ukončení Hry přes klávesu ESC
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
pygame.quit()