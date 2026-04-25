import pygame
import math
import sys
import random
import os

# Inicializace všech modulů Pygame (nutné před voláním jiných Pygame funkcí)
pygame.init()

# Nastavení okna hry
# Získáme rozlišení primárního monitoru
width, height = pygame.display.get_desktop_sizes()[0]
# Vytvoříme herní okno v režimu celé obrazovky s daným rozlišením
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
# Nastavíme titulek herního okna
pygame.display.set_caption("The Labyrinth")
# Vytvoříme objekt Clock pro řízení a omezování snímkové frekvence (FPS)
clock = pygame.time.Clock()

# Font pro zobrazení souřadnic v rohu obrazovky
font = pygame.font.SysFont(None, 30)

# Font pro zobrazení textů spojených se zdravím (pokud je potřeba)
health_font = pygame.font.SysFont(None, 50)

# Font pro obrazovku smrti (Game Over)
dead_font = pygame.font.SysFont(None, 100)

# Definice mapy bludiště (W = zeď, P = hráč, E = nepřítel, mezera = cesta, L = zamčená zeď)
maze_layout = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWLWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W       W         W               W                        W",
    "W WWWWW W WWWWWWW W WWWWWWWWWWWWW W WWWWWWWWWWWWWWWWWWWWWW W",
    "W     W W       W W             W W                      W W",
    "WWWWW W WWWWWWW W WWWWW WWWWWWW W WWWWWWWWWWWWWWW WWWWWW W W",
    "W     W       W W     W W     W W               W W    W W W",
    "W WWWWWWWWWWW W WWWWW W W WWW W W WWWWWWWWWWWWW W W WW W W W",
    "W           W W     W W W W   W       W       W W W  W W W W",
    "WWWWWWWWWWW W WWWWW WWW W WWWWWWW WWW W WWWWW W W WWWW W W W",
    "W         W W           W       W   W W     W W W      W W W",
    "W WWWWWWW W WWWWWWWWWWWWW WWWWW W WWW W WWW W W WWWWWWWW W W",
    "W       W W       W       W   W       W   W W W          W W",
    "WWWWWWW W WWWWWWW W WWWWWWW W WWW WWWWWWW W W W WWWWWWWWWW W",
    "W     W W W       W W       W           W W W W W        W W",
    "W WWW W W W WWWWW W W WWWWWWWWWWW WWWWW W W W W W WWWWWW W W",
    "W   W W W W     W W W W                 W W   W W W    W W W",
    "W WWW W W WWWWW W W W W      W          W WWWWW W WWWW W W W",
    "W   W W W       W W W W      P   KE     W       W W    W W W",
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

# Nastavení hráče
size = 80 # Velikost textury hráče
hitbox_size = 60 # Velikost kolizního obdélníku (hitboxu)
hitbox_offset = (size - hitbox_size) / 2 # Vystředění hitboxu
color = (29, 30, 66) # Výchozí barva (pokud chybí textura)

# Nastavení nepřítele
enemy_size = 50 # Velikost nepřátelského objektu
enemy_color = (161, 163, 145) # Výchozí barva nepřítele
enemy_speed = 3 # Počet pixelů, o které se nepřítel posune v každém snímku

# Zdraví hráče (počet srdcí/orbů)
player_health = 6

# Nastavení hry
brightness = 0  # 0-255, 0 = žádný světlý překryv (overlay)
target_fps = 120 # Cílová snímková frekvence
show_fps_counter = False # Přepínač pro zobrazení FPS

# Zvětšení mapy (měřítko bludiště)
scale = 4.5 

# Velikost jednoho bloku (zdi) vynásobená měřítkem
block_size = int(50 * scale)
walls = [] # Seznam pro uložení všech obyčejných zdí
locked_walls = [] # Seznam pro uložení zamčených zdí

inventory = [] # Inventář hráče (na začátku prázdný)
inventory_open = False # Stav, zda je zrovna otevřena obrazovka inventáře
items_on_ground = [] # Seznam předmětů ležících na mapě
pickup_notifications = [] # Seznam pro zobrazení sebraných předmětů v rohu obrazovky

# Default values (Výchozí startovní souřadnice pro případ, že na mapě chybí P a E)
start_x, start_y = 100, 100
start_enemy_x, start_enemy_y = 650, 650

# Procházení každého znaku v mapě (řádky a sloupce) pro tvorbu herního světa
for row_idx, row in enumerate(maze_layout):
    for col_idx, cell in enumerate(row):
        # Vytvoření objektu Rect pro danou buňku v mřížce
        rect = pygame.Rect(
            int(col_idx * block_size), 
            int(row_idx * block_size), 
            block_size, 
            block_size
        )
        if cell == "W":
            # Přidání klasické zdi do pole překážek
            walls.append(rect)
        elif cell == "L":
            # Přidání zamčené zdi (dveří) do pole
            locked_walls.append(rect)
        elif cell == "P":
            # Nastavení startovní pozice hráče (s ohledem na vycentrování postavy v bloku)
            start_x = int(col_idx * block_size + (block_size - size) / 2)
            start_y = int(row_idx * block_size + (block_size - size) / 2)
        elif cell == "E":
            # Nastavení startovní pozice nepřítele (s ohledem na vycentrování)
            start_enemy_x = int(col_idx * block_size + (block_size - enemy_size) / 2)
            start_enemy_y = int(row_idx * block_size + (block_size - enemy_size) / 2)
        elif cell == "K":
            # Umístění klíče doprostřed bloku na mapě
            item_x = int(col_idx * block_size + block_size / 2)
            item_y = int(row_idx * block_size + block_size / 2)
            items_on_ground.append({'type': 'Key', 'x': item_x, 'y': item_y})

