import pygame
import math
import sys
import random
import os

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


# Labyrinth Mapa (W = Zed, P = Hrač, E = enemy, mezera = cesta)
maze_layout = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W       W         W               W                        W",
    "W WWWWW W WWWWWWW W WWWWWWWWWWWWW W WWWWWWWWWWWWWWWWWWWWWW W",
    "W     W W       W W             W W                      W W",
    "WWWWW W WWWWWWW W WWWWW WWWWWWW W WWWWWWWWWWWWWWW WWWWWW W W",
    "W     W       W W     W W     W W               W W    W W W",
    "W WWWWWWWWWWW W WWWWW W W WWW W WWWWWWWWWWWWWWW W W WW W W W",
    "W           W W     W W W W   W       W       W W W  W W W W",
    "WWWWWWWWWWW W WWWWW WWW W WWWWWWWWWWW W WWWWW W W WWWW W W W",
    "W         W W           W       W   W W     W W W      W W W",
    "W WWWWWWW W WWWWWWWWWWWWW WWWWW W WWW W WWW W W WWWWWWWW W W",
    "W       W W       W       W   W       W   W W W          W W",
    "WWWWWWW W WWWWWWW W WWWWWWW W WWWWWWWWWWW W W W WWWWWWWWWW W",
    "W     W W W       W W       W           W W W W W        W W",
    "W WWW W W W WWWWW W W WWWWWWWWWWWWWWWWW W W W W W WWWWWW W W",
    "W   W W W W     W W W W                 W W   W W W    W W W",
    "W WWW W W WWWWW W W W W                 W WWWWW W WWWW W W W",
    "W   W W W       W W W W      P    E     W       W W    W W W",
    "WWWWW W WWWWWWWWW W W W                 W W WWWWW W WWWW W W",
    "W     W           W W W                 W W W     W      W W",
    "W WWWWWWWWWWWWWWWWW W WWWWWWWWWWWWWWWWWWW W W WWWWW WWWWWW W",
    "W                 W W                     W W W          W W",
    "W WWWWWWWWWWWWWWW W W WWWWWWWWWWWWWWWWWWW W W W WWWWWWWW W W",
    "W W             W W W W                   W W W W      W   W",
    "W W WWWWWWWWWWW W W W W WWWWWWWWWWWWWWWWW W W W W WWWW W W W",
    "W W           W W W W W                 W W W W W    W W W W",
    "W WWWWWWWWWWW W W W W W WWWWWWWWWWWWWWW W W W W WWWW W W W W",
    "W             W W W   W                 W   W        W   W W",
    "WWWWWWWWWWWWWWW W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW W",
    "W                                                          W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# Player config
size = 80
color = (29, 30, 66)

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

# Default values
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
zoom = 0.7

camera_x = x - (width / 2) / zoom
camera_y = y - (height / 2) / zoom

# Kamera se pohybuje jen když je hráč blízko okraje
deadzone = 300 

# --- Načtení textur ---
TEXTURES_DIR = os.path.join(os.path.dirname(__file__), "textures")

def get_texture(filename, default_color, size_tuple, pixelate_size=None):
    path = os.path.join(TEXTURES_DIR, filename)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            if pixelate_size:
                img = pygame.transform.scale(img, pixelate_size)
            return pygame.transform.scale(img, size_tuple)
        except Exception as e:
            print(f"Chyba při načítání {filename}: {e}")
            
    # Vytvoření fallback povrchu
    surf = pygame.Surface(size_tuple, pygame.SRCALPHA)
    surf.fill(default_color)
    return surf

wall_draw_size = math.ceil(block_size * zoom)
player_draw_size = math.ceil(size * zoom)
enemy_draw_size = math.ceil(enemy_size * zoom)

# Textura pro podlahu
floor_fallback = pygame.Surface((256, 256))
floor_fallback.fill((35, 109, 122))
if os.path.exists(os.path.join(TEXTURES_DIR, "floor.png")):
    try:
        floor_img = pygame.image.load(os.path.join(TEXTURES_DIR, "floor.png")).convert_alpha()
        
# Rozpixelování textur
        pixelated_floor = pygame.transform.scale(floor_img, (64, 64))
        floor_texture = pygame.transform.scale(pixelated_floor, (int(256 * zoom), int(256 * zoom)))
    except Exception as e:
        print(f"Error loading floor.png: {e}")
        floor_texture = floor_fallback