# Přiřazení počátečních hodnot aktuálním souřadnicím
x, y = start_x, start_y
enemy_x, enemy_y = start_enemy_x, start_enemy_y

# Nastavení kamery
zoom = 0.7 # Úroveň přiblížení (méně než 1 oddaluje, více než 1 přibližuje)

# Vypočtení pozice kamery tak, aby hráč začínal uprostřed obrazovky
camera_x = x - (width / 2) / zoom
camera_y = y - (height / 2) / zoom

# Mrtvá zóna (Deadzone) - Kamera se nebude posouvat, dokud hráč nevyjde z této vzdálenosti od středu
deadzone = 300 

# --- Načtení textur ---
# Získání správné cesty ke složce "textures", ať se skript spouští odkudkoliv
TEXTURES_DIR = os.path.join(os.path.dirname(__file__), "textures")

def get_texture(filename, default_color, size_tuple, pixelate_size=None):
    # Funkce pro načtení textury ze souboru s možností záložní barvy (pokud soubor chybí)
    path = os.path.join(TEXTURES_DIR, filename)
    if os.path.exists(path):
        try:
            # Načteme obrázek a zachováme jeho průhlednost (alpha kanál)
            img = pygame.image.load(path).convert_alpha()
            if pixelate_size:
                # Záměrně obrázek nejdříve zmenšíme, aby vznikl retro pixel artový efekt
                img = pygame.transform.scale(img, pixelate_size)
            # Nakonec obrázek přizpůsobíme požadované velikosti a vrátíme
            return pygame.transform.scale(img, size_tuple)
        except Exception as e:
            # Vypíšeme chybu do konzole, pokud se obrázek nepodaří načíst správně
            print(f"Chyba při načítání {filename}: {e}")
            
    # Pokud soubor neexistuje nebo nastala chyba, vytvoříme náhradní obdélník s výchozí barvou
    surf = pygame.Surface(size_tuple, pygame.SRCALPHA)
    surf.fill(default_color)
    return surf

# Výpočet vykreslovacích rozměrů objektů podle aktuálního přiblížení (zoomu)
wall_draw_size = math.ceil(block_size * zoom)
player_draw_size = math.ceil(size * zoom)
enemy_draw_size = math.ceil(enemy_size * zoom)

# Nastavení textury pro podlahu a záložního řešení (když textura chybí)
floor_fallback = pygame.Surface((256, 256))
floor_fallback.fill((35, 109, 122)) # Tmavě modrozelená barva podlahy
if os.path.exists(os.path.join(TEXTURES_DIR, "floor.png")):
    try:
        floor_img = pygame.image.load(os.path.join(TEXTURES_DIR, "floor.png")).convert_alpha()
        
        # Zmenšením na 64x64 a zvětšením vytvoříme pixelový vzhled (retro styl)
        pixelated_floor = pygame.transform.scale(floor_img, (64, 64))
        # Následně ji upravíme podle aktuálního přiblížení
        floor_texture = pygame.transform.scale(pixelated_floor, (int(256 * zoom), int(256 * zoom)))
    except Exception as e:
        print(f"Error loading floor.png: {e}")
        floor_texture = floor_fallback
else:
    floor_texture = floor_fallback

# Varianty podlahy pro vizuální rozmanitost (aby podlaha nepůsobila jednotvárně, vytvoříme zrcadlové kopie textury)
floor_variations = [
    floor_texture,
    pygame.transform.flip(floor_texture, True, False), # Převráceno zleva doprava
    pygame.transform.flip(floor_texture, False, True), # Převráceno shora dolů
    pygame.transform.flip(floor_texture, True, True)   # Převráceno v obou osách
]

# Načtení konkrétních textur do proměnných (s využitím naší bezpečné funkce)
textura_zed = get_texture("wall.png", (100, 100, 100), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))
textura_zamcena_zed = get_texture("locked_wall.png", (139, 69, 19), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))
textura_hrac = get_texture("player.png", color, (player_draw_size, player_draw_size))
textura_nepritel = get_texture("enemy.png", enemy_color, (enemy_draw_size, enemy_draw_size))
textura_klic_icon = get_texture("key.png", (255, 215, 0), (50, 50))
textura_slime_orb = get_texture("slime_orb.png", (0, 188, 212), (30, 30))
textura_slime_orb_eyes = get_texture("slime_orb_eyes.png", (33, 150, 243), (50, 50))
# --- Konec načtení textur ---

# Vytvoření předvykresleného povrchu pro bludiště (optimalizace pro zvýšení plynulosti hry)
# Místo vykreslování každé zdi zvlášť každý snímek, vykreslíme všechny zdi jednou na tento velký "papír"
maze_width = len(maze_layout[0]) * wall_draw_size
maze_height = len(maze_layout) * wall_draw_size
maze_surface = pygame.Surface((maze_width, maze_height), pygame.SRCALPHA)

# Vykreslení obyčejných zdí na předpřipravený povrch (maze_surface)
for wall in walls:
    surf_x = int(wall.x * zoom)
    surf_y = int(wall.y * zoom)
    maze_surface.blit(textura_zed, (surf_x, surf_y))

# Vykreslení zamčených zdí (dveří) na předpřipravený povrch
for l_wall in locked_walls:
    surf_x = int(l_wall.x * zoom)
    surf_y = int(l_wall.y * zoom)
    maze_surface.blit(textura_zamcena_zed, (surf_x, surf_y))

# Proměnné pro animaci pohybu (pohupování postavičky, když jde)
wobble_time = 0.0
wobble_amp = 0.0
particles = [] # Seznam pro vizuální efekty při pohybu postavy

# Vytvoření povrchů pro prachové částice (pro podporu průhlednosti)
dust_surfaces = []
for i in range(10):
    radius = random.uniform(1, 2.5)
    surf_size = int(radius * 2) + 2
    surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
    alpha = random.randint(30, 80)
    color = (random.randint(150, 200), random.randint(150, 200), random.randint(130, 180), alpha)
    pygame.draw.circle(surf, color, (surf_size // 2, surf_size // 2), radius)
    dust_surfaces.append((surf, surf_size // 2))

# Ambient dust particles
ambient_dust = []
for _ in range(150):
    ambient_dust.append({
        'x': random.uniform(0, width),
        'y': random.uniform(0, height),
        'speed_y': random.uniform(-0.4, -0.1),
        'wobble_offset': random.uniform(0, math.pi * 2),
        'wobble_speed': random.uniform(0.5, 1.5),
        'surf_idx': random.randint(0, len(dust_surfaces)-1)
    })

running = True

# Hlavní herní smyčka
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Esc - Pause screen & Inventory screen ("B")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                inventory_open = True
                inv_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                inv_surf.fill((0, 0, 0, 230))
                
                inv_font = pygame.font.SysFont(None, 100)
                item_font = pygame.font.SysFont(None, 50)
                
                bg_copy = screen.copy()
                
                while inventory_open:
                    for i_event in pygame.event.get():
                        if i_event.type == pygame.QUIT:
                            running = False
                            inventory_open = False
                        if i_event.type == pygame.KEYDOWN:
                            if i_event.key == pygame.K_b or i_event.key == pygame.K_ESCAPE:
                                inventory_open = False
                    
                    if not running:
                        break
                    
                    screen.blit(bg_copy, (0, 0))
                    screen.blit(inv_surf, (0, 0))
                    
                    title = inv_font.render("INVENTORY", True, (255, 255, 255))
                    screen.blit(title, (width // 2 - title.get_width() // 2, 100))
                    
                    start_y = 250
                    for i, item in enumerate(inventory):
                        if item == "Key":
                            text = item_font.render("- Golden Key", True, (255, 215, 0))
                            screen.blit(text, (width // 2 - 150, start_y + i * 80))
                            screen.blit(textura_klic_icon, (width // 2 - 220, start_y + i * 80 - 10))
                    
                    if len(inventory) == 0:
                        empty_text = item_font.render("Your inventory is empty...", True, (150, 150, 150))
                        screen.blit(empty_text, (width // 2 - empty_text.get_width() // 2, start_y))
                        
                    pygame.display.flip()
                    clock.tick(60)

            if event.key == pygame.K_SPACE:
                # Mechanika sbírání předmětů
                pickup_range = 150 # Dosah pro sebrání předmětu
                player_cx = x + size / 2
                player_cy = y + size / 2
                for item in items_on_ground[:]:
                    # Kontrola vzdálenosti hráče od předmětu
                    if math.hypot(player_cx - item['x'], player_cy - item['y']) <= pickup_range:
                        inventory.append(item['type'])
                        # Přidáme oznámení o sebrání do seznamu (s aktuálním časem pro postupné zmizení)
                        pickup_notifications.append({
                            'type': item['type'],
                            'time': pygame.time.get_ticks() / 1000.0,
                            'alpha': 255
                        })
                        items_on_ground.remove(item)
                        break # Najednou sebere jen jeden předmět

            if event.key == pygame.K_ESCAPE:
                paused = True
                pause_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pause_surf.fill((0, 0, 0, 180))
                
                pause_font = pygame.font.SysFont(None, 100)
                small_font = pygame.font.SysFont(None, 50)
                
                pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
                resume_text = small_font.render("Press ESC to Resume", True, (200, 200, 200))
                quit_text = small_font.render("Press Q to Quit", True, (200, 200, 200))
                settings_text = small_font.render("Press S for Settings", True, (200, 200, 200))
                
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
                            if p_event.key == pygame.K_s:
                                # Open settings
                                settings_open = True
                                settings_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                                settings_surf.fill((0, 0, 0, 200))
                                
                                settings_font = pygame.font.SysFont(None, 80)
                                option_font = pygame.font.SysFont(None, 40)
                                
                                settings_title = settings_font.render("SETTINGS", True, (255, 255, 255))
                                brightness_text = option_font.render(f"Brightness: {brightness}", True, (255, 255, 255))
                                fps_text = option_font.render(f"FPS: {target_fps}", True, (255, 255, 255))
                                fps_counter_text = option_font.render(f"FPS Counter: {'ON' if show_fps_counter else 'OFF'}", True, (255, 255, 255))
                                back_text = option_font.render("Press ESC to go back", True, (200, 200, 200))
                                brightness_hint = option_font.render("Use LEFT/RIGHT arrows to adjust brightness", True, (150, 150, 150))
                                fps_hint = option_font.render("Use UP/DOWN arrows to adjust FPS", True, (150, 150, 150))
                                fps_counter_hint = option_font.render("Press SPACE to toggle FPS counter", True, (150, 150, 150))
                                
                                while settings_open:
                                    for s_event in pygame.event.get():
                                        if s_event.type == pygame.QUIT:
                                            running = False
                                            settings_open = False
                                            paused = False
                                        if s_event.type == pygame.KEYDOWN:
                                            if s_event.key == pygame.K_ESCAPE:
                                                settings_open = False
                                            elif s_event.key == pygame.K_LEFT:
                                                brightness = max(0, brightness - 10)
                                                brightness_text = option_font.render(f"Brightness: {brightness}", True, (255, 255, 255))
                                            elif s_event.key == pygame.K_RIGHT:
                                                brightness = min(255, brightness + 10)
                                                brightness_text = option_font.render(f"Brightness: {brightness}", True, (255, 255, 255))
                                            elif s_event.key == pygame.K_UP:
                                                target_fps = min(240, target_fps + 10)
                                                fps_text = option_font.render(f"FPS: {target_fps}", True, (255, 255, 255))
                                            elif s_event.key == pygame.K_DOWN:
                                                target_fps = max(30, target_fps - 10)
                                                fps_text = option_font.render(f"FPS: {target_fps}", True, (255, 255, 255))
                                            elif s_event.key == pygame.K_SPACE:
                                                show_fps_counter = not show_fps_counter
                                                fps_counter_text = option_font.render(f"FPS Counter: {'ON' if show_fps_counter else 'OFF'}", True, (255, 255, 255))
                                    
                                    if not running:
                                        break
                                    
                                    screen.blit(bg_copy, (0, 0))
                                    screen.blit(settings_surf, (0, 0))
                                    screen.blit(settings_title, (width // 2 - settings_title.get_width() // 2, 100))
                                    screen.blit(brightness_text, (width // 2 - brightness_text.get_width() // 2, 250))
                                    screen.blit(brightness_hint, (width // 2 - brightness_hint.get_width() // 2, 300))
                                    screen.blit(fps_text, (width // 2 - fps_text.get_width() // 2, 400))
                                    screen.blit(fps_hint, (width // 2 - fps_hint.get_width() // 2, 450))
                                    screen.blit(fps_counter_text, (width // 2 - fps_counter_text.get_width() // 2, 500))
                                    screen.blit(fps_counter_hint, (width // 2 - fps_counter_hint.get_width() // 2, 550))
                                    screen.blit(back_text, (width // 2 - back_text.get_width() // 2, height - 100))
                                    
                                    pygame.display.flip()
                                    clock.tick(60)
                    
                    if not running:
                        break
                    
                    screen.blit(bg_copy, (0, 0))
                    screen.blit(pause_surf, (0, 0))
                    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 100))
                    screen.blit(resume_text, (width // 2 - resume_text.get_width() // 2, height // 2 + 20))
                    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 80))
                    screen.blit(settings_text, (width // 2 - settings_text.get_width() // 2, height // 2 + 140))
                    
                    pygame.display.flip()
                    clock.tick(60)
            
    if not running:
        break
    
 # Ovládání myší

    ## Získání aktuální pozice kurzoru myši na obrazovce (v pixelech okna)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    ## Převod pozice kurzoru na obrazovce do herního světa (podle toho, kde je zrovna kamera)
    world_mouse_x = camera_x + mouse_x / zoom
    world_mouse_y = camera_y + mouse_y / zoom

    ## Výpočet směru a vzdálenosti pohybu hráče (kostky) k myši
    dx = world_mouse_x - (x + size / 2)
    dy = world_mouse_y - (y + size / 2)
    distance = math.hypot(dx, dy) # Přepona pravoúhlého trojúhelníku (celková vzdálenost)
    player_moved = False # Proměnná sledující, zda se hráč v tomto snímku pohnul
    
    if distance > 1.0: # Pokud nejsme přesně na myši, budeme se pohybovat
        speed = min(5, distance) # Omezíme rychlost na maximálně 5 pixelů (aby hráč nevyletěl moc rychle)
        move_x = (dx / distance) * speed # Posun v ose X
        move_y = (dy / distance) * speed # Posun v ose Y

        # Pohyb a kontrola kolize (nárazu do zdi) v horizontálním směru (osa X)
        new_x = x + move_x
        # Vytvoření dočasného obdélníku pro zjištění kolize na nové pozici
        cube_rect_x = pygame.Rect(new_x + hitbox_offset, y + hitbox_offset, hitbox_size, hitbox_size)
        # Zkontrolujeme, zda tento obdélník nekoliduje s jakoukoliv pevnou zdí
        collision_x = cube_rect_x.collidelist(walls) != -1
                
        if not collision_x:
            # Pokud nekolidujeme se zdí, zkontrolujeme kolizi se zamčenými dveřmi
            if cube_rect_x.collidelist(locked_walls) != -1:
                if "Key" in inventory and running:
                    # Pokud máme klíč, vyhráváme hru!
                    win_font = pygame.font.SysFont(None, 100)
                    win_text = win_font.render("YOU ESCAPED", True, (255, 215, 0))
                    win_bg = pygame.Surface((width, height), pygame.SRCALPHA)
                    win_bg.fill((0, 0, 0, 220)) # Tmavý poloprůhledný podklad
                    screen.blit(win_bg, (0, 0))
                    screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - 50))
                    pygame.display.flip() # Vykreslíme vítěznou obrazovku
                    pygame.time.delay(4000) # Počkáme 4 sekundy
                    running = False # Ukončíme hru
                collision_x = True # Pokud klíč nemáme, dveře fungují jako zeď

        # Pokud nedošlo k žádné kolizi, provedeme pohyb
        if not collision_x:
            x = new_x
            player_moved = True

        # Pohyb a kontrola kolize ve vertikálním směru (osa Y)
        new_y = y + move_y
        cube_rect_y = pygame.Rect(x + hitbox_offset, new_y + hitbox_offset, hitbox_size, hitbox_size)
        collision_y = cube_rect_y.collidelist(walls) != -1
                
        if not collision_y:
            if cube_rect_y.collidelist(locked_walls) != -1:
                if "Key" in inventory and running:
                    # Odemčení dveří i při nárazu shora nebo zespodu
                    win_font = pygame.font.SysFont(None, 100)
                    win_text = win_font.render("YOU ESCAPED", True, (255, 215, 0))
                    win_bg = pygame.Surface((width, height), pygame.SRCALPHA)
                    win_bg.fill((0, 0, 0, 220))
                    screen.blit(win_bg, (0, 0))
                    screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - 50))
                    pygame.display.flip()
                    pygame.time.delay(4000)
                    running = False
                collision_y = True

        if not collision_y:
            y = new_y
            player_moved = True

    # Pokud se hráč pohnul, přidáme částice (efekt chůze) a zvýšíme pohupování
    if player_moved:
        wobble_amp = min(1.0, wobble_amp + 0.1) # Postupně zvyšujeme sílu pohupování do maxima 1.0
        wobble_time += 0.15 # Zvyšujeme časovač pro sinusovou funkci (rychlost pohupování)
        
        # Náhodně vytvoříme 1 až 2 částice prachu/jisker za hráčem
        for _ in range(random.randint(1, 2)):
            particles.append({
                'x': x + size / 2 + random.uniform(-size / 3, size / 3), # Náhodná pozice blízko středu hráče
                'y': y + size / 2 + random.uniform(-size / 3, size / 3),
                'radius': random.uniform(3, 7), # Velikost částice
                'color': (random.randint(0, 50), random.randint(150, 220), random.randint(220, 255)), # Modravá barva
                'life': random.randint(10, 20), # Jak dlouho částice "žije" (zmizí)
                'dx': random.uniform(-0.5, 0.5), # Náhodný horizontální rozptyl
                'dy': random.uniform(-1.0, 0) # Náhodný vertikální rozptyl (spíše nahoru)
            })
    else:
        # Pokud hráč stojí, postupně utlumíme pohupování
        wobble_amp = max(0.0, wobble_amp - 0.1)
        if wobble_amp > 0:
            wobble_time += 0.30 # Necháme doznívat animaci

    # --- Umělá inteligence nepřítele (Enemy AI) ---
    # Nepřítel se neustále snaží dostat přímo k hráči (jednoduché pronásledování)
    dx_enemy = x - enemy_x
    dy_enemy = y - enemy_y
    distance_enemy = math.hypot(dx_enemy, dy_enemy) # Vzdálenost mezi hráčem a nepřítelem
    if distance_enemy > 0:
        speed_enemy = min(enemy_speed, distance_enemy)
        move_x_enemy = (dx_enemy / distance_enemy) * speed_enemy
        move_y_enemy = (dy_enemy / distance_enemy) * speed_enemy

        # Pohyb nepřítele a kolize se zdmi (Osa X)
        new_enemy_x = enemy_x + move_x_enemy
        enemy_rect_x = pygame.Rect(new_enemy_x, enemy_y, enemy_size, enemy_size)
        collision_enemy_x = enemy_rect_x.collidelist(walls) != -1 or enemy_rect_x.collidelist(locked_walls) != -1
        
        if not collision_enemy_x:
            enemy_x = new_enemy_x

        # Pohyb nepřítele a kolize se zdmi (Osa Y)
        new_enemy_y = enemy_y + move_y_enemy
        enemy_rect_y = pygame.Rect(enemy_x, new_enemy_y, enemy_size, enemy_size)
        collision_enemy_y = enemy_rect_y.collidelist(walls) != -1 or enemy_rect_y.collidelist(locked_walls) != -1
        
        if not collision_enemy_y:
            enemy_y = new_enemy_y

    ## Kontrola kolize (dotyku) mezi hráčem a nepřítelem
    if pygame.Rect(x + hitbox_offset, y + hitbox_offset, hitbox_size, hitbox_size).colliderect(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)):
        player_health = max(0, player_health - 1) # Hráč ztrácí jeden život

        ## Po zásahu se nepřítel resetuje na svou původní startovní pozici
        enemy_x = start_enemy_x
        enemy_y = start_enemy_y
        
        # Pokud hráči dojdou životy, zobrazí se obrazovka smrti
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
            dead_surf = dead_font.render(dead_text, True, (115, 110, 110))
            dead_bg = pygame.Surface((width, height), pygame.SRCALPHA)
            dead_bg.fill((0, 0, 0, 220))
            screen.blit(dead_bg, (0, 0))
            screen.blit(dead_surf, ((width - dead_surf.get_width()) // 2, (height - dead_surf.get_height()) // 2))
            pygame.display.flip()
            pygame.time.delay(2000)


            # Respawn player
            player_health = 6
            x = start_x
            y = start_y
            enemy_x = start_enemy_x
            enemy_y = start_enemy_y

    # --- Aktualizace kamery ---
    # Kamera se posouvá jen pokud je hráč blízko okraje obrazovky (mimo mrtvou zónu)
    player_screen_x = (x - camera_x) * zoom
    player_screen_y = (y - camera_y) * zoom

    # Hranice na obrazovce, za kterými se kamera začne hýbat
    left = deadzone
    right = width - deadzone
    top = deadzone
    bottom = height - deadzone

    # Posun kamery v ose X
    if player_screen_x < left:
        camera_x = x - left / zoom
    elif player_screen_x > right:
        camera_x = x - right / zoom

    # Posun kamery v ose Y
    if player_screen_y < top:
        camera_y = y - top / zoom
    elif player_screen_y > bottom:
        camera_y = y - bottom / zoom

    # --- Vykreslování (Rendering) ---
    
    # Vyčištění obrazovky temnou barvou (pozadí mimo mapu)
    screen.fill((20, 20, 20))
    
    # Vykreslení podlahy s dlaždicováním (tiling) textury (aby se podlaha opakovala do nekonečna)
    bg_w, bg_h = floor_texture.get_size()
    # Zajišťuje plynulý posun podlahy vzhledem ke kameře
    start_floor_x = -int(camera_x * zoom) % bg_w
    start_floor_y = -int(camera_y * zoom) % bg_h
    
    for fx in range(start_floor_x - bg_w, width, bg_w):
        for fy in range(start_floor_y - bg_h, height, bg_h):
            tile_x = int((camera_x * zoom + fx) // bg_w)
            tile_y = int((camera_y * zoom + fy) // bg_h)
            # Deterministický výběr náhodné varianty textury podlahy pomocí bitových operací
            var_index = (tile_x * 374761393 ^ tile_y * 668265263) % len(floor_variations)
            screen.blit(floor_variations[var_index], (fx, fy))

    # Vykreslení předvykresleného bludiště (všech zdí naráz)
    surf_left = int(camera_x * zoom)
    surf_top = int(camera_y * zoom)
    # Zkopírujeme jen tu část obří mapy, kterou kamera aktuálně vidí
    visible_rect = (surf_left, surf_top, width, height)
    screen.blit(maze_surface, (0, 0), visible_rect)
    
    # Vykreslení předmětů na zemi (efekt jiskřivých pixelů)
    curr_t = pygame.time.get_ticks() / 1000.0
    for item in items_on_ground:
        item_dx = int((item['x'] - camera_x) * zoom)
        item_dy = int((item['y'] - camera_y) * zoom)
        
        # Kontrola, zda je předmět zhruba na obrazovce, abychom nevykreslovali zbytečnosti
        if -50 < item_dx < width + 50 and -50 < item_dy < height + 50:
            # Výpočet plynulého pulzování (velikost jiskry se mění v čase)
            pulse = (math.sin(curr_t * 8 + item['x']) + 1) / 2 # Hodnota mezi 0.0 a 1.0
            sparkle_rad = max(4, int(12 * pulse * zoom)) # Zvětšený poloměr jiskry
            
            # Zlatá barva pro klíč, světle modrá pro ostatní případné předměty
            color_outer = (255, 215, 0) if item['type'] == "Key" else (200, 255, 255)
            
            # Nakreslení vnějšího lesku a vnitřního jasného bodu (jádra jiskry)
            pygame.draw.circle(screen, color_outer, (item_dx, item_dy), sparkle_rad)
            pygame.draw.circle(screen, (255, 255, 255), (item_dx, item_dy), max(2, int(sparkle_rad * 0.4)))

    # Update a vykreslení částic
    active_particles = []
    for p in particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['life'] -= 0.5
        p['radius'] -= 0.15
        if p['life'] > 0 and p['radius'] > 0:
            active_particles.append(p)
            
            p_draw_x = int((p['x'] - camera_x) * zoom)
            p_draw_y = int((p['y'] - camera_y) * zoom)
            p_draw_radius = max(1, int(p['radius'] * zoom))
            pygame.draw.circle(screen, p['color'], (p_draw_x, p_draw_y), p_draw_radius)
    particles = active_particles

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

    # --- Zjištění viditelnosti pro enemy ---
    vision_radius = 2000
    player_center_world_x = x + size / 2
    player_center_world_y = y + size / 2
    enemy_center_world_x = enemy_x + enemy_size / 2
    enemy_center_world_y = enemy_y + enemy_size / 2

    enemy_visible = False
    dist_to_enemy = math.hypot(player_center_world_x - enemy_center_world_x, player_center_world_y - enemy_center_world_y)
    
    if dist_to_enemy <= vision_radius:
        los_rect = pygame.Rect(min(player_center_world_x, enemy_center_world_x), 
                               min(player_center_world_y, enemy_center_world_y), 
                               abs(player_center_world_x - enemy_center_world_x), 
                               abs(player_center_world_y - enemy_center_world_y))
        los_rect.inflate_ip(100, 100)
        los_walls = [w for w in walls if los_rect.colliderect(w)] + [w for w in locked_walls if los_rect.colliderect(w)]

        check_points = [
            (enemy_center_world_x, enemy_center_world_y),
            (enemy_x, enemy_y),
            (enemy_x + enemy_size, enemy_y),
            (enemy_x, enemy_y + enemy_size),
            (enemy_x + enemy_size, enemy_y + enemy_size)
        ]
        
        for pt in check_points:
            los_line = ((player_center_world_x, player_center_world_y), pt)
            pt_visible = True
            for wall in los_walls:
                if wall.clipline(*los_line):
                    pt_visible = False
                    break
            
            if pt_visible:
                enemy_visible = True
                break

    # Nakreslení enemy
    if enemy_visible:
        enemy_draw_x = int((enemy_x - camera_x) * zoom)
        enemy_draw_y = int((enemy_y - camera_y) * zoom)
        screen.blit(textura_nepritel, (enemy_draw_x, enemy_draw_y))


    # --- FOG OF WAR (Mlha války / Zorné pole) ---
    # Implementace Raycastingu, který zjistí, kam až hráč "vidí"
    ray_step = 2  # Paprsek vysíláme každé 2 stupně, což zajišťuje dobrou kvalitu i výkon
    
    # Vytvoření povrchu, který zakryje celou obrazovku tmou
    fog_surf = pygame.Surface((width, height))
    fog_surf.fill((0, 0, 0)) # Černé pozadí (absolutní tma)

    player_center_world_x = x + size / 2
    player_center_world_y = y + size / 2

    polygon_points = [] # Seznam bodů, které tvoří viditelnou část oblasti
    
    # Rychlá optimalizace: Před samotným vysíláním paprsků si vyfiltrujeme jen ty zdi, 
    # které jsou vůbec v dosahu zraku (abychom nepočítali kolize pro celou mapu)
    vision_rect = pygame.Rect(player_center_world_x - vision_radius, player_center_world_y - vision_radius, vision_radius * 2, vision_radius * 2)
    walls_in_range = [wall for wall in walls if vision_rect.colliderect(wall)] + [wall for wall in locked_walls if vision_rect.colliderect(wall)]

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

    # --- AMBIENT DUST ---
    current_time_dust = pygame.time.get_ticks() / 1000.0
    for dust in ambient_dust:
        dust['y'] += dust['speed_y']
        
        wobble = math.sin(current_time_dust * dust['wobble_speed'] + dust['wobble_offset']) * 0.3
        dust['x'] += wobble
        
        # Wrap around screen
        if dust['x'] < 0: dust['x'] = width
        if dust['x'] > width: dust['x'] = 0
        if dust['y'] < 0: dust['y'] = height
        if dust['y'] > height: dust['y'] = 0
        
        surf, offset = dust_surfaces[dust['surf_idx']]
        screen.blit(surf, (int(dust['x']) - offset, int(dust['y']) - offset))
    # --- KONEC AMBIENT DUST ---

    # --- Vykreslování uživatelského rozhraní (HUD) ---

    # Zobrazení aktuálních souřadnic hráče vlevo nahoře
    player_text = f"Player: {int(x)}, {int(y)}"
    player_surf = font.render(player_text, True, (255, 255, 255)) # Vykreslení textu bílou barvou

    bg_width = player_surf.get_width() + 10
    bg_height = player_surf.get_height() + 10

    # Poloprůhledné černé pozadí pod textem, aby byl čitelný
    text_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    text_bg.fill((0, 0, 0, 180))

    screen.blit(text_bg, (10, 10))
    screen.blit(player_surf, (15, 13))

    # Zobrazení zdraví hráče (animované orby)
    orb_spacing = 35
    icon_width = 50
    padding = 10
    
    # Výpočet šířky pozadí pro zdraví podle toho, kolik orbů zbývá
    total_health_width = icon_width + padding + ((player_health - 1) * orb_spacing) if player_health > 1 else icon_width
    bg_width = total_health_width + padding * 2
    bg_height = 50 + padding * 2
    
    health_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    health_bg.fill((0, 0, 0, 180))
    health_bg_y = height - bg_height - 10
    
    screen.blit(health_bg, (10, health_bg_y))

    # Slizový orb s očima (reprezentuje poslední život)
    if player_health > 0:
        eyes_x = 10 + padding
        eyes_y = health_bg_y + padding
        
        # Pokud zbývá jen 1 život, orb s očima se začne třást (efekt strachu/nízkého zdraví)
        if player_health == 1:
            shake_x = random.randint(-5, 5)
            shake_y = random.randint(-5, 5)
            eyes_x += shake_x
            eyes_y += shake_y
            
        screen.blit(textura_slime_orb_eyes, (eyes_x, eyes_y))

    # Animované slizové orby (představují zbylé životy navíc)
    current_time = pygame.time.get_ticks() / 1000.0 # Získání aktuálního času v sekundách pro animace
    for i in range(max(0, player_health - 1)):
        # Každý orb má mírně posunutý čas animace, aby se nevlnily všechny úplně stejně
        anim_time = current_time * 5 + (i * 0.8) 
        squish = math.sin(anim_time) * 0.15 # Vytvoření efektu natahování a smršťování
        
        orb_w = max(1, int(30 * (1.0 + squish)))
        orb_h = max(1, int(30 * (1.0 - squish)))
        
        # Změna velikosti textury podle vypočítaného natažení
        scaled_orb = pygame.transform.scale(textura_slime_orb, (orb_w, orb_h))
        
        # Zarovnání orbu na střed po jeho smrštění/natažení
        offset_x = (30 - orb_w) // 2
        offset_y = (30 - orb_h) // 2
        bob_y = math.cos(anim_time) * 4 # Pohyb orbu jemně nahoru a dolů (levitace)
        
        draw_x = 10 + padding + icon_width + padding + (i * orb_spacing) + offset_x
        draw_y = health_bg_y + padding + 10 + bob_y + offset_y
        
        screen.blit(scaled_orb, (draw_x, draw_y)) # Vykreslení konkrétního orbu

    # --- Zobrazení notifikací o sebrání předmětů ---
    notif_y = height - 80 # Výchozí Y pozice v pravém dolním rohu
    active_notifications = []
    
    for notif in pickup_notifications:
        time_alive = current_time - notif['time']
        
        # Oznámení zůstane na obrazovce 3 sekundy
        if time_alive < 3.0:
            # Postupné blednutí (fade out) během poslední sekundy
            if time_alive > 2.0:
                notif['alpha'] = max(0, int(255 * (3.0 - time_alive)))
                
            # Připravíme text
            item_name = "Golden Key" if notif['type'] == "Key" else notif['type']
            notif_text = health_font.render(f"+ {item_name}", True, (255, 215, 0) if notif['type'] == "Key" else (255, 255, 255))
            notif_text.set_alpha(notif['alpha'])
            
            # Pozadí pro notifikaci
            bg_width = notif_text.get_width() + 80 # Místo i pro ikonu
            bg_height = max(50, notif_text.get_height() + 20)
            notif_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            notif_bg.fill((0, 0, 0, int(180 * (notif['alpha'] / 255.0))))
            
            # Vykreslení notifikace (od pravého okraje)
            draw_x = width - bg_width - 20
            
            screen.blit(notif_bg, (draw_x, notif_y))
            if notif['type'] == "Key":
                # Přidáme ikonu klíče a upravíme její průhlednost
                icon_copy = textura_klic_icon.copy()
                icon_copy.set_alpha(notif['alpha'])
                screen.blit(icon_copy, (draw_x + 10, notif_y + (bg_height - 50) // 2))
                
            screen.blit(notif_text, (draw_x + 70, notif_y + (bg_height - notif_text.get_height()) // 2))
            
            # Posuneme Y pozici pro další oznámení (aby se řadily nad sebe)
            notif_y -= (bg_height + 10)
            active_notifications.append(notif)
            
    pickup_notifications = active_notifications

    # Zobrazení počítadla FPS (Snímků za sekundu), pokud je zapnuté v nastavení
    if show_fps_counter:
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
        fps_bg = pygame.Surface((fps_text.get_width() + 10, fps_text.get_height() + 10), pygame.SRCALPHA)
        fps_bg.fill((0, 0, 0, 180))
        screen.blit(fps_bg, (width - fps_text.get_width() - 20, 10))
        screen.blit(fps_text, (width - fps_text.get_width() - 15, 13))

    # Brightness overlay (Překrytí obrazovky bílou barvou pro zvýšení jasu přes nastavení)
    if brightness > 0:
        brightness_overlay = pygame.Surface((width, height))
        brightness_overlay.fill((255, 255, 255))
        brightness_overlay.set_alpha(brightness) # Nastavení úrovně průhlednosti bílé plochy
        screen.blit(brightness_overlay, (0, 0))

    # Tato funkce vezme vše, co jsme během snímku nakreslili do paměti a plácne to na monitor naráz
    pygame.display.flip()
    
    # Omezovač FPS - zajišťuje, že hra nepoběží rychleji než na určený cíl (target_fps)
    clock.tick(target_fps)

# Když se smyčka ukončí (running = False), bezpečně vypneme pygame okno
pygame.quit()