else:
    floor_texture = floor_fallback

floor_variations = [
    floor_texture,
    pygame.transform.flip(floor_texture, True, False),
    pygame.transform.flip(floor_texture, False, True),
    pygame.transform.flip(floor_texture, True, True)
]

textura_zed = get_texture("wall.png", (100, 100, 100), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))
textura_hrac = get_texture("player.png", color, (player_draw_size, player_draw_size))
textura_nepritel = get_texture("enemy.png", enemy_color, (enemy_draw_size, enemy_draw_size))
# --- Konec načtení textur ---


wobble_time = 0.0
wobble_amp = 0.0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Esc - Pause screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = True
                pause_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pause_surf.fill((0, 0, 0, 180))
                
                pause_font = pygame.font.SysFont(None, 100)
                small_font = pygame.font.SysFont(None, 50)
                
                pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
                resume_text = small_font.render("Press ESC to Resume", True, (200, 200, 200))
                quit_text = small_font.render("Press Q to Quit", True, (200, 200, 200))
                
                bg_copy = screen.copy()
                
                while paused:
                    for p_event in pygame.event.get():
                        if p_event.type == pygame.QUIT:
                            running = False
                            paused = False
                        if p_event.type == pygame.KEYDOWN:
                            if p_event.key == pygame.K_ESCAPE:
                                paused = False
                            if p_event.key == pygame.K_q:
                                running = False
                                paused = False
                    
                    if not running:
                        break
                    
                    screen.blit(bg_copy, (0, 0))
                    screen.blit(pause_surf, (0, 0))
                    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 100))
                    screen.blit(resume_text, (width // 2 - resume_text.get_width() // 2, height // 2 + 20))
                    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 80))
                    
                    pygame.display.flip()
                    clock.tick(60)
            
    if not running:
        break
    
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
    player_moved = False
    
    if distance > 1.0:
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
            player_moved = True

    if player_moved:
        wobble_amp = min(1.0, wobble_amp + 0.1)
        wobble_time += 0.15
    else:
        wobble_amp = max(0.0, wobble_amp - 0.1)
        if wobble_amp > 0:
            wobble_time += 0.30

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

    # Vykreslení podlahy s texturou (tiling loop)
    # Vyplníme pozadí pro případ, že něco ujede
    screen.fill((20, 20, 20))
    bg_w, bg_h = floor_texture.get_size()
    start_floor_x = -int(camera_x * zoom) % bg_w
    start_floor_y = -int(camera_y * zoom) % bg_h
    
    for fx in range(start_floor_x - bg_w, width, bg_w):
        for fy in range(start_floor_y - bg_h, height, bg_h):
            tile_x = int((camera_x * zoom + fx) // bg_w)
            tile_y = int((camera_y * zoom + fy) // bg_h)
            var_index = (tile_x * 374761393 ^ tile_y * 668265263) % len(floor_variations)
            screen.blit(floor_variations[var_index], (fx, fy))


    # Nakreslení zdí
    for wall in walls:
        draw_x = int((wall.x - camera_x) * zoom)
        draw_y = int((wall.y - camera_y) * zoom)
        screen.blit(textura_zed, (draw_x, draw_y))
    
    # Nakreslení kostky (hráče)
    draw_x = int((x - camera_x) * zoom)
    draw_y = int((y - camera_y) * zoom)
    
    if wobble_amp > 0:
        wobble = math.sin(wobble_time) * 0.15 * wobble_amp
        draw_w = int(player_draw_size * (1.0 - wobble))
        draw_h = int(player_draw_size * (1.0 + wobble))
        
        scaled_textura = pygame.transform.scale(textura_hrac, (draw_w, draw_h))
        offset_x = (player_draw_size - draw_w) // 2
        offset_y = player_draw_size - draw_h
        
        screen.blit(scaled_textura, (draw_x + offset_x, draw_y + offset_y))
    else:
        screen.blit(textura_hrac, (draw_x, draw_y))

    # Nakreslení enemy
    enemy_draw_x = int((enemy_x - camera_x) * zoom)
    enemy_draw_y = int((enemy_y - camera_y) * zoom)
    screen.blit(textura_nepritel, (enemy_draw_x, enemy_draw_y))


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
                    
        # Když paprsek narazí do zdi, posuneme vizi kousek do zdi
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
        
    # Nastavení průhlednosti mlhy
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

pygame.quit()