import pygame    # Hlavní knihovna pro tvorbu her
import math      # Matematické funkce (sinus, hypotenusa atd.)
import sys       # Systémové funkce (ukončení programu)
import random    # Generování náhodných čísel
import os        # Práce se soubory a složkami
import json      # Práce s formátem JSON (ukládání pozic)
import copy      # Pro hluboké kopírování objektů

# Inicializace všech modulů Pygame (nutné před voláním jiných Pygame funkcí)
pygame.init()

# Nastavení okna hry
# Získáme rozlišení primárního monitoru
width, height = pygame.display.get_desktop_sizes()[0]
# Vytvoříme herní okno v režimu celé obrazovky s daným rozlišením
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
# Nastavíme titulek herního okna
pygame.display.set_caption("The Labyrinth")
# Skryjeme systémový kurzor a nahradíme ho vlastním
pygame.mouse.set_visible(False)
# Vytvoříme objekt Clock pro řízení a omezování snímkové frekvence (FPS)
clock = pygame.time.Clock()

# Fonty pro různé části hry
font = pygame.font.SysFont(None, 30)
health_font = pygame.font.SysFont(None, 50)
dead_font = pygame.font.SysFont(None, 100)
pause_font = pygame.font.SysFont(None, 110)
btn_font = pygame.font.SysFont(None, 54)
menu_title_font = pygame.font.SysFont(None, 140)
option_font = pygame.font.SysFont(None, 40)


# Definice mapy bludiště (W = zeď, P = hráč, E = nepřítel, mezera = cesta, L = zamčená zeď, B = rozbitelná zeď)
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
    "W   W W W W     W W W W   D             W W   W W W    W W W",
    "W WWW W W WWWWW W W W W R  K WE W       W WWWWW W WWWW W W W",
    "W   W W W       W W W W  HX  PF   E     W       W W    W W W",
    "WWWWW W WWWWWWWWW W W W  W  S W         W W WWWWW W WWWW W W",
    "W     W           W W W   G     C       W W W     W      W W",
    "W WWWWWWWWWWWWWWWWW W WWWWWWWWWWWWWWWWWWW W W WWWWW WWWWWW W",
    "W                 W W                     W W W          W W",
    "W WWWWWWWWWWWWWWW W W WWWWWWWWWWWWWWWWWWW W W W WWWWWWWW W W",
    "W W             W W W W                   W W W W      W   W",
    "W W WWWWWWWWWWW W W W W WWWWWWWWWWWWWWWWW W W W W WWWW W W W",
    "W W      W     W   W W W                 W W W W W    W W W W",
    "W        W     W   W W W WWWWWWWWWWWWWWW W W W W WWWW W W W W",
    "W        W     WWW W   W                 W   W        W     W",
    "WWWWWWW WWWWWWW    WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW W",
    "W                                                           W",
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
show_hitboxes = False # Přepínač pro zobrazení hitboxů

# Zvětšení mapy (měřítko bludiště)
scale = 4.5 

# Velikost jednoho bloku (zdi) vynásobená měřítkem
block_size = int(50 * scale)
walls = [] # Seznam pro uložení všech obyčejných zdí
locked_walls = [] # Seznam pro uložení zamčených zdí

inventory = [] # Inventář hráče (na začátku prázdný)
current_weapon = None       # Aktuálně vybavená zbraň (None, 'Sword', 'Spear', 'Scythe')
unlocked_weapons = []       # Seznam odemčených zbraní hráče
inventory_open = False # Stav, zda je zrovna otevřena obrazovka inventáře
items_on_ground = [] # Seznam předmětů ležících na mapě
pickup_notifications = [] # Seznam pro zobrazení sebraných předmětů v rohu obrazovky
healing_platforms = [] # Seznam léčivých platforem (checkpointů)
healing_platform_glow = [] # Aktivní animace záblesku při aktivaci léčivé platformy
decorations = []      # Seznam dekorací v labyrintu (krystaly, pavučiny, atd.)
atmospheric_motes = [] # Plovoucí prachové částice pro atmosféru

# Systém útoků
is_attacking = False
attack_timer = 0
attack_duration = 15 # Trvání útoku v počtu snímků
attack_angle = 0    # Úhel zamknutý při zahájení útoku
player_invincibility_timer = 0 # Timer nesmrtelnosti po zásahu

# Systém nepřátel
enemies = []        # Seznam všech aktivních nepřátel
max_enemy_hp = 4

# Systém dashe hráče
player_dash_timer = 0
player_dash_cooldown = 0
player_is_dashing = False
player_dash_x, player_dash_y = 0, 0
DASH_COOLDOWN_TIME = 60 # Počet snímků mezi dashi (cca 0.75s při 120fps)
DASH_DURATION = 5      # Trvání dashe v počtu snímků (zkráceno pro větší dynamiku)
DASH_SPEED_MULT = 6.5   # Násobek rychlosti při dashi (zvýšeno pro větší rychlost)

# Systém léčení hráče
mana_charges = 0 # Počet mana nabití (sdílené pro heal a slime blast)
MAX_MANA_CHARGES = 3 # Maximální počet nabití man
healing_in_progress = False # Je nyní aktivní léčení
healing_timer = 0 # Jak dlouho se hráč léčí
healing_duration = 80 # Trvání léčení (80 snímků = 1 sekunda při 120fps)
healing_speed_multiplier = 0.4 # Hráč se pohybuje 40% normální rychlostí během léčení
healing_per_charge = 1 # Kolik životů se uzdraví za jedno nabití (při 6 životech)
charge_per_enemy_hit = 0.3 # Kolik nabití se přidá za zásah nepřítele

# Systém rozbitelných zdí
breakable_walls = [] # Seznam rozbitelných zdí s jejich HP

# Systém slime blast schopnosti
slime_blast_projectiles = [] # Seznam aktivních slime blast projektilů
slime_blast_available = False # Má hráč schopnost slime blast
SLIME_BLAST_RANGE = 600 # Dosah projektilu
SLIME_BLAST_SPEED = 12 # Rychlost projektilu
SLIME_BLAST_SIZE = 20 # Velikost projektilu
SLIME_BLAST_DAMAGE = 1000 # Damage dealt to enemies by slime blast

# Systém pro detekci držení F klávesy
f_key_pressed = False # Zda je F klávesa stisknuta
f_key_press_time = 0 # Čas kdy byla F klávesa stisknuta
HOLD_THRESHOLD = 20 # Počet snímků (cca 0.167s při 120fps) pro rozlišení mezi press a hold
# Slime blast cooldown (milliseconds)
SLIME_BLAST_COOLDOWN_MS = 1000
slime_blast_last_cast = -10000
# Secret easter egg flag (toggled by hidden top-right click)
show_big_message = False

# Default values (Výchozí startovní souřadnice pro případ, že na mapě chybí P)
start_x, start_y = 100, 100

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
        elif cell == "B":
            # Přidání rozbitelné zdi do pole
            breakable_walls.append({
                'rect': rect,
                'hp': 3,  # Počet zásahů potřebných k rozbití
                'max_hp': 3
            })
        elif cell == "P":
            # Nastavení startovní pozice hráče (s ohledem na vycentrování postavy v bloku)
            start_x = int(col_idx * block_size + (block_size - size) / 2)
            start_y = int(row_idx * block_size + (block_size - size) / 2)
        elif cell == "E":
            # Původně nastavovalo startovní pozici pro jednoho nepřítele, nyní řešeno v reset_game_world
            pass
        elif cell == "H":
            # Umístění léčivé platformy (checkpoint) na pozici bloku v mapě
            hp_rect = pygame.Rect(
                int(col_idx * block_size), # X souřadnice levého horního rohu
                int(row_idx * block_size), # Y souřadnice levého horního rohu
                block_size,                # Šířka bloku
                block_size                 # Výška bloku
            )
            healing_platforms.append(hp_rect) # Přidání do seznamu platforem

# --- Herní stav (Global variables) ---
current_save_slot = None # Aktuálně vybraný slot pro ukládání
last_saved_platform_idx = -1 # ID poslední platformy, kde se ukládalo

def reset_game_world():
    """Resetuje všechny herní proměnné na výchozí hodnoty pro novou hru."""
    global x, y, enemies, player_health, inventory, items_on_ground
    global pickup_notifications, healing_platform_glow, checkpoint_x, checkpoint_y
    global camera_x, camera_y, wobble_time, wobble_amp, particles
    global current_weapon, unlocked_weapons
    global player_dash_timer, player_dash_cooldown, player_is_dashing
    global start_x, start_y
    global mana_charges, healing_in_progress, healing_timer
    global breakable_walls, slime_blast_projectiles, slime_blast_available

    # Reset parametrů
    player_health = 6
    inventory = []
    current_weapon = None
    unlocked_weapons = []
    pickup_notifications = []
    healing_platform_glow = []
    wobble_time = 0.0
    wobble_amp = 0.0
    particles = []
    mana_charges = 0
    healing_in_progress = False
    healing_timer = 0
    slime_blast_projectiles = []
    slime_blast_available = True  # Hráč začíná se schopností slime blast
    
    walls.clear()
    locked_walls.clear()
    breakable_walls.clear()
    items_on_ground.clear()
    enemies.clear()
    healing_platforms.clear()
    decorations.clear()
    atmospheric_motes.clear()

    # Procházení každého znaku v mapě (Single Pass)
    for row_idx, row in enumerate(maze_layout):
        for col_idx, cell in enumerate(row):
            rx, ry = int(col_idx * block_size), int(row_idx * block_size)
            rect = pygame.Rect(rx, ry, block_size, block_size)

            if cell == "W":
                walls.append(rect)
                # Dekorace na zdech
                if random.random() < 0.15:
                    decorations.append({'type': 'Vine', 'x': rx + random.randint(0, block_size-64), 'y': ry + random.randint(0, block_size-64), 'angle': random.choice([0, 90, 180, 270])})
            elif cell == "L":
                locked_walls.append(rect)
            elif cell == "B":
                # Přidání rozbitelné zdi
                breakable_walls.append({
                    'rect': rect,
                    'hp': 3,
                    'max_hp': 3
                })
            elif cell == "P":
                x = int(rx + (block_size - size) / 2)
                y = int(ry + (block_size - size) / 2)
                start_x, start_y = x, y
                checkpoint_x, checkpoint_y = x, y
            elif cell == "H":
                healing_platforms.append(rect)
            elif cell == "K":
                items_on_ground.append({'type': 'Key', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == "E":
                ex, ey = rx + (block_size - enemy_size) // 2, ry + (block_size - enemy_size) // 2
                enemies.append({'x': ex, 'y': ey, 'start_x': ex, 'start_y': ey, 'hp': max_enemy_hp, 'type': 'Fly', 'dash_timer': 0, 'dash_cooldown': 0, 'is_dashing': False, 'dash_x': 0, 'dash_y': 0, 'buzz_offset': random.uniform(0, 100), 'respawn_timer': 0, 'knockback_x': 0, 'knockback_y': 0})
            elif cell == "G":
                ex, ey = rx + (block_size - enemy_size) // 2, ry + (block_size - enemy_size) // 2
                enemies.append({'x': ex, 'y': ey, 'start_x': ex, 'start_y': ey, 'hp': max_enemy_hp, 'type': 'Seeker', 'respawn_timer': 0, 'knockback_x': 0, 'knockback_y': 0})
            elif cell == "S":
                items_on_ground.append({'type': 'Glitter Slime Ball', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == "X":
                # Slime Blast upgrade item placed on map (press SPACE to pick up)
                items_on_ground.append({'type': 'Slime Blast', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == "D":
                items_on_ground.append({'type': 'Sword', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == "R":
                items_on_ground.append({'type': 'Spear', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == "C":
                items_on_ground.append({'type': 'Scythe', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == "F":
                items_on_ground.append({'type': 'Feather', 'x': rx + block_size // 2, 'y': ry + block_size // 2})
            elif cell == " ":
                # Dekorace na podlaze
                if random.random() < 0.04:
                    c_type = random.choice(['Blue', 'Purple', 'Teal'])
                    # Aktualizované barvy záře pro modré varianty
                    if c_type == 'Blue':
                        c_color = (0, 100, 255)
                    elif c_type == 'Purple': # Nyní Blue Light
                        c_color = (111, 169, 209)
                    else: # Nyní Blue Dark
                        c_color = (0, 83, 194)
                    
                    decorations.append({
                        'type': 'Crystal', 
                        'subtype': c_type,
                        'color': c_color,
                        'x': rx + random.randint(15, block_size-47), 
                        'y': ry + random.randint(15, block_size-47),
                        'pulse_offset': random.uniform(0, math.pi * 2)
                    })
                elif random.random() < 0.06:
                    is_near_wall = any(maze_layout[row_idx+dr][col_idx+dc] == "W" for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)] if 0 <= row_idx+dr < len(maze_layout) and 0 <= col_idx+dc < len(maze_layout[0]))
                    if is_near_wall:
                        decorations.append({'type': 'Cobweb', 'x': rx + random.randint(0, block_size-64), 'y': ry + random.randint(0, block_size-64)})

    # Inicializace atmosférického prachu
    for _ in range(120):
        atmospheric_motes.append({
            'x': random.uniform(0, len(maze_layout[0]) * block_size),
            'y': random.uniform(0, len(maze_layout) * block_size),
            'speed': random.uniform(0.2, 0.6),
            'radius': random.uniform(1.5, 4),
            'wobble': random.uniform(0, math.pi * 2),
            'alpha': random.randint(40, 120)
        })

    player_dash_timer = player_dash_cooldown = 0
    player_is_dashing = False
    camera_x = x - (width / 2) / zoom
    camera_y = y - (height / 2) / zoom

def save_game(slot_id, slot_name=None):
    """Uloží aktuální stav hry do JSON souboru."""
    if slot_id is None: return # Pokud není vybrán slot, nic se neukládá
    
    # Pokud slot_name není zadán (při automatickém ukládání), pokusíme se ho zachovat z existujícího uložení
    if slot_name is None:
        existing = load_save_info(slot_id)
        slot_name = existing['name'] if existing else f"Slot {slot_id}"

    # Vytvoření slovníku se všemi daty k uložení
    save_data = {
        "name": slot_name,               # Jméno slotu zobrazené v menu
        "player_x": x,                   # Pozice X hráče
        "player_y": y,                   # Pozice Y hráče
        "enemies": enemies,              # Seznam nepřátel
        "player_health": player_health,  # Aktuální životy
        "inventory": inventory,          # Seznam věcí v inventáři
        "current_weapon": current_weapon,         # Aktuálně vybavená zbraň
        "unlocked_weapons": unlocked_weapons,     # Odemčené zbraně
        "checkpoint_x": checkpoint_x,    # Poslední uložený checkpoint X
        "checkpoint_y": checkpoint_y,    # Poslední uložený checkpoint Y
        "items_on_ground": items_on_ground, # Zbývající věci na zemi v bludišti
        "camera_x": camera_x,            # Pozice kamery X
        "camera_y": camera_y,            # Pozice kamery Y
        "slime_blast_available": slime_blast_available,  # Má hráč slime blast
        "mana_charges": mana_charges       # Sdílené nabití (mana) pro slime blast a heal
    }
    
    # Cesta k souboru (uloženo ve složce "saves")
    path = os.path.join(os.path.dirname(__file__), "saves", f"save_{slot_id}.json")
    try:
        # Zápis do souboru ve formátu JSON s kódováním UTF-8
        with open(path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
        print(f"Hra uložena do slotu {slot_id}")
    except Exception as e:
        # Vypíše chybu, pokud se zápis nepovede (např. chybějící oprávnění)
        print(f"Chyba při ukládání: {e}")

def load_game(slot_id):
    """Načte kompletní stav hry z JSON souboru."""
    global x, y, enemies, player_health, inventory, items_on_ground
    global checkpoint_x, checkpoint_y, camera_x, camera_y, current_save_slot
    global current_weapon, unlocked_weapons
    global slime_blast_available, mana_charges
    
    # Cesta k souboru uložené pozice
    path = os.path.join(os.path.dirname(__file__), "saves", f"save_{slot_id}.json")
    if not os.path.exists(path):
        return False # Pokud soubor neexistuje, načítání selže
        
    try:
        # Otevření a přečtení JSON dat
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Přiřazení načtených hodnot globálním proměnným hry
        x = data["player_x"]
        y = data["player_y"]
        enemies = data.get("enemies", [])
        player_health = data["player_health"]
        inventory = data["inventory"]
        current_weapon = data.get("current_weapon", None)
        unlocked_weapons = data.get("unlocked_weapons", [])
        checkpoint_x = data["checkpoint_x"]
        checkpoint_y = data["checkpoint_y"]
        items_on_ground = data["items_on_ground"]
        camera_x = data["camera_x"]
        camera_y = data["camera_y"]
        slime_blast_available = data.get("slime_blast_available", True)
        mana_charges = data.get("mana_charges", 0)
        
        # Nastavení aktuálně aktivního slotu
        current_save_slot = slot_id
        return True # Úspěšně načteno
    except Exception as e:
        # Vypíše chybu při poškození souboru nebo nesprávném formátu
        print(f"Chyba při načítání: {e}")
        return False

def load_save_info(slot_id):
    """Načte pouze základní informace o uložené hře (pro zobrazení v menu)."""
    path = os.path.join(os.path.dirname(__file__), "saves", f"save_{slot_id}.json")
    if not os.path.exists(path):
        return None # Slot je prázdný
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) # Vrátí data jako slovník
    except:
        return None # Chyba při čtení

def delete_save(slot_id):
    """Smaže soubor s uloženou hrou daného slotu."""
    path = os.path.join(os.path.dirname(__file__), "saves", f"save_{slot_id}.json")
    if os.path.exists(path):
        os.remove(path) # Odstranění souboru z disku


# Přiřazení počátečních hodnot aktuálním souřadnicím
x, y = start_x, start_y

# Checkpoint - léčivá platforma uloží poslední bezpečnou pozici hráče
checkpoint_x, checkpoint_y = start_x, start_y

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

def get_texture(filename, default_color, size_tuple, pixelate_size=None, colorkey=None):
    # Funkce pro načtení textury ze souboru s možností záložní barvy (pokud soubor chybí)
    path = os.path.join(TEXTURES_DIR, filename)
    if os.path.exists(path):
        try:
            # Načtení obrázku
            raw_img = pygame.image.load(path)
            if colorkey:
                # Pro barvu klíče (colorkey) je lepší použít convert() bez alpha kanálu
                img = raw_img.convert()
                img.set_colorkey(colorkey)
            else:
                # Pro zachování průhlednosti (alpha kanál) použijeme convert_alpha()
                img = raw_img.convert_alpha()

            if pixelate_size:
                # Záměrně obrázek nejdříve zmenšíme, aby vznikl retro pixel artový efekt
                img = pygame.transform.scale(img, pixelate_size)
            # Nakonec obrázek přizpůsobíme požadované velikosti v pixelech a vrátíme
            return pygame.transform.scale(img, size_tuple)
        except Exception as e:
            # Vypíšeme chybu do konzole, pokud se obrázek nepodaří načíst správně
            print(f"Chyba při načítání {filename}: {e}")
            
    # Pokud soubor neexistuje nebo nastala chyba, vytvoříme náhradní plochu s výchozí barvou
    surf = pygame.Surface(size_tuple, pygame.SRCALPHA)
    surf.fill(default_color)
    return surf

def create_crystal_texture(size, color_base):
    """Vytvoří texturu zářícího krystalu s danou základní barvou."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    r, g, b = color_base
    glow_col = (max(0, r-50), max(0, g-50), max(0, b-50))
    core_col = (min(255, r+100), min(255, g+100), min(255, b+100))
    
    pts = [(size//2, 2), (size-2, size//2), (size//2, size-2), (2, size//2)]
    pygame.draw.polygon(surf, glow_col, pts)
    pygame.draw.polygon(surf, core_col, [(size//2, 4), (size-4, size//2), (size//2, size-4), (4, size//2)], 2)
    pygame.draw.circle(surf, (255, 255, 255), (size//2, size//2), 2)
    return surf

def create_vine_texture(size):
    """Vytvoří texturu popínavých rostlin."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for _ in range(5):
        start = (random.randint(0, size), random.randint(0, size))
        end = (random.randint(0, size), random.randint(0, size))
        pygame.draw.line(surf, (20, 60, 40), start, end, 2)
        pygame.draw.circle(surf, (30, 80, 50), end, 3)
    return surf

def create_cobweb_texture(size):
    """Vytvoří texturu pavučiny."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size//2, size//2)
    color = (150, 150, 160, 100)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        end = (center[0] + math.cos(rad) * size//2, center[1] + math.sin(rad) * size//2)
        pygame.draw.line(surf, color, center, end, 1)
    for r in range(4, size//2, 6):
        prev_pt = None
        for angle in range(0, 361, 45):
            rad = math.radians(angle)
            curr_pt = (center[0] + math.cos(rad) * r, center[1] + math.sin(rad) * r)
            if prev_pt:
                pygame.draw.line(surf, color, prev_pt, curr_pt, 1)
            prev_pt = curr_pt
    return surf

def create_pixel_weapon(weapon_type, size=96): # Zvětšená základní plocha pro delší zbraně
    """Procedurálně vytvoří pixel-artovou zbraň v modré barvě s průhledným pozadím."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    glow_color = (100, 200, 255)
    core_color = (200, 240, 255)
    handle_color = (40, 60, 100)
    
    px = size // 16 # Větší pixely pro 96x96 plochu
    
    if weapon_type == 'Sword':
        # Delší čepel (Blade) - range 3 až 13
        for i in range(2, 13):
            pygame.draw.rect(surf, glow_color, (7.2*px, i*px, 1.6*px, px))
            pygame.draw.rect(surf, core_color, (7.6*px, i*px, 0.8*px, px))
        # Záštita a jílec
        pygame.draw.rect(surf, handle_color, (5.5*px, 13*px, 5*px, px))
        pygame.draw.rect(surf, handle_color, (7.6*px, 14*px, 0.8*px, 2*px))
        
    elif weapon_type == 'Spear':
        # Silnější rukojeť a hrot (Revert thin change)
        for i in range(6, 15):
            pygame.draw.rect(surf, handle_color, (7.5*px, i*px, px, px))
        # Silnější hrot (Spearhead)
        pygame.draw.rect(surf, glow_color, (7*px, 4*px, 2*px, 2*px))
        pygame.draw.rect(surf, core_color, (7.5*px, 3*px, px, 3*px))
        pygame.draw.rect(surf, glow_color, (7.5*px, 2*px, px, px))
        
    elif weapon_type == 'Scythe':
        # Větší zahnutá čepel
        for i in range(4, 15):
            pygame.draw.rect(surf, handle_color, (7.6*px, i*px, 0.8*px, px))
        # Velká kosa čepel
        for i in range(2, 9):
            pygame.draw.rect(surf, glow_color, (i*px, 4*px, px, 2*px))
            pygame.draw.rect(surf, core_color, (i*px, 4.5*px, px, px))
        pygame.draw.rect(surf, glow_color, (1*px, 5*px, px, px))

    return surf

    return surf

def create_bug_texture(size):
    """Procedurálně vytvoří pixel-artovou mouchu (nepřítele)."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    px = size // 10
    
    # Křídla (zadní vrstva, poloprůhledná)
    wing_color = (180, 220, 255, 120)
    pygame.draw.ellipse(surf, wing_color, (2*px, 0*px, 4*px, 3*px)) # Horní křídlo
    pygame.draw.ellipse(surf, wing_color, (2*px, 7*px, 4*px, 3*px)) # Dolní křídlo

    # Tělo (tmavě modrá/černá)
    body_color = (30, 30, 50)
    pygame.draw.ellipse(surf, body_color, (2*px, 3*px, 7*px, 4*px))
    
    # Detail na zádech (stínování)
    pygame.draw.ellipse(surf, (50, 50, 80), (3*px, 4*px, 4*px, 2*px))

    # Oči (zářivě tyrkysová, aby to sedělo do Labyrintu)
    eye_color = (100, 255, 255)
    pygame.draw.circle(surf, eye_color, (int(8.5*px), int(4.2*px)), px//2 + 1)
    pygame.draw.circle(surf, eye_color, (int(8.5*px), int(5.8*px)), px//2 + 1)
    
    # Nožičky (drobné výčnělky)
    leg_color = (20, 20, 40)
    pygame.draw.line(surf, leg_color, (4*px, 3*px), (3*px, 1*px), 2)
    pygame.draw.line(surf, leg_color, (6*px, 3*px), (7*px, 1*px), 2)
    pygame.draw.line(surf, leg_color, (4*px, 7*px), (3*px, 9*px), 2)
    pygame.draw.line(surf, leg_color, (6*px, 7*px), (7*px, 9*px), 2)
        
    return surf

def create_feather_texture(size):
    """Procedurálně vytvoří pixel-artové pírko ve stylu Glitter Ballu."""
    pixel_size = 16
    temp_surf = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)
    
    color_main = (240, 245, 255)
    color_shadow = (180, 200, 230)
    color_accent = (100, 200, 255)
    
    # Brko (střed)
    for i in range(4, 12):
        temp_surf.set_at((i, 15-i), color_shadow)
    
    # Vějíř pírka
    vane_pixels = [
        (5,9), (5,8), (6,8), (6,7), (7,7), (7,6), (8,6), (8,5), (9,5), (9,4), (10,4), (10,3),
        (7,11), (8,11), (8,10), (9,10), (9,9), (10,9), (10,8), (11,8), (11,7)
    ]
    for p in vane_pixels:
        temp_surf.set_at(p, color_main)

    # Akcenty/stíny
    temp_surf.set_at((8,8), color_accent)
    temp_surf.set_at((6,10), color_accent)
    temp_surf.set_at((10,5), color_shadow)

    # Zvětšení s pixelovým efektem
    final_surf = pygame.transform.scale(temp_surf, (size, size))
    
    # Ambientní záře
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(glow, (150, 220, 255, 40), (size//2, size//2), size//2)
    final_surf.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
    return final_surf

def create_seeker_texture(size):
    """Procedurálně vytvoří pixel-artový Seeker - agresivního nepřítele se špičkami."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    px = size // 10
    
    # Hlavní koule těla (grayish-blue)
    body_color = (80, 120, 160)
    pygame.draw.circle(surf, body_color, (size//2, size//2), int(3.5*px))
    
    # Vnitřní stínování
    shadow_color = (50, 80, 0)
    pygame.draw.circle(surf, shadow_color, (size//2 - px, size//2 - px), int(2.5*px))
    
    # Ostré špičky kolem těla (8 hrotů)
    spike_color = (100, 140, 180)
    spike_length = int(2*px)
    center_x = size // 2
    center_y = size // 2
    base_radius = int(4*px)
    
    for i in range(8):
        angle = (i * 45) * math.pi / 180
        start_x = int(center_x + math.cos(angle) * base_radius)
        start_y = int(center_y + math.sin(angle) * base_radius)
        end_x = int(center_x + math.cos(angle) * (base_radius + spike_length))
        end_y = int(center_y + math.sin(angle) * (base_radius + spike_length))
        pygame.draw.line(surf, spike_color, (start_x, start_y), (end_x, end_y), 3)
    
    # Oči - svítivě modré
    eye_color = (100, 200, 220)
    eye_radius = px // 2 + 1
    pygame.draw.circle(surf, eye_color, (int(center_x - 1.5*px), int(center_y - 0.5*px)), eye_radius)
    pygame.draw.circle(surf, eye_color, (int(center_x + 1.5*px), int(center_y - 0.5*px)), eye_radius)
    
    # Blikající pupily
    pupil_color = (50, 150, 200)
    pygame.draw.circle(surf, pupil_color, (int(center_x - 1.5*px), int(center_y - 0.5*px)), max(1, eye_radius // 2))
    pygame.draw.circle(surf, pupil_color, (int(center_x + 1.5*px), int(center_y - 0.5*px)), max(1, eye_radius // 2))
    
    # Modrý zásvit kolem Seekera
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(glow, (100, 150, 200, 50), (size//2, size//2), size//2)
    surf.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    
    return surf

def create_slime_blast_texture(size):
    """Procedurálně vytvoří texturu pro slime blast schopnost."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Hlavní slimák - zářivě modrý
    slime_color = (50, 150, 255)
    glow_color = (100, 200, 255)
    edge_color = (30, 100, 200)
    
    # Kruhový slimák
    pygame.draw.circle(surf, slime_color, (size//2, size//2), int(size * 0.35))
    pygame.draw.circle(surf, glow_color, (size//2 - 3, size//2 - 3), int(size * 0.25))
    
    # Oči
    eye_color = (255, 100, 100)
    pygame.draw.circle(surf, eye_color, (int(size * 0.35), int(size * 0.35)), 4)
    pygame.draw.circle(surf, eye_color, (int(size * 0.65), int(size * 0.35)), 4)
    pygame.draw.circle(surf, (200, 50, 50), (int(size * 0.35), int(size * 0.35)), 2)
    pygame.draw.circle(surf, (200, 50, 50), (int(size * 0.65), int(size * 0.35)), 2)
    
    # Zářivý oreol - modrý
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(glow, (100, 200, 255, 80), (size//2, size//2), int(size * 0.45))
    surf.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    
    return surf

# Vlastnosti hitboxů zbraní (dosah, úhel rozptylu a poškození)
WEAPON_HITBOX_PROPS = {
    'Sword':  {'range': 260, 'arc': 110, 'damage': 1},
    'Spear':  {'range': 400, 'arc': 25,  'damage': 2},
    'Scythe': {'range': 280, 'arc': 160, 'damage': 3}
}

# Vykreslení vlastního kurzoru na obrazovce (místo systémové šipky)
def draw_custom_cursor(surf, x, y, size=10):
    cursor_color = (180, 220, 255)      # Světle modrá barva kurzoru
    highlight_color = (255, 255, 255)   # Bílá barva pro středový bod
    # Kreslení kružnice (obrysu)
    pygame.draw.circle(surf, cursor_color, (x, y), size, 2)
    # Kreslení vodorovné linky zaměřovače
    pygame.draw.line(surf, cursor_color, (x - size, y), (x + size, y), 1)
    # Kreslení svislé linky zaměřovače
    pygame.draw.line(surf, cursor_color, (x, y - size), (x, y + size), 1)
    # Kreslení malého bodu uprostřed
    pygame.draw.circle(surf, highlight_color, (x, y), 2)

# --- Pomocná funkce pro kreslení tlačítka s hover efektem ---
def draw_button(surf, rect, label, hovered):
    # Definice barev pro normální stav a stav při přejetí myší (hover)
    base_col   = (30,  40,  70, 210)  # Tmavě modrá (poloprůhledná)
    hover_col  = (50,  80, 160, 230) # Jasnější modrá při najetí myší
    border_col = (80, 140, 255) if hovered else (60, 80, 140) # Barva rámečku
    fill_col   = hover_col if hovered else base_col # Výběr barvy pozadí

    # Vytvoření plochy pro pozadí tlačítka (podpora průhlednosti)
    btn_bg = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    # Kreslení zaobleného obdélníku pozadí
    pygame.draw.rect(btn_bg, fill_col, btn_bg.get_rect(), border_radius=14)
    surf.blit(btn_bg, rect.topleft) # Vykreslení pozadí na hlavní plochu

    # Kreslení rámečku tlačítka
    pygame.draw.rect(surf, border_col, rect, width=2, border_radius=14)

    # Přidání jemného vnějšího zásvitu, pokud je na tlačítko najeto myší
    if hovered:
        glow_s = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_s, (80, 160, 255, 45), glow_s.get_rect(), border_radius=18)
        surf.blit(glow_s, (rect.x - 10, rect.y - 10))

    # Příprava a vycentrování textu tlačítka
    lbl_col = (230, 240, 255) if hovered else (180, 190, 220) # Barva písma
    lbl_surf = btn_font.render(label, True, lbl_col)
    surf.blit(lbl_surf, (
        rect.x + (rect.width  - lbl_surf.get_width())  // 2, # Centrování horizontálně
        rect.y + (rect.height - lbl_surf.get_height()) // 2  # Centrování vertikálně
    ))

def fade_to_black(screen, clock):
    """Vytvoří plynulé zatmění obrazovky (fade-out) pro filmové přechody mezi menu."""
    fade_surf = pygame.Surface((width, height)) # Plocha o velikosti celé obrazovky
    fade_surf.fill((0, 0, 0)) # Černá barva
    # Postupně zvyšujeme neprůhlednost (alpha) od 0 (průhledné) do 255 (neprůhledné)
    for alpha in range(0, 255, 12):
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0)) # Překrytí obrazovky
        pygame.display.flip() # Aktualizace zobrazení
        clock.tick(60) # Omezení rychlosti animace


# Výpočet vykreslovacích rozměrů objektů podle aktuálního přiblížení (zoomu)
wall_draw_size = math.ceil(block_size * zoom)
player_draw_size = math.ceil(size * zoom)
enemy_draw_size = math.ceil(enemy_size * zoom)

# Nastavení textury pro podlahu a záložního řešení (když textura chybí)
floor_fallback = pygame.Surface((256, 256))
floor_fallback.fill((10, 40, 50)) # Tmavě modrozelená barva podlahy
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

# --- Obrazovka nastavení (Settings Menu) ---
def show_settings_menu(screen, clock, bg_image):
    global brightness, target_fps, show_fps_counter, show_hitboxes, running
    
    settings_open = True
    # Vytvoření poloprůhledné černé plochy přes celou obrazovku
    settings_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    settings_surf.fill((0, 0, 0, 200))

    settings_font = pygame.font.SysFont(None, 80)
    settings_title = settings_font.render("SETTINGS", True, (255, 255, 255))
    
    # Definice rozměrů a pozic tlačítek pro nastavení
    btn_sz = 60
    row_y = [200, 280, 360, 440, 520, 600] # Výškové úrovně pro řádky nastavení
    
    # Obdélníky pro interaktivní prvky (tlačítka a volby)
    br_minus_btn = pygame.Rect(width // 2 - 200, row_y[0], btn_sz, btn_sz)
    br_plus_btn  = pygame.Rect(width // 2 + 150, row_y[0], btn_sz, btn_sz)
    fps_minus_btn = pygame.Rect(width // 2 - 200, row_y[1], btn_sz, btn_sz)
    fps_plus_btn  = pygame.Rect(width // 2 + 150, row_y[1], btn_sz, btn_sz)
    fps_toggle_btn = pygame.Rect(width // 2 - 200, row_y[2], 400, btn_sz)
    hitbox_toggle_btn = pygame.Rect(width // 2 - 200, row_y[3], 400, btn_sz)
    controls_btn = pygame.Rect(width // 2 - 200, row_y[4], 400, btn_sz)
    back_btn = pygame.Rect(width // 2 - 170, height - 110, 340, 64)

    settings_mode = "main" # Aktuální režim (hlavní nastavení nebo nápověda k ovládání)

    while settings_open:
        smx, smy = pygame.mouse.get_pos() # Aktuální pozice myši
        for s_event in pygame.event.get():
            if s_event.type == pygame.QUIT:
                running = False
                settings_open = False
            if s_event.type == pygame.KEYDOWN:
                if s_event.key == pygame.K_ESCAPE:
                    # Pokud jsme v ovládání, vrátíme se do menu nastavení, jinak zavřeme menu
                    if settings_mode == "controls":
                        settings_mode = "main"
                    else:
                        settings_open = False
            
            # Detekce kliknutí myší
            if s_event.type == pygame.MOUSEBUTTONDOWN and s_event.button == 1:
                if settings_mode == "main":
                    if back_btn.collidepoint(smx, smy):
                        settings_open = False # Zavřít nastavení
                    elif br_minus_btn.collidepoint(smx, smy):
                        brightness = max(0, brightness - 10) # Snížit jas
                    elif br_plus_btn.collidepoint(smx, smy):
                        brightness = min(255, brightness + 10) # Zvýšit jas
                    elif fps_minus_btn.collidepoint(smx, smy):
                        target_fps = max(30, target_fps - 10) # Snížit limit FPS
                    elif fps_plus_btn.collidepoint(smx, smy):
                        target_fps = min(240, target_fps + 10) # Zvýšit limit FPS
                    elif fps_toggle_btn.collidepoint(smx, smy):
                        show_fps_counter = not show_fps_counter # Přepnout počítadlo FPS
                    elif hitbox_toggle_btn.collidepoint(smx, smy):
                        show_hitboxes = not show_hitboxes # Přepnout zobrazení hitboxů
                    elif controls_btn.collidepoint(smx, smy):
                        settings_mode = "controls" # Přepnout na zobrazení ovládání
                else:
                    # Pokud jsme v ovládání, tlačítko zpět nás vrátí do menu nastavení
                    if back_btn.collidepoint(smx, smy):
                        settings_mode = "main"

        if not running:
            break

        # Vykreslení prvků menu
        screen.blit(bg_image, (0, 0)) # Pozadí
        screen.blit(settings_surf, (0, 0)) # Poloprůhledný překryv
        screen.blit(settings_title, (width // 2 - settings_title.get_width() // 2, 100)) # Nadpis

        if settings_mode == "main":
            # Text pro Jas (Brightness)
            br_val_text = option_font.render(f"Brightness: {brightness}", True, (255, 255, 255))
            screen.blit(br_val_text, (width // 2 - br_val_text.get_width() // 2, row_y[0] + 10))
            draw_button(screen, br_minus_btn, "-", br_minus_btn.collidepoint(smx, smy))
            draw_button(screen, br_plus_btn, "+", br_plus_btn.collidepoint(smx, smy))
            
            # Text pro FPS limit
            fps_val_text = option_font.render(f"FPS: {target_fps}", True, (255, 255, 255))
            screen.blit(fps_val_text, (width // 2 - fps_val_text.get_width() // 2, row_y[1] + 10))
            draw_button(screen, fps_minus_btn, "-", fps_minus_btn.collidepoint(smx, smy))
            draw_button(screen, fps_plus_btn, "+", fps_plus_btn.collidepoint(smx, smy))
            
            # Tlačítka pro počítadlo FPS, hitboxy a vstup do ovládání
            fps_count_label = f"FPS Counter: {'ON' if show_fps_counter else 'OFF'}"
            draw_button(screen, fps_toggle_btn, fps_count_label, fps_toggle_btn.collidepoint(smx, smy))
            
            hitbox_label = f"Show Hitboxes: {'ON' if show_hitboxes else 'OFF'}"
            draw_button(screen, hitbox_toggle_btn, hitbox_label, hitbox_toggle_btn.collidepoint(smx, smy))
            
            draw_button(screen, controls_btn, "Controls", controls_btn.collidepoint(smx, smy))

        elif settings_mode == "controls":
            # Zobrazení nápovědy k ovládání
            controls_title = option_font.render("CONTROLS", True, (255, 255, 255))
            screen.blit(controls_title, (width // 2 - controls_title.get_width() // 2, 220))
            controls_lines = [
                "W / A / S / D - Move",
                "Mouse - Aim / Attack",
                "MOUSE LEFT - Attack",
                "SPACE - Pickup item",
                "1 / 2 / 3 - Select Weapon Slot",
                "B - Open Inventory",
                "ESC - Pause / Back",
            ]
            for idx, line in enumerate(controls_lines):
                line_surf = option_font.render(line, True, (220, 220, 220))
                screen.blit(line_surf, (width // 2 - line_surf.get_width() // 2, 290 + idx * 45))

        # Tlačítko pro návrat zpět
        draw_button(screen, back_btn, "Back", back_btn.collidepoint(smx, smy))
        draw_custom_cursor(screen, smx, smy) # Vykreslení zaměřovače
        pygame.display.flip()
        clock.tick(60)

def get_text_input(screen, clock, title_text, initial_text=""):
    """Jednoduchá funkce pro zadávání textu z klávesnice (pro přejmenování slotu)."""
    input_active = True
    user_text = initial_text
    input_font = pygame.font.SysFont(None, 60)
    
    # Tmavé pozadí pro zadávání textu
    bg_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    bg_overlay.fill((0, 0, 0, 230))

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False # Potvrzení klávesou Enter
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1] # Mazání posledního znaku
                elif event.key == pygame.K_ESCAPE:
                    return initial_text # Zrušení pomocí Escape
                else:
                    # Přidání znaku z klávesnice (omezení na 15 znaků)
                    if len(user_text) < 15:
                        user_text += event.unicode

        screen.blit(bg_overlay, (0, 0))
        
        # Vykreslení nadpisu okna
        t_surf = font.render(title_text, True, (200, 200, 200))
        screen.blit(t_surf, (width // 2 - t_surf.get_width() // 2, height // 2 - 100))
        
        # Vykreslení rámečku a zadaného textu s kurzorem (|)
        txt_surf = input_font.render(user_text + "|", True, (255, 255, 255))
        pygame.draw.rect(screen, (40, 60, 100), (width // 2 - 250, height // 2 - 30, 500, 70), border_radius=10)
        pygame.draw.rect(screen, (80, 120, 255), (width // 2 - 250, height // 2 - 30, 500, 70), 2, border_radius=10)
        screen.blit(txt_surf, (width // 2 - txt_surf.get_width() // 2, height // 2 - 15))
        
        # Nápověda k ovládání zadávání
        hint = font.render("Press ENTER to confirm, ESC to cancel", True, (100, 150, 200))
        screen.blit(hint, (width // 2 - hint.get_width() // 2, height // 2 + 60))

        pygame.display.flip()
        clock.tick(60)
    
    # Odstranění mezer na začátku a konci; pokud je text prázdný, použijeme výchozí název
    return user_text.strip() if user_text.strip() else "Unnamed Slot"

def show_save_slots(screen, clock):
    """Obrazovka pro výběr, přejmenování a mazání uložených herních pozic (Save Slotů)."""
    global current_save_slot
    
    slots_open = True
    # Vytvoření dynamického pozadí s modrým gradientem
    bg_img = pygame.Surface((width, height))
    bg_img.fill((10, 15, 30))
    for i in range(height):
        col = (10, 15 + i // 40, 30 + i // 20)
        pygame.draw.line(bg_img, col, (0, i), (width, i))

    while slots_open:
        mx, my = pygame.mouse.get_pos()
        # Načtení informací o všech 4 slotech pro aktuální zobrazení
        slot_infos = [load_save_info(i) for i in range(1, 5)]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    slots_open = False # Návrat do hlavního menu
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Logika detekce kliknutí na tlačítka v jednotlivých řádcích (slotech)
                for i in range(1, 5):
                    base_y = 220 + (i-1) * 160
                    # Definice hitboxů pro Play, Rename a Delete (musí odpovídat vykreslování)
                    btn_play = pygame.Rect(width // 2 - 100, base_y, 250, 80)
                    btn_rename = pygame.Rect(width // 2 + 180, base_y, 100, 80)
                    btn_delete = pygame.Rect(width // 2 + 300, base_y, 100, 80)
                    
                    if btn_play.collidepoint(mx, my):
                        fade_to_black(screen, clock) # Efekt zatmění
                        if slot_infos[i-1]:
                            # Načtení existující hry
                            if load_game(i):
                                return "PLAYING"
                        else:
                            # Vytvoření zcela nové hry v prázdném slotu
                            reset_game_world()
                            current_save_slot = i
                            save_game(i, f"New Adventure {i}")
                            return "PLAYING"
                    
                    if btn_rename.collidepoint(mx, my) and slot_infos[i-1]:
                        # Dialog pro přejmenování slotu
                        new_name = get_text_input(screen, clock, "Rename Slot:", slot_infos[i-1]['name'])
                        load_game(i) # Načteme data slotu do paměti
                        save_game(i, new_name) # Uložíme je zpět s novým jménem
                    
                    if btn_delete.collidepoint(mx, my) and slot_infos[i-1]:
                        # Smazání uložené pozice
                        delete_save(i)
                
                # Tlačítko pro návrat do menu
                back_btn = pygame.Rect(width // 2 - 100, height - 100, 200, 60)
                if back_btn.collidepoint(mx, my):
                    slots_open = False

        # Vykreslení prvků obrazovky Save Slotů
        screen.blit(bg_img, (0, 0))
        title = menu_title_font.render("SELECT SLOT", True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 60))

        for i in range(1, 5):
            base_y = 220 + (i-1) * 160
            info = slot_infos[i-1]
            
            # Box pozadí každého slotu
            box_rect = pygame.Rect(width // 2 - 400, base_y - 20, 800, 120)
            pygame.draw.rect(screen, (20, 30, 50, 150), box_rect, border_radius=15)
            pygame.draw.rect(screen, (50, 80, 150), box_rect, 2, border_radius=15)
            
            # Zobrazení názvu slotu
            slot_name = info['name'] if info else "--- EMPTY SLOT ---"
            name_color = (255, 255, 255) if info else (100, 110, 130)
            name_surf = option_font.render(f"#{i} {slot_name}", True, name_color)
            screen.blit(name_surf, (width // 2 - 380, base_y + 15))
            
            # Hlavní tlačítko slotu (PLAY nebo NEW GAME)
            btn_play = pygame.Rect(width // 2 - 100, base_y, 250, 80)
            play_lbl = "PLAY" if info else "NEW GAME"
            draw_button(screen, btn_play, play_lbl, btn_play.collidepoint(mx, my))
            
            # Zobrazení tlačítek pro přejmenování a smazání pouze u existujících pozic
            if info:
                btn_rename = pygame.Rect(width // 2 + 180, base_y, 100, 80)
                btn_delete = pygame.Rect(width // 2 + 300, base_y, 100, 80)
                draw_button(screen, btn_rename, "R", btn_rename.collidepoint(mx, my))
                draw_button(screen, btn_delete, "X", btn_delete.collidepoint(mx, my))
                
                # Dodatečné informace o postupu ve slotu (životy)
                details = f"Health: {info['player_health']}"
                det_surf = font.render(details, True, (150, 160, 180))
                screen.blit(det_surf, (width // 2 - 380, base_y + 55))

        # Tlačítko zpět dole na obrazovce
        back_btn = pygame.Rect(width // 2 - 100, height - 100, 200, 60)
        draw_button(screen, back_btn, "Back", back_btn.collidepoint(mx, my))
        
        draw_custom_cursor(screen, mx, my) # Vykreslení kurzoru
        pygame.display.flip() # Překlopení snímku na monitor
        clock.tick(60) # Omezení FPS na 60 v menu
    
    return "MAIN_MENU" # Návrat k hlavnímu menu, pokud nebylo kliknuto na Play

# --- Hlavní menu (Main Menu) ---
def show_main_menu(screen, clock):
    global running
    
    menu_running = True
    bg_img = pygame.Surface((width, height))
    bg_img.fill((10, 15, 30)) # Tmavě modré pozadí pro menu
    
    # Přidáme jemný gradient nebo texturu na pozadí
    for i in range(height):
        col = (10, 15 + i // 40, 30 + i // 20)
        pygame.draw.line(bg_img, col, (0, i), (width, i))
    
    # Přidáme pár ambientních částic do menu pro efekt
    menu_particles = []
    for _ in range(50):
        menu_particles.append({
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'speed': random.uniform(0.2, 0.8),
            'radius': random.uniform(1, 3)
        })

    btn_w, btn_h = 340, 70
    btn_x = width - btn_w - 150
    # Posuneme vše výše (odečteme více od svislého středu)
    play_btn     = pygame.Rect(btn_x, height // 2 - 120,       btn_w, btn_h)
    settings_btn = pygame.Rect(btn_x, height // 2 - 120 + 100, btn_w, btn_h)
    quit_btn     = pygame.Rect(btn_x, height // 2 - 120 + 200, btn_w, btn_h)



    while menu_running:
        mx, my = pygame.mouse.get_pos() # Získání pozice myši
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Detekce kliknutí na tlačítka menu
                if play_btn.collidepoint(mx, my):
                    fade_to_black(screen, clock) # Přechod do výběru slotů
                    state = show_save_slots(screen, clock)
                    if state == "PLAYING":
                        return "PLAYING" # Zahájení hry
                elif settings_btn.collidepoint(mx, my):
                    show_settings_menu(screen, clock, bg_img) # Otevření nastavení
                elif quit_btn.collidepoint(mx, my):
                    running = False # Ukončení hry
                    menu_running = False

        if not running:
            break

        # --- Pulzující efekt tmavého pozadí ---
        pulse_time = pygame.time.get_ticks() / 1000.0
        pulse_val = (math.sin(pulse_time * 1.5) + 1) / 2 # Hodnota 0 až 1
        
        # Vykreslení pozadí a částic
        screen.blit(bg_img, (0, 0))
        
        # Přidáme tmavý pulzující overlay pro hloubku
        pulse_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pulse_alpha = int(40 + 40 * pulse_val) # Pulzuje mezi 40 a 80
        pulse_surf.fill((0, 0, 5, pulse_alpha))
        screen.blit(pulse_surf, (0, 0))

        for p in menu_particles:

            p['y'] -= p['speed']
            if p['y'] < -10: p['y'] = height + 10
            pygame.draw.circle(screen, (50, 100, 200), (int(p['x']), int(p['y'])), int(p['radius']))

        # Titulek hry
        title_surf = menu_title_font.render("THE LABYRINTH", True, (255, 255, 255))
        title_x = width - title_surf.get_width() - 150 # Pozice vpravo
        title_y = height // 2 - 500
        
        # Vykreslení modré záře (stínu) pod titulkem pro lepší čitelnost
        glow_surf = menu_title_font.render("THE LABYRINTH", True, (50, 150, 255))
        for offset in range(1, 5):
            screen.blit(glow_surf, (title_x + offset, title_y + offset))
        screen.blit(title_surf, (title_x, title_y)) # Samotný bílý text



        # Tlačítka
        draw_button(screen, play_btn,     "PLAY",     play_btn.collidepoint(mx, my))
        draw_button(screen, settings_btn, "SETTINGS", settings_btn.collidepoint(mx, my))
        draw_button(screen, quit_btn,     "QUIT",     quit_btn.collidepoint(mx, my))

        draw_custom_cursor(screen, mx, my)
        pygame.display.flip()
        clock.tick(60)
    
    return "QUIT"

# --- Obrazovka Inventáře (Inventory Menu) ---
def show_inventory(screen, clock, bg_copy):
    """Zobrazí obrazovku inventáře s předměty hráče a rozmazaným pozadím."""
    global running, inventory, current_weapon, unlocked_weapons
    
    # Efekt rozmazání pozadí (blur) pomocí dvojího škálování
    bg_copy = pygame.transform.smoothscale(bg_copy, (width // 10, height // 10))
    bg_copy = pygame.transform.smoothscale(bg_copy, (width, height))

    inventory_open = True

    # Tmavě modrý panel inventáře přes celou obrazovku
    inv_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    inv_surf.fill((0, 0, 10, 245)) # Velmi tmavý a neprůhledný podklad

    
    inv_title_font = pygame.font.SysFont(None, 100)
    section_font = pygame.font.SysFont(None, 60)
    item_font = pygame.font.SysFont(None, 45)
    
    while inventory_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                inventory_open = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    inventory_open = False
        
        if not running:
            break
            
        screen.blit(bg_copy, (0, 0))
        screen.blit(inv_surf, (0, 0))
        
        # Nadpis inventáře
        title = inv_title_font.render("INVENTORY", True, (255, 255, 255))
        screen.blit(title, (width // 2 - title.get_width() // 2, 80))

        # Vykreslení velké ikony hráče na levé straně
        player_inv_size = 350
        textura_hrac_velka = pygame.transform.scale(textura_hrac, (player_inv_size, player_inv_size))
        icon_x = width // 4 - player_inv_size // 2
        icon_y = height // 2 - player_inv_size // 2
        screen.blit(textura_hrac_velka, (icon_x, icon_y))
        
        # Rozdělení na sekce: MISC (střed) a UPGRADES (vpravo)
        misc_x = width // 2 - 200
        upgrades_x = width // 2 + 300
        start_y = 220
        
        # Sekce MISC
        misc_title = section_font.render("MISC ITEMS", True, (150, 200, 255))
        screen.blit(misc_title, (misc_x, start_y))
        pygame.draw.line(screen, (70, 100, 180), (misc_x, start_y + 50), (misc_x + 300, start_y + 50), 2)
        
        misc_items = [item for item in inventory if item == "Key"]
        for idx, item in enumerate(misc_items):
            if item == "Key":
                text = item_font.render("Golden Key", True, (255, 215, 0))
                screen.blit(textura_klic_icon, (misc_x, start_y + 80 + idx * 70))
                screen.blit(text, (misc_x + 70, start_y + 90 + idx * 70))
        
        if not misc_items:
            empty_text = item_font.render("No misc items...", True, (100, 100, 120))
            screen.blit(empty_text, (misc_x, start_y + 80))
            
        # Sekce UPGRADES
        upgrades_title = section_font.render("UPGRADES", True, (180, 255, 200))
        screen.blit(upgrades_title, (upgrades_x, start_y))
        pygame.draw.line(screen, (70, 180, 120), (upgrades_x, start_y + 50), (upgrades_x + 300, start_y + 50), 2)
        
        upgrade_items = [item for item in inventory if item == "Glitter Slime Ball"]
        for idx, item in enumerate(upgrade_items):
            if item == "Glitter Slime Ball":
                text = item_font.render("Glitter Slime Ball", True, (180, 255, 255))
                screen.blit(textura_glitter_ball, (upgrades_x, start_y + 80 + idx * 70))
                screen.blit(text, (upgrades_x + 70, start_y + 90 + idx * 70))
                desc = item_font.render("(Passive: Increased Speed)", True, (120, 180, 180))
                screen.blit(desc, (upgrades_x + 70, start_y + 120 + idx * 70))
        
        feather_items = [item for item in inventory if item == "Feather"]
        for idx, item in enumerate(feather_items):
            f_offset = len(upgrade_items) * 70
            text = item_font.render("Feather", True, (240, 245, 255))
            screen.blit(textura_feather_icon, (upgrades_x, start_y + 80 + f_offset + idx * 70))
            screen.blit(text, (upgrades_x + 70, start_y + 90 + f_offset + idx * 70))
            desc = item_font.render("(Active: Dash - RMB)", True, (150, 200, 255))
            screen.blit(desc, (upgrades_x + 70, start_y + 120 + f_offset + idx * 70))
        
        # Slime Blast Display
        if slime_blast_available:
            f_offset = (len(upgrade_items) + len(feather_items)) * 70
            text = item_font.render("Slime Blast", True, (150, 255, 150))
            screen.blit(textura_slime_blast_icon, (upgrades_x, start_y + 80 + f_offset))
            screen.blit(text, (upgrades_x + 70, start_y + 90 + f_offset))
            desc = item_font.render("(Active: Cast - F)", True, (100, 200, 100))
            screen.blit(desc, (upgrades_x + 70, start_y + 120 + f_offset))
        
        if not upgrade_items and not feather_items and not slime_blast_available:
            empty_text = item_font.render("No upgrades...", True, (100, 120, 100))
            screen.blit(empty_text, (upgrades_x, start_y + 80))

        # Sekce WEAPONS (Zbraně odemčené hráčem)
        weapons_x = misc_x
        weapons_start_y = start_y + 320 # Posunuto níže
        weapons_title = section_font.render("WEAPONS", True, (255, 180, 80))
        screen.blit(weapons_title, (weapons_x, weapons_start_y))
        pygame.draw.line(screen, (180, 110, 30), (weapons_x, weapons_start_y + 50), (weapons_x + 300, weapons_start_y + 50), 2)

        weapon_colors = {'Sword': (80, 160, 255), 'Spear': (0, 220, 220), 'Scythe': (160, 80, 255)}
        if unlocked_weapons:
            for w_idx, wname in enumerate(unlocked_weapons):
                is_active = (wname == current_weapon)
                wcolor = weapon_colors.get(wname, (200, 200, 200))
                row_y = weapons_start_y + 65 + w_idx * 80
                # Zvýraznění aktivní zbraně
                if is_active:
                    hl_surf = pygame.Surface((450, 65), pygame.SRCALPHA) # Rozšířeno, aby se vešel text
                    hl_surf.fill((*wcolor, 35))
                    pygame.draw.rect(hl_surf, (*wcolor, 180), (0, 0, 450, 65), 2, border_radius=8)
                    screen.blit(hl_surf, (weapons_x - 5, row_y - 5))
                # Ikona zbraně
                wtex = WEAPON_TEXTURES.get(wname)
                if wtex:
                    wicon = pygame.transform.scale(wtex, (50, 50))
                    screen.blit(wicon, (weapons_x, row_y))
                # Název zbraně + číslo slotu
                slot_num = w_idx + 1
                label = f"[{slot_num}]  {wname}"
                if is_active:
                    label += "  ◄ ACTIVE"
                label_color = wcolor if is_active else (160, 170, 190)
                label_surf = item_font.render(label, True, label_color)
                screen.blit(label_surf, (weapons_x + 60, row_y + 12))
        else:
            # Nejprve zkontrolujeme kolizi s nepřáteli (projektil by měl zasáhnout i nepřátele)
            hit_enemy = False
            for enemy in enemies:
                if enemy.get('respawn_timer', 0) > 0:
                    continue
                enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_size, enemy_size)
                if proj_rect.colliderect(enemy_rect):
                    # Aplikujeme poškození
                    dmg = proj.get('damage', SLIME_BLAST_DAMAGE)
                    enemy['hp'] -= dmg

                    # Vytvoření modrých částic při zásahu nepřítele
                    for _ in range(14):
                        particles.append({
                            'x': proj['x'], 'y': proj['y'],
                            'radius': random.uniform(3, 9), 'life': 18,
                            'color': (100, 180, 255),
                            'dx': random.uniform(-16, 16), 'dy': random.uniform(-16, 16)
                        })

                    # Knockback od směru projektilu
                    try:
                        kb_angle = math.atan2((enemy['y'] + enemy_size/2) - proj['y'], (enemy['x'] + enemy_size/2) - proj['x'])
                        kb_strength = 12
                        enemy['knockback_x'] = math.cos(kb_angle) * kb_strength
                        enemy['knockback_y'] = math.sin(kb_angle) * kb_strength
                    except Exception:
                        pass

                    # Pokud nepřítel zemře, resetujeme ho podobně jako u zbraní
                    if enemy['hp'] <= 0:
                        enemy['x'], enemy['y'] = enemy['start_x'], enemy['start_y']
                        enemy['hp'] = max_enemy_hp
                        enemy['is_dashing'] = False
                        enemy['respawn_timer'] = 7200

                    # Odstraníme projektil a ukončíme kontrolu
                    if proj in slime_blast_projectiles:
                        slime_blast_projectiles.remove(proj)
                    hit_enemy = True
                    break

            if hit_enemy:
                continue
            no_w = item_font.render("No weapons found...", True, (100, 110, 130))
            screen.blit(no_w, (weapons_x, weapons_start_y + 65))
            
        draw_custom_cursor(screen, *pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(60)

# Varianty podlahy pro vizuální rozmanitost (aby podlaha nepůsobila jednotvárně, vytvoříme zrcadlové kopie textury)

floor_variations = [
    floor_texture,
    pygame.transform.flip(floor_texture, True, False), # Převráceno zleva doprava
    pygame.transform.flip(floor_texture, False, True), # Převráceno shora dolů
    pygame.transform.flip(floor_texture, True, True)   # Převráceno v obou osách
]

game_state = "MAIN_MENU"



# Načtení konkrétních textur do proměnných (s využitím naší bezpečné funkce)
textura_zed = get_texture("wall.png", (100, 100, 100), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))
textura_zamcena_zed = get_texture("locked_wall.png", (139, 69, 19), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))
textura_rozbitelna_zed = get_texture("breakable_wall.png", (180, 150, 100), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))
textura_hrac = get_texture("player.png", color, (player_draw_size, player_draw_size))
textura_nepritel = create_bug_texture(enemy_draw_size)
textura_seeker = create_seeker_texture(enemy_draw_size)
textura_klic_icon = get_texture("key.png", (255, 215, 0), (50, 50))
textura_slime_orb = get_texture("slime_orb.png", (0, 188, 212), (30, 30))
textura_slime_orb_eyes = get_texture("slime_orb_eyes.png", (33, 150, 243), (50, 50))
textura_glitter_ball = get_texture("glitter_slime_ball.png", (180, 255, 255), (50, 50), pixelate_size=(16, 16), colorkey=(0, 0, 0))

# Textury zbraní (Procedurálně generované modré pixel-art zbraně)
textura_weapon_sword  = create_pixel_weapon('Sword', 96)
textura_weapon_spear  = create_pixel_weapon('Spear', 96)
textura_weapon_scythe = create_pixel_weapon('Scythe', 96)
textura_weapon_icon   = pygame.transform.scale(textura_weapon_sword, (50, 50)) # Ikona je zmenšený meč
textura_feather = create_feather_texture(50)
textura_feather_icon = pygame.transform.scale(textura_feather, (50, 50))
textura_slime_blast_icon = create_slime_blast_texture(50)

# --- Textury dekorací ---
textura_crystal_blue = create_crystal_texture(32, (0, 150, 255))
textura_crystal_blue_light = create_crystal_texture(32, (111, 169, 209))
textura_crystal_blue_dark = create_crystal_texture(32, (0, 83, 194))

textura_vine = create_vine_texture(64)
textura_cobweb = create_cobweb_texture(64)

WEAPON_TEXTURES = {'Sword': textura_weapon_sword, 'Spear': textura_weapon_spear, 'Scythe': textura_weapon_scythe}


textura_healing_platform = get_texture("healing_platform.png", (0, 100, 220), (wall_draw_size, wall_draw_size), pixelate_size=(64, 64))

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

# Vykreslení rozbitelných zdí na předpřipravený povrch
for b_wall in breakable_walls:
    surf_x = int(b_wall['rect'].x * zoom)
    surf_y = int(b_wall['rect'].y * zoom)
    maze_surface.blit(textura_rozbitelna_zed, (surf_x, surf_y))

# Proměnné pro animaci pohybu (pohupování postavičky, když jde)
wobble_time = 0.0
wobble_amp = 0.0
shake_intensity = 0.0
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
    # --- Správa stavů hry ---
    if game_state == "MAIN_MENU":
        game_state = show_main_menu(screen, clock)
        if game_state == "QUIT":
            running = False
            break
        continue # Pokud se vracíme z menu, začneme smyčku znovu (vyčištění eventů atd.)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If the big message overlay is showing, any click or key press dismisses it
        if show_big_message:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                show_big_message = False
                continue

        # Kliknutí myší - Útok (left click handled on MOUSEBUTTONUP for reliability)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Top-right secret button hitbox
            mx, my = event.pos
            secret_rect = pygame.Rect(width - 34, 6, 28, 18)
            if secret_rect.collidepoint(mx, my):
                show_big_message = True
                continue
            if current_weapon and not is_attacking and not healing_in_progress:
                is_attacking = True
                attack_timer = attack_duration
                # Zamknutí úhlu pro útok
                draw_x_tmp = int((x - camera_x) * zoom)
                draw_y_tmp = int((y - camera_y) * zoom)
                rel_x = mouse_x - (draw_x_tmp + player_draw_size // 2)
                rel_y = mouse_y - (draw_y_tmp + player_draw_size // 2)
                attack_angle = math.degrees(math.atan2(rel_y, rel_x))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Mechanika dashe (pravé tlačítko myši)
            if "Feather" in inventory and player_dash_cooldown == 0 and not player_is_dashing:
                player_is_dashing = True
                player_dash_timer = DASH_DURATION
                player_dash_cooldown = DASH_COOLDOWN_TIME
                
                # Výpočet směru k myši pro dash
                draw_x_tmp = int((x - camera_x) * zoom)
                draw_y_tmp = int((y - camera_y) * zoom)
                rel_x = mouse_x - (draw_x_tmp + player_draw_size // 2)
                rel_y = mouse_y - (draw_y_tmp + player_draw_size // 2)
                dist = math.hypot(rel_x, rel_y)
                if dist > 0:
                    player_dash_x = (rel_x / dist) * 8 * DASH_SPEED_MULT # Použijeme základní rychlost * násobek
                    player_dash_y = (rel_y / dist) * 8 * DASH_SPEED_MULT
                
                # Startovací efekt dashe
                for _ in range(12):
                    particles.append({
                        'x': x + size / 2, 'y': y + size / 2,
                        'radius': random.uniform(5, 10), 'life': 20,
                        'color': (200, 240, 255), 'dx': random.uniform(-6, 6), 'dy': random.uniform(-6, 6)
                    })

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bg_copy = screen.copy()
                show_inventory(screen, clock, bg_copy)
            if event.key == pygame.K_f:
                # Počátek držení F klávesy
                f_key_pressed = True
                f_key_press_time = 0
            if event.key == pygame.K_SPACE:
                # Mechanika sbírání předmětů
                pickup_range = 150 # Dosah pro sebrání předmětu
                player_cx = x + size / 2
                player_cy = y + size / 2
                for item in items_on_ground[:]:
                    if math.hypot(player_cx - item['x'], player_cy - item['y']) <= pickup_range:
                        if item['type'] in ('Sword', 'Spear', 'Scythe'):
                            if item['type'] not in unlocked_weapons:
                                unlocked_weapons.append(item['type'])
                            if current_weapon is None:
                                current_weapon = item['type']
                        elif item['type'] == 'Slime Blast':
                            # Grant the player the slime blast ability (upgrade)
                            slime_blast_available = True
                            mana_charges = min(MAX_MANA_CHARGES, mana_charges + 1)
                        else:
                            inventory.append(item['type'])
                        pickup_notifications.append({'type': item['type'], 'time': pygame.time.get_ticks() / 1000.0, 'alpha': 255})
                        items_on_ground.remove(item)
                        break

            if event.key == pygame.K_1:
                if len(unlocked_weapons) >= 1: current_weapon = unlocked_weapons[0]
            if event.key == pygame.K_2:
                if len(unlocked_weapons) >= 2: current_weapon = unlocked_weapons[1]
            if event.key == pygame.K_3:
                if len(unlocked_weapons) >= 3: current_weapon = unlocked_weapons[2]

            if event.key == pygame.K_ESCAPE:
                paused = True
                pause_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pause_surf.fill((0, 0, 0, 190))
                pause_text = pause_font.render("PAUSED", True, (255, 255, 255))

                # Rozměry a pozice tlačítek v pauze
                btn_w, btn_h = 340, 60
                btn_x = width // 2 - btn_w // 2
                start_btn_y = height // 2 - 50
                
                btn_resume    = pygame.Rect(btn_x, start_btn_y,        btn_w, btn_h)
                btn_settings  = pygame.Rect(btn_x, start_btn_y + 80,   btn_w, btn_h)
                btn_main_menu = pygame.Rect(btn_x, start_btn_y + 160,  btn_w, btn_h)
                btn_quit      = pygame.Rect(btn_x, start_btn_y + 240,  btn_w, btn_h)

                pygame.mouse.set_visible(False)
                bg_copy = screen.copy()

                while paused:
                    mx, my = pygame.mouse.get_pos()
                    for p_event in pygame.event.get():
                        if p_event.type == pygame.QUIT:
                            running = False
                            paused = False
                        if p_event.type == pygame.KEYDOWN:
                            if p_event.key == pygame.K_ESCAPE:
                                paused = False
                        if p_event.type == pygame.MOUSEBUTTONDOWN and p_event.button == 1:
                            if btn_resume.collidepoint(mx, my):
                                paused = False
                            elif btn_settings.collidepoint(mx, my):
                                show_settings_menu(screen, clock, bg_copy)
                            elif btn_main_menu.collidepoint(mx, my):
                                # Návrat do menu (bez automatického uložení)
                                game_state = "MAIN_MENU"
                                paused = False
                            elif btn_quit.collidepoint(mx, my):
                                running = False
                                paused = False

                    if not running:
                        break

                    # --- Vykreslení pauza obrazovky ---
                    screen.blit(bg_copy, (0, 0))
                    screen.blit(pause_surf, (0, 0))
                    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 180))

                    # Jemná oddělovací linka pod nadpisem
                    line_y = height // 2 - 95
                    pygame.draw.line(screen, (70, 100, 180), (width // 2 - 170, line_y), (width // 2 + 170, line_y), 1)

                    # Tlačítka s hover efektem
                    draw_button(screen, btn_resume,    "Resume",    btn_resume.collidepoint(mx, my))
                    draw_button(screen, btn_settings,  "Settings",  btn_settings.collidepoint(mx, my))
                    draw_button(screen, btn_main_menu, "Main Menu", btn_main_menu.collidepoint(mx, my))
                    draw_button(screen, btn_quit,      "Exit Game", btn_quit.collidepoint(mx, my))
                    draw_custom_cursor(screen, mx, my)

                    pygame.display.flip()
                    clock.tick(60)

                    pygame.display.flip()
                    clock.tick(60)

                pygame.mouse.set_visible(False)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f and f_key_pressed:
                # Uvolnění F klávesy - určíme, zda jde o press či hold
                if f_key_press_time < HOLD_THRESHOLD:
                    # Krátký press - aktivace slime blast
                    if slime_blast_available:
                        # Enforce cooldown (1 second)
                        now_ms = pygame.time.get_ticks()
                        if now_ms - slime_blast_last_cast >= SLIME_BLAST_COOLDOWN_MS:
                            slime_blast_last_cast = now_ms
                            # Výpočet směru k myši
                            draw_x_tmp = int((x - camera_x) * zoom)
                            draw_y_tmp = int((y - camera_y) * zoom)
                            rel_x = mouse_x - (draw_x_tmp + player_draw_size // 2)
                            rel_y = mouse_y - (draw_y_tmp + player_draw_size // 2)
                            dist = math.hypot(rel_x, rel_y)

                            if dist > 0:
                                # Normalizace směru
                                dir_x = rel_x / dist
                                dir_y = rel_y / dist

                                # Spotřebuj jednu manu a vytvoř projektil
                                if mana_charges > 0:
                                    mana_charges -= 1
                                    proj = {
                                        'x': x + size / 2 + dir_x * 50,
                                        'y': y + size / 2 + dir_y * 50,
                                        'dx': dir_x * SLIME_BLAST_SPEED,
                                        'dy': dir_y * SLIME_BLAST_SPEED,
                                        'age': 0,
                                        'max_age': int(SLIME_BLAST_RANGE / SLIME_BLAST_SPEED),
                                        'damage': SLIME_BLAST_DAMAGE
                                    }
                                    slime_blast_projectiles.append(proj)
                                    # Small blue burst when casting
                                    for _ in range(8):
                                        particles.append({
                                            'x': proj['x'], 'y': proj['y'],
                                            'radius': random.uniform(3, 7), 'life': 18,
                                            'color': (100, 180, 255),
                                            'dx': random.uniform(-6, 6), 'dy': random.uniform(-6, 6)
                                        })
                        
                else:
                    # Dlouhý hold - aktivace léčení
                    if mana_charges > 0:
                        healing_in_progress = True
                        healing_timer = healing_duration
                        mana_charges -= 1
                
                f_key_pressed = False
                f_key_press_time = 0
            
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

    # --- Logika pohybu a dashe ---
    move_x = 0
    move_y = 0

    if player_is_dashing:
        move_x = player_dash_x
        move_y = player_dash_y
        player_dash_timer -= 1
        player_moved = True
        
        # Trail efekt během dashe
        if random.random() < 0.6:
            particles.append({
                'x': x + size / 2 + random.uniform(-15, 15), 
                'y': y + size / 2 + random.uniform(-15, 15),
                'radius': random.uniform(4, 8), 'life': 12,
                'color': (150, 220, 255, 180), 'dx': 0, 'dy': 0
            })
            
        if player_dash_timer <= 0:
            player_is_dashing = False
    elif healing_in_progress:
        # Během léčení je hráč zpomalený
        # Pohyb se stále vykonává, ale s menší rychlostí
        if distance > 1.0:
            current_speed = (8 if "Glitter Slime Ball" in inventory else 5) * healing_speed_multiplier
            speed = min(current_speed, distance)
            move_x = (dx / distance) * speed
            move_y = (dy / distance) * speed
        
        # Léčící částice (bílé a zlaté)
        for _ in range(3):
            particles.append({
                'x': x + size / 2 + random.uniform(-30, 30), 
                'y': y + size / 2 + random.uniform(-30, 30),
                'radius': random.uniform(3, 7), 'life': 15,
                'color': (255, 215, 100) if random.random() > 0.5 else (255, 255, 255),  # Zlatá nebo bílá
                'dx': random.uniform(-2, 2), 'dy': random.uniform(-3, -0.5)
            })
        
        # Pokračování léčení
        healing_timer -= 1
        if healing_timer <= 0:
            # Léčení skončilo - uzdravíme hráče
            player_health = min(6, player_health + healing_per_charge)
            mana_charges -= 1
            healing_in_progress = False
            
            # Finální efekt léčení (větší výbuch částic)
            for _ in range(20):
                particles.append({
                    'x': x + size / 2, 
                    'y': y + size / 2,
                    'radius': random.uniform(4, 10), 'life': 20,
                    'color': (255, 215, 100),  # Zlatá
                    'dx': random.uniform(-6, 6), 'dy': random.uniform(-6, 6)
                })
    elif distance > 1.0: # Pokud nejsme přesně na myši, budeme se pohybovat
        # Vypočítáme aktuální rychlost (sprint pokud máme Glitter Slime Ball)
        current_speed = 8 if "Glitter Slime Ball" in inventory else 5
        speed = min(current_speed, distance) # Omezíme rychlost na maximálně 5 pixelů (aby hráč nevyletěl moc rychle)
        move_x = (dx / distance) * speed # Posun v ose X
        move_y = (dy / distance) * speed # Posun v ose Y

    # Aktualizace cooldownu dashe
    if player_dash_cooldown > 0:
        player_dash_cooldown -= 1

    # Aktualizace času stisknutí F klávesy
    if f_key_pressed:
        f_key_press_time += 1

    if move_x != 0 or move_y != 0:


        # Pohyb a kontrola kolize (nárazu do zdi) v horizontálním směru (osa X)
        new_x = x + move_x
        # Vytvoření dočasného obdélníku pro zjištění kolize na nové pozici
        cube_rect_x = pygame.Rect(new_x + hitbox_offset, y + hitbox_offset, hitbox_size, hitbox_size)
        # Zkontrolujeme, zda tento obdélník nekoliduje s jakoukoliv pevnou zdí
        collision_x = cube_rect_x.collidelist(walls) != -1
        
        # Kontrola kolize s rozbitelnou zdí
        if not collision_x:
            for b_wall in breakable_walls:
                if cube_rect_x.colliderect(b_wall['rect']):
                    collision_x = True
                    break
                
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
        
        # Pokud došlo ke kolizi při dashi, ukončíme dash
        if collision_x and player_is_dashing:
            player_is_dashing = False

        # Pokud nedošlo k žádné kolizi, provedeme pohyb
        if not collision_x:
            x = new_x
            player_moved = True

        # Pohyb a kontrola kolize ve vertikálním směru (osa Y)
        new_y = y + move_y
        cube_rect_y = pygame.Rect(x + hitbox_offset, new_y + hitbox_offset, hitbox_size, hitbox_size)
        collision_y = cube_rect_y.collidelist(walls) != -1
        
        # Kontrola kolize s rozbitelnou zdí
        if not collision_y:
            for b_wall in breakable_walls:
                if cube_rect_y.colliderect(b_wall['rect']):
                    collision_y = True
                    break
                
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
        
        if collision_y and player_is_dashing:
            player_is_dashing = False

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

    # Aktualizace timeru nesmrtelnosti
    if player_invincibility_timer > 0:
        player_invincibility_timer -= 1

    # --- Kontrola kolize s léčivou platformou (checkpoint) ---
    player_hitbox = pygame.Rect(x + hitbox_offset, y + hitbox_offset, hitbox_size, hitbox_size)
    on_any_platform = False
    for idx, hp in enumerate(healing_platforms):
        if player_hitbox.colliderect(hp):
            on_any_platform = True
            # Uložení nového checkpointu
            checkpoint_x = x
            checkpoint_y = y
            # Plné vyléčení hráče
            player_health = 6
            
            # Spuštění záblesku pouze pokud na platformě ještě není aktivní záblesk
            center_x = hp.x + hp.width / 2
            center_y = hp.y + hp.height / 2
            already_glowing = any(
                abs(g['x'] - center_x) < 5 and abs(g['y'] - center_y) < 5
                for g in healing_platform_glow
            )
            if not already_glowing:
                # Automatické uložení hry do aktuálního slotu (pouze pokud jsme na nové platformě)
                if last_saved_platform_idx != idx:
                    save_game(current_save_slot)
                    last_saved_platform_idx = idx

                for ring_idx in range(4):
                    healing_platform_glow.append({
                        'x': center_x,
                        'y': center_y,
                        'radius': ring_idx * 18.0,
                        'alpha': 220 - ring_idx * 40
                    })
            break
    
    if not on_any_platform:
        last_saved_platform_idx = -1

    # --- Umělá inteligence nepřátel (Enemy AI) ---
    for enemy in enemies:
        # Přeskočíme nepřátele, kteří čekají na respawn
        if enemy.get('respawn_timer', 0) > 0:
            enemy['respawn_timer'] -= 1
            continue

        dx_enemy = x - enemy['x']
        dy_enemy = y - enemy['y']
        distance_enemy = math.hypot(dx_enemy, dy_enemy) # Vzdálenost mezi hráčem a nepřítelem

        # --- Kontrola Line of Sight (aby nepřítel neviděla skrz zdi) ---
        has_los = False
        if distance_enemy < 1000: # Maximální dosah zraku
            # Zjednodušený test viditelnosti (přímka mezi nepřítelem a hráčem)
            los_line = ((enemy['x'] + enemy_size/2, enemy['y'] + enemy_size/2), (x + size/2, y + size/2))
            
            # Najdeme jen zdi v okolí pro optimalizaci
            los_rect = pygame.Rect(min(x, enemy['x']), min(y, enemy['y']), abs(x - enemy['x']), abs(y - enemy['y']))
            los_rect.inflate_ip(100, 100)
            nearby_walls = [w for w in walls if los_rect.colliderect(w)] + [w for w in locked_walls if los_rect.colliderect(w)]
            
            has_los = True
            for wall in nearby_walls:
                if wall.clipline(*los_line):
                    has_los = False
                    break
        
        move_x_enemy = 0
        move_y_enemy = 0
        enemy_type = enemy.get('type', 'Fly')

        # --- Logika pro Fly (moucha) - Dash útok ---
        if enemy_type == 'Fly':
            # Logika Dash útoku (prudký výpad mouchy)
            dash_range = 450 # Vzdálenost, při které moucha začne útok
            dash_speed_mult = 5.5 # Kolikrát je dash rychlejší než normální pohyb
            
            if not enemy.get('is_dashing', False):
                if enemy.get('dash_cooldown', 0) > 0:
                    enemy['dash_cooldown'] -= 1
                elif has_los and distance_enemy < dash_range and distance_enemy > 0:
                    # Spuštění dashe - moucha se zaměří na hráče a vyrazí
                    enemy['is_dashing'] = True
                    enemy['dash_timer'] = 25 # Trvání dashe v počtu snímků
                    enemy['dash_x'] = (dx_enemy / distance_enemy) * enemy_speed * dash_speed_mult
                    enemy['dash_y'] = (dy_enemy / distance_enemy) * enemy_speed * dash_speed_mult
                    
                    # Efekt prachu/vzduchu při startu dashe
                    for _ in range(10):
                        particles.append({
                            'x': enemy['x'] + enemy_size / 2, 'y': enemy['y'] + enemy_size / 2,
                            'radius': random.uniform(4, 8), 'life': 15,
                            'color': (150, 200, 255), 'dx': random.uniform(-5, 5), 'dy': random.uniform(-5, 5)
                        })

            if enemy.get('is_dashing', False):
                move_x_enemy = enemy['dash_x']
                move_y_enemy = enemy['dash_y']
                enemy['dash_timer'] -= 1
                
                # Zanechávání stop (trail) částic během dashe pro vizuální efekt rychlosti
                if random.random() < 0.4:
                    particles.append({
                        'x': enemy['x'] + enemy_size / 2 + random.uniform(-10, 10), 
                        'y': enemy['y'] + enemy_size / 2 + random.uniform(-10, 10),
                        'radius': random.uniform(3, 6), 'life': 10,
                        'color': (100, 150, 255, 150), 'dx': 0, 'dy': 0
                    })
                    
                if enemy.get('dash_timer', 0) <= 0:
                    enemy['is_dashing'] = False
                    enemy['dash_cooldown'] = 70 # Doba odpočinku po dashi
            else:
                # Klasické pronásledování (pomalý let k hráči) - pouze pokud vidí hráče
                if has_los and distance_enemy > 0:
                    speed_enemy = min(enemy_speed, distance_enemy)
                    move_x_enemy = (dx_enemy / distance_enemy) * speed_enemy
                    move_y_enemy = (dy_enemy / distance_enemy) * speed_enemy

        # --- Logika pro Seeker (pronásledovatel) - Přímé pronásledování ---
        elif enemy_type == 'Seeker':
            seeker_speed = 5.5  # Vyšší rychlost než moucha
            
            if has_los and distance_enemy > 0:
                # Přímé pronásledování hráče když ho vidí
                speed_enemy = min(seeker_speed, distance_enemy)
                move_x_enemy = (dx_enemy / distance_enemy) * speed_enemy
                move_y_enemy = (dy_enemy / distance_enemy) * speed_enemy
                
                # Přidání zelených částic kolem Seekera když pronásleduje (vizuální efekt)
                if random.random() < 0.3:
                    particles.append({
                        'x': enemy['x'] + enemy_size / 2 + random.uniform(-5, 5), 
                        'y': enemy['y'] + enemy_size / 2 + random.uniform(-5, 5),
                        'radius': random.uniform(2, 5), 'life': 12,
                        'color': (100, 200, 100), 'dx': random.uniform(-2, 2), 'dy': random.uniform(-2, 2)
                    })

        # Aplikace knockbacku na nepřítele
        knockback_x = enemy.get('knockback_x', 0)
        knockback_y = enemy.get('knockback_y', 0)
        
        if knockback_x != 0 or knockback_y != 0:
            # Aplikace knockbacku (Osa X)
            new_enemy_x = enemy['x'] + knockback_x
            enemy_rect_x = pygame.Rect(new_enemy_x, enemy['y'], enemy_size, enemy_size)
            collision_enemy_x = enemy_rect_x.collidelist(walls) != -1 or enemy_rect_x.collidelist(locked_walls) != -1
            
            if not collision_enemy_x:
                enemy['x'] = new_enemy_x
            
            # Aplikace knockbacku (Osa Y)
            new_enemy_y = enemy['y'] + knockback_y
            enemy_rect_y = pygame.Rect(enemy['x'], new_enemy_y, enemy_size, enemy_size)
            collision_enemy_y = enemy_rect_y.collidelist(walls) != -1 or enemy_rect_y.collidelist(locked_walls) != -1
            
            if not collision_enemy_y:
                enemy['y'] = new_enemy_y
            
            # Postupné zeslabování knockbacku (friction)
            enemy['knockback_x'] *= 0.85
            enemy['knockback_y'] *= 0.85
        
        # Pohyb nepřítele a kolize se zdmi
        if move_x_enemy != 0 or move_y_enemy != 0:
            # Pohyb nepřítele a kolize se zdmi (Osa X)
            new_enemy_x = enemy['x'] + move_x_enemy
            enemy_rect_x = pygame.Rect(new_enemy_x, enemy['y'], enemy_size, enemy_size)
            collision_enemy_x = enemy_rect_x.collidelist(walls) != -1 or enemy_rect_x.collidelist(locked_walls) != -1
            
            if not collision_enemy_x:
                enemy['x'] = new_enemy_x
            elif enemy.get('is_dashing', False):
                enemy['is_dashing'] = False # Přerušení dashe při nárazu do zdi
                enemy['dash_cooldown'] = 40

            # Pohyb nepřítele a kolize se zdmi (Osa Y)
            new_enemy_y = enemy['y'] + move_y_enemy
            enemy_rect_y = pygame.Rect(enemy['x'], new_enemy_y, enemy_size, enemy_size)
            collision_enemy_y = enemy_rect_y.collidelist(walls) != -1 or enemy_rect_y.collidelist(locked_walls) != -1
            
            if not collision_enemy_y:
                enemy['y'] = new_enemy_y
            elif enemy.get('is_dashing', False):
                enemy['is_dashing'] = False
                enemy['dash_cooldown'] = 40

        ## Kontrola kolize (dotyku) mezi hráčem a nepřítelem
        if player_invincibility_timer == 0 and pygame.Rect(x + hitbox_offset, y + hitbox_offset, hitbox_size, hitbox_size).colliderect(pygame.Rect(enemy['x'], enemy['y'], enemy_size, enemy_size)):
            player_health = max(0, player_health - 1) # Hráč ztrácí jeden život
            shake_intensity = 15.0 # Spuštění otřesu obrazovky
            player_invincibility_timer = 60 # Krátká nesmrtelnost po zásahu

            # Vytvoření efektu bílých ultra-rychlých částic při zásahu hráče
            for _ in range(15):
                particles.append({
                    'x': x + size / 2, 'y': y + size / 2,
                    'radius': random.uniform(6, 12), 'life': 20,
                    'color': (255, 255, 255), # Bílá barva pro hráče
                    'dx': random.uniform(-18, 18), 'dy': random.uniform(-18, 18)
                })

            # Poznámka: Nepřítel už se neresetuje na startovní pozici, proletí skrz hráče
            
            # Pokud hráči dojdou životy, zobrazí se obrazovka smrti
            if player_health == 0:
                death_messages = [
                    "Worse than Gajdacz",
                    "Wasted!",
                    "Shoutout to Ondřej Pieter",
                ]
                dead_text = random.choice(death_messages)
                dead_surf = dead_font.render(dead_text, True, (115, 110, 110))
                dead_bg = pygame.Surface((width, height), pygame.SRCALPHA)
                dead_bg.fill((0, 0, 0, 220))
                screen.blit(dead_bg, (0, 0))
                screen.blit(dead_surf, ((width - dead_surf.get_width()) // 2, (height - dead_surf.get_height()) // 2))
                pygame.display.flip()
                pygame.time.delay(2000)

                # Respawn hráče na posledním checkpointu (léčivé platformě nebo startu)
                player_health = 6
                x = checkpoint_x
                y = checkpoint_y
                # Resetujeme VŠECHNY nepřátele na jejich startovní pozice
                for e in enemies:
                    e['x'], e['y'] = e['start_x'], e['start_y']
                    e['is_dashing'] = False
                    e['dash_cooldown'] = 30
                break # Přerušíme AI loop, protože hráč už je jinde a scéna se resetovala

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
    
    # Aplikace otřesu obrazovky (Screen Shake)
    temp_camera_x, temp_camera_y = camera_x, camera_y
    if shake_intensity > 0:
        camera_x += random.uniform(-shake_intensity, shake_intensity)
        camera_y += random.uniform(-shake_intensity, shake_intensity)
        shake_intensity = max(0, shake_intensity - 0.8) # Postupné utlumení otřesu

    # Vyčištění obrazovky temnou barvou (pozadí mimo mapu)
    screen.fill((10, 10, 10))
    
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

    # --- Vykreslení dekorací ---
    for deco in decorations:
        dx = int((deco['x'] - camera_x) * zoom)
        dy = int((deco['y'] - camera_y) * zoom)
        if -100 < dx < width + 100 and -100 < dy < height + 100:
            if deco['type'] == 'Crystal':
                pulse = (math.sin(pygame.time.get_ticks() / 600.0 + deco['pulse_offset']) + 1) / 2
                glow_size = int(32 * zoom * (1.0 + 0.3 * pulse))
                
                # Výběr textury podle podtypu
                c_tex = textura_crystal_blue
                if deco['subtype'] == 'Purple': c_tex = textura_crystal_blue_light
                elif deco['subtype'] == 'Teal': c_tex = textura_crystal_blue_dark
                
                crystal_scaled = pygame.transform.scale(c_tex, (int(32 * zoom), int(32 * zoom)))
                screen.blit(crystal_scaled, (dx, dy))
                
                # Záře krystalu (additive blend) s odpovídající barvou
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*deco['color'], int(45 * pulse)), (glow_size, glow_size), glow_size)
                screen.blit(glow_surf, (dx + int(16 * zoom) - glow_size, dy + int(16 * zoom) - glow_size), special_flags=pygame.BLEND_RGBA_ADD)
            elif deco['type'] == 'Vine':
                vine_scaled = pygame.transform.scale(textura_vine, (int(64 * zoom), int(64 * zoom)))
                vine_rot = pygame.transform.rotate(vine_scaled, deco['angle'])
                screen.blit(vine_rot, (dx, dy))
            elif deco['type'] == 'Cobweb':
                web_scaled = pygame.transform.scale(textura_cobweb, (int(64 * zoom), int(64 * zoom)))
                screen.blit(web_scaled, (dx, dy))

    # --- Vykreslení léčivých platforem ---
    curr_glow_t = pygame.time.get_ticks() / 1000.0
    hp_draw_size = int(block_size * zoom)
    for hp in healing_platforms:
        hp_draw_x = int((hp.x - camera_x) * zoom)
        hp_draw_y = int((hp.y - camera_y) * zoom)
        if -hp_draw_size < hp_draw_x < width + hp_draw_size and -hp_draw_size < hp_draw_y < height + hp_draw_size:
            screen.blit(textura_healing_platform, (hp_draw_x, hp_draw_y))
            # Pulzující modrá záře kolem platformy
            pulse = (math.sin(curr_glow_t * 2.5) + 1) / 2
            glow_r = int((hp_draw_size // 2) * (0.7 + 0.35 * pulse))
            if glow_r > 0:
                glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
                glow_alpha = int(35 + 30 * pulse)
                pygame.draw.circle(glow_surf, (30, 160, 255, glow_alpha), (glow_r, glow_r), glow_r)
                screen.blit(glow_surf, (hp_draw_x + hp_draw_size // 2 - glow_r, hp_draw_y + hp_draw_size // 2 - glow_r))

    # Vykreslení zábleskových kroužků po aktivaci platformy
    active_glows = []
    for glow in healing_platform_glow:
        glow['radius'] += 3.5
        glow['alpha'] = max(0, glow['alpha'] - 6)
        if glow['alpha'] > 0:
            active_glows.append(glow)
            gx = int((glow['x'] - camera_x) * zoom)
            gy = int((glow['y'] - camera_y) * zoom)
            gr = int(glow['radius'] * zoom)
            if gr > 0:
                ring_surf = pygame.Surface((gr * 2 + 4, gr * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(ring_surf, (80, 200, 255, int(glow['alpha'])), (gr + 2, gr + 2), gr, max(1, int(3 * zoom)))
                screen.blit(ring_surf, (gx - gr - 2, gy - gr - 2))
    healing_platform_glow = active_glows
    # --- Konec léčivých platforem ---

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

            # Jednotná barva jiskry pro všechny předměty (světle modrá)
            color_outer = (200, 255, 255)

            # Nakreslení vnějšího lesku a vnitřního jasného bodu (jádra jiskry)
            pygame.draw.circle(screen, color_outer, (item_dx, item_dy), sparkle_rad)
            pygame.draw.circle(screen, (255, 255, 255), (item_dx, item_dy), max(2, int(sparkle_rad * 0.4)))

    # --- Vykreslení slime blast projektilů ---
    for proj in slime_blast_projectiles:
        proj_draw_x = int((proj['x'] - camera_x) * zoom)
        proj_draw_y = int((proj['y'] - camera_y) * zoom)
        proj_radius = int(SLIME_BLAST_SIZE * zoom)
        
        # Kontrola viditelnosti na obrazovce
        if -proj_radius - 10 < proj_draw_x < width + proj_radius + 10 and -proj_radius - 10 < proj_draw_y < height + proj_radius + 10:
            # Vykreslení zářícího slime balku - modrý
            pygame.draw.circle(screen, (100, 180, 255), (proj_draw_x, proj_draw_y), proj_radius)
            pygame.draw.circle(screen, (150, 200, 255), (proj_draw_x - 2, proj_draw_y - 2), max(1, proj_radius - 3))
            # Vnější zásvit
            pygame.draw.circle(screen, (100, 180, 255), (proj_draw_x, proj_draw_y), proj_radius, 2)

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
    # Efekt blikání při nesmrtelnosti
    player_visible = True
    if player_invincibility_timer > 0:
        if (pygame.time.get_ticks() // 150) % 2 == 0:
            player_visible = False
            
    draw_x = int((x - camera_x) * zoom)
    draw_y = int((y - camera_y) * zoom)
    
    if player_visible:
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

    # --- Vykreslení a animace zbraně v ruce ---
    if current_weapon and is_attacking:
        # Použijeme zamknutý úhel útoku pro celou animaci
        angle_to_use = attack_angle
        
        # Základní parametry zbraně
        weapon_surf = WEAPON_TEXTURES[current_weapon]
        w_size = int(150 * zoom) # 2x větší vizuální velikost
        weapon_img = pygame.transform.scale(weapon_surf, (w_size, w_size))
        
        # Animace
        anim_offset_angle = 0
        anim_dist_offset = 0
        
        # Procento dokončení útoku (0.0 až 1.0)
        progress = 1.0 - (attack_timer / attack_duration)
        
        if current_weapon == 'Sword':
            anim_offset_angle = -60 + (progress * 120)
        elif current_weapon == 'Scythe':
            anim_offset_angle = 60 - (progress * 120)
        elif current_weapon == 'Spear':
            anim_dist_offset = math.sin(progress * math.pi) * 80 * zoom

        # --- Detekce zásahu (Hitbox logic) ---
        if attack_timer == attack_duration // 2:
            props = WEAPON_HITBOX_PROPS.get(current_weapon, {'range': 100, 'arc': 90, 'damage': 1})
            
            for enemy in enemies:
                # Přeskočíme mrtvé nepřátele, kteří čekají na respawn
                if enemy.get('respawn_timer', 0) > 0:
                    continue

                enemy_center_world_x = enemy['x'] + enemy_size / 2
                enemy_center_world_y = enemy['y'] + enemy_size / 2

                # Seznam bodů na konkrétním nepříteli, které budeme testovat pro zásah
                enemy_hitbox_points = [
                    (enemy['x'], enemy['y']),
                    (enemy['x'] + enemy_size, enemy['y']),
                    (enemy['x'], enemy['y'] + enemy_size),
                    (enemy['x'] + enemy_size, enemy['y'] + enemy_size),
                    (enemy_center_world_x, enemy_center_world_y)
                ]
                
                hit_registered = False
                for pt_x, pt_y in enemy_hitbox_points:
                    dx_e = pt_x - player_center_world_x
                    dy_e = pt_y - player_center_world_y
                    dist_e = math.hypot(dx_e, dy_e)
                    angle_e = math.degrees(math.atan2(dy_e, dx_e))
                    
                    # Výpočet rozdílu úhlů (normalizováno na -180 až 180 stupňů)
                    angle_diff = (angle_e - angle_to_use + 180) % 360 - 180
                    
                    # Pokud je alespoň jeden bod v dosahu a úhlu, započítáme zásah tomuto nepříteli
                    if dist_e <= props['range'] and abs(angle_diff) <= props['arc'] / 2:
                        hit_registered = True
                        break
                
                if hit_registered:
                    # Zásah konkrétního nepřítele!
                    enemy['hp'] -= props['damage']
                    
                    # Přidání nabití léčícího systému za zasažení nepřítele
                    mana_charges = min(MAX_MANA_CHARGES, mana_charges + charge_per_enemy_hit)
                    
                    # Aplikace knockbacku - hýbeme nepřítelem směrem od hráče
                    if (enemy['x'] - player_center_world_x) != 0 or (enemy['y'] - player_center_world_y) != 0:
                        knockback_angle = math.atan2(enemy['y'] - player_center_world_y, enemy['x'] - player_center_world_x)
                        knockback_strength = 15  # Síla knockbacku v pixelech
                        enemy['knockback_x'] = math.cos(knockback_angle) * knockback_strength
                        enemy['knockback_y'] = math.sin(knockback_angle) * knockback_strength
                    
                    # Vytvoření efektu krve/jisker na pozici nepřítele
                    for _ in range(15):
                        particles.append({
                            'x': enemy_center_world_x, 'y': enemy_center_world_y,
                            'radius': random.uniform(6, 12), 'life': 20,
                            'color': (255, 100, 100), # Červená barva pro zásah
                            'dx': random.uniform(-18, 18), 'dy': random.uniform(-18, 18)
                        })
                    
                    # Pokud nepřítel zemře, respawnujeme ho na jeho startovní pozici po prodlevě
                    if enemy['hp'] <= 0:
                        enemy['x'], enemy['y'] = enemy['start_x'], enemy['start_y']
                        enemy['hp'] = max_enemy_hp
                        enemy['is_dashing'] = False
                        enemy['respawn_timer'] = 7200 # 2 minuty při 60 FPS (120 sekund)

        # Rotace a vykreslení zbraně
        final_angle = -(angle_to_use + 90 + anim_offset_angle)
        rotated_weapon = pygame.transform.rotate(weapon_img, final_angle)
        
        dist = (player_draw_size // 2 + 80 * zoom) + anim_dist_offset
        rad = math.radians(angle_to_use + anim_offset_angle)
        w_x = (draw_x + player_draw_size // 2) + math.cos(rad) * dist
        w_y = (draw_y + player_draw_size // 2) + math.sin(rad) * dist
        
        w_rect = rotated_weapon.get_rect(center=(int(w_x), int(w_y)))
        screen.blit(rotated_weapon, w_rect)

    # Vždy aktualizujeme timer útoku (pokud zrovna útočíme), i když zbraň zrovna nevykreslujeme
    if is_attacking:
        attack_timer -= 1
        if attack_timer <= 0:
            is_attacking = False

    # --- Aktualizace a detekce kolize slime blast projektilů ---
    for proj in slime_blast_projectiles[:]:
        proj['x'] += proj['dx']
        proj['y'] += proj['dy']
        proj['age'] += 1
        
        # Kontrola zda projektil nedošel na konec svého dosahu
        if proj['age'] >= proj['max_age']:
            slime_blast_projectiles.remove(proj)
            continue
        
        # Kontrola kolize s rozbitelnou zdí
        proj_rect = pygame.Rect(proj['x'] - SLIME_BLAST_SIZE // 2, proj['y'] - SLIME_BLAST_SIZE // 2, SLIME_BLAST_SIZE, SLIME_BLAST_SIZE)
        for b_wall in breakable_walls[:]:
            if proj_rect.colliderect(b_wall['rect']):
                # Snížení HP rozbitelné zdi
                b_wall['hp'] -= 1
                
                # Vytvoření efektu částic při zásahu
                for _ in range(10):
                    particles.append({
                        'x': proj['x'], 'y': proj['y'],
                        'radius': random.uniform(3, 8), 'life': 15,
                        'color': (100, 180, 255),  # Modrá barva pro slime
                        'dx': random.uniform(-15, 15), 'dy': random.uniform(-15, 15)
                    })
                
                # Pokud má zeď 0 nebo méně HP, odstraníme ji
                if b_wall['hp'] <= 0:
                    breakable_walls.remove(b_wall)
                
                # Odstraníme projektil
                slime_blast_projectiles.remove(proj)
                break
        else:
            # Pokud projektil nenarazil na zeď, kontrolujeme kolizi se stěnami
            collision_with_wall = False
            for wall in walls:
                if proj_rect.colliderect(wall):
                    collision_with_wall = True
                    break
            
            if collision_with_wall:
                # Vytvoření efektu částic
                for _ in range(8):
                    particles.append({
                        'x': proj['x'], 'y': proj['y'],
                        'radius': random.uniform(2, 6), 'life': 12,
                        'color': (100, 180, 255),
                        'dx': random.uniform(-10, 10), 'dy': random.uniform(-10, 10)
                    })
                slime_blast_projectiles.remove(proj)

    # --- Vykreslení nepřátel ---
    player_center_world_x = x + size / 2
    player_center_world_y = y + size / 2
    for enemy in enemies:
        # Přeskočíme nepřátele, kteří čekají na respawn
        if enemy.get('respawn_timer', 0) > 0:
            continue
            
        # --- Zjištění viditelnosti pro konkrétního nepřítele ---
        vision_radius = 2000
        enemy_center_world_x = enemy['x'] + enemy_size / 2
        enemy_center_world_y = enemy['y'] + enemy_size / 2

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
                (enemy['x'], enemy['y']),
                (enemy['x'] + enemy_size, enemy['y']),
                (enemy['x'], enemy['y'] + enemy_size),
                (enemy['x'] + enemy_size, enemy['y'] + enemy_size)
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

        if enemy_visible:
            # Výpočet úhlu k hráči pro rotaci nepřítele
            dx_e = player_center_world_x - enemy_center_world_x
            dy_e = player_center_world_y - enemy_center_world_y
            angle_e = math.degrees(math.atan2(dy_e, dx_e))
            
            enemy_type = enemy.get('type', 'Fly')
            
            # Efekt bzučení pouze pro mouchy (Fly)
            if enemy_type == 'Fly':
                buzz_t = pygame.time.get_ticks() * 0.02 + enemy.get('buzz_offset', 0)
                buzz_x = math.sin(buzz_t) * 4
                buzz_y = math.cos(buzz_t * 1.3) * 4
            else:
                # Seekers nemají bzučení - pohybují se hladce
                buzz_x = 0
                buzz_y = 0
            
            enemy_draw_x = int((enemy['x'] + buzz_x - camera_x) * zoom)
            enemy_draw_y = int((enemy['y'] + buzz_y - camera_y) * zoom)
            
            # Výběr správné textury podle typu nepřítele
            if enemy_type == 'Seeker':
                enemy_texture = textura_seeker
                rotation_angle = angle_e  # Seeker se otáčí více
            else:  # Fly
                enemy_texture = textura_nepritel
                rotation_angle = -angle_e  # Fly má opačný smysl rotace
            
            # Rotace textury
            rotated_enemy = pygame.transform.rotate(enemy_texture, rotation_angle)
            
            # Vycentrování rotované textury
            enemy_rect = rotated_enemy.get_rect(center=(
                enemy_draw_x + int(enemy_draw_size / 2),
                enemy_draw_y + int(enemy_draw_size / 2)
            ))
            
            screen.blit(rotated_enemy, enemy_rect)


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

    # --- ZOBRAZENÍ HITBOXŮ (Debug) ---
    if show_hitboxes:
        # Hitbox hráče (zelený)
        p_hit_rect = pygame.Rect(
            int((x + hitbox_offset - camera_x) * zoom),
            int((y + hitbox_offset - camera_y) * zoom),
            int(hitbox_size * zoom),
            int(hitbox_size * zoom)
        )
        pygame.draw.rect(screen, (0, 255, 0), p_hit_rect, 2)

        # Hitboxy nepřátel (červené)
        for enemy in enemies:
            if enemy.get('respawn_timer', 0) == 0:
                e_hit_rect = pygame.Rect(
                    int((enemy['x'] - camera_x) * zoom),
                    int((enemy['y'] - camera_y) * zoom),
                    int(enemy_size * zoom),
                    int(enemy_size * zoom)
                )
                pygame.draw.rect(screen, (255, 0, 0), e_hit_rect, 2)

        # Dosah sbírání předmětů (žlutý)
        for item in items_on_ground:
            item_dx = int((item['x'] - camera_x) * zoom)
            item_dy = int((item['y'] - camera_y) * zoom)
            pickup_rad = int(150 * zoom) # Dosah je 150
            pygame.draw.circle(screen, (255, 255, 0), (item_dx, item_dy), pickup_rad, 1)

        # Hitbox léčivých platforem (modrý)
        for hp in healing_platforms:
            hp_rect = pygame.Rect(
                int((hp.x - camera_x) * zoom),
                int((hp.y - camera_y) * zoom),
                int(hp.width * zoom),
                int(hp.height * zoom)
            )
            pygame.draw.rect(screen, (0, 100, 255), hp_rect, 1)

        # Hitbox útoku zbraně (modrý výsek)
        if is_attacking and current_weapon:
            props = WEAPON_HITBOX_PROPS.get(current_weapon)
            if props:
                range_px = int(props['range'] * zoom)
                arc_deg = props['arc']
                
                # Střed hráče v souřadnicích obrazovky
                pcx = int((x + size / 2 - camera_x) * zoom)
                pcy = int((y + size / 2 - camera_y) * zoom)
                
                # Výpočet bodů pro vykreslení výseče útoku
                start_rad = math.radians(attack_angle - arc_deg / 2)
                end_rad = math.radians(attack_angle + arc_deg / 2)
                
                points = [(pcx, pcy)]
                steps = 15
                for i in range(steps + 1):
                    angle = start_rad + (end_rad - start_rad) * (i / steps)
                    px = pcx + math.cos(angle) * range_px
                    py = pcy + math.sin(angle) * range_px
                    points.append((px, py))
                
                if len(points) > 2:
                    # Vykreslení obrysu výseče útoku
                    pygame.draw.polygon(screen, (0, 150, 255), points, 2)

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


    # Zobrazení zdraví hráče (animované orby)
    orb_spacing = 35
    icon_width = 50
    padding = 10
    
    # Výpočet šířky pozadí pro zdraví podle toho, kolik orbů zbývá
    total_health_width = icon_width + padding + ((player_health - 1) * orb_spacing) if player_health > 1 else icon_width
    bg_width = total_health_width + padding * 2
    bg_height = 50 + padding * 2
    
    health_bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    pygame.draw.rect(health_bg, (30, 40, 70, 210), (0, 0, bg_width, bg_height), border_radius=12)
    pygame.draw.rect(health_bg, (80, 140, 255), (0, 0, bg_width, bg_height), 2, border_radius=12)
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

    # --- HUD zbrane (levá strana, nad zdravím) ---
    if current_weapon and current_weapon != "None":
        weapon_hud_y = health_bg_y - 80
        weapon_slot_w = 220
        weapon_slot_h = 64
        # Vytvoření povrchu pro pozadí slotu zbraně
        weapon_slot_bg = pygame.Surface((weapon_slot_w, weapon_slot_h), pygame.SRCALPHA)
        weapon_slot_bg.fill((10, 20, 50, 200))
        pygame.draw.rect(weapon_slot_bg, (80, 160, 255), (0, 0, weapon_slot_w, weapon_slot_h), 2, border_radius=10)

        screen.blit(weapon_slot_bg, (10, weapon_hud_y))

        # Ikona zbraně (aktuální textura zbraně)
        icon_pulse = (math.sin(current_time * 3) + 1) / 2
        icon_size = max(8, int(50 + icon_pulse * 4))
        
        if current_weapon in WEAPON_TEXTURES:
            weapon_tex = WEAPON_TEXTURES[current_weapon]
        else:
            weapon_tex = textura_weapon_icon # Záložní ikona
            
        weapon_icon_scaled = pygame.transform.scale(weapon_tex, (icon_size, icon_size))
        screen.blit(weapon_icon_scaled, (14, weapon_hud_y + (weapon_slot_h - icon_size) // 2))

        # Název a přepínací nápověda
        weapon_name_font = pygame.font.SysFont(None, 28)
        w_name_surf = weapon_name_font.render(current_weapon, True, (180, 220, 255))
        screen.blit(w_name_surf, (70, weapon_hud_y + 10))
        switch_hint = weapon_name_font.render("[1] [2] [3]", True, (80, 120, 180))
        screen.blit(switch_hint, (70, weapon_hud_y + 36))

    # --- HUD dashe (vedle HUDu zbraně) ---
    if "Feather" in inventory:
        dash_hud_x = 10 + (220 + 10 if (current_weapon and current_weapon != "None") else 0)
        dash_hud_y = health_bg_y - 80
        dash_size = 64
        
        # Pozadí slotu dashe
        dash_bg = pygame.Surface((dash_size, dash_size), pygame.SRCALPHA)
        dash_bg.fill((10, 20, 50, 200))
        pygame.draw.rect(dash_bg, (80, 160, 255), (0, 0, dash_size, dash_size), 2, border_radius=10)
        screen.blit(dash_bg, (dash_hud_x, dash_hud_y))
        
        # Ikona pírka
        feather_icon_hud = pygame.transform.scale(textura_feather, (40, 40))
        if player_dash_cooldown > 0:
            feather_icon_hud.set_alpha(100) # Ztlumení při cooldownu
        screen.blit(feather_icon_hud, (dash_hud_x + 12, dash_hud_y + 12))
        
        # Indikátor cooldownu (kruhový nebo bar)
        if player_dash_cooldown > 0:
            cooldown_pct = player_dash_cooldown / DASH_COOLDOWN_TIME
            cd_height = int(dash_size * cooldown_pct)
            cd_surf = pygame.Surface((dash_size, cd_height), pygame.SRCALPHA)
            cd_surf.fill((255, 255, 255, 60))
            screen.blit(cd_surf, (dash_hud_x, dash_hud_y + (dash_size - cd_height)))

    # --- Zobrazení nabití many (top-left) ---
    try:
        mana_x = 10
        mana_y = 10
        heal_font = pygame.font.SysFont(None, 18)
        mana_label = heal_font.render("MANA", True, (100, 180, 255))
        screen.blit(mana_label, (mana_x, mana_y))
        charge_radius = 6
        charges_x = mana_x + 50
        charges_y = mana_y + 8
        for i in range(MAX_MANA_CHARGES):
            hx = charges_x + i * (charge_radius * 3)
            hy = charges_y
            if mana_charges > i:
                fill_col = (100, 180, 255)
            else:
                fill_col = (30, 40, 60)
            pygame.draw.circle(screen, fill_col, (hx, hy), charge_radius)
            pygame.draw.circle(screen, (100, 180, 255), (hx, hy), charge_radius, 1)
    except Exception:
        pass
    
    # --- Zobrazení notifikací o sebrání předmětů ---
    # --- Secret easter egg display (top-right) ---
    try:
        # Draw a small visible button in the top-right corner
        btn_w, btn_h = 28, 18
        btn_x = width - btn_w - 6
        btn_y = 6
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        btn_color = (100, 180, 255) if show_big_message else (60, 90, 130)
        btn_surf.fill(btn_color)
        pygame.draw.rect(btn_surf, (200, 220, 255), (0, 0, btn_w, btn_h), 1, border_radius=3)
        screen.blit(btn_surf, (btn_x, btn_y))

        if show_big_message:
            # Full-screen blessing message
            try:
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 200))
                big_font = pygame.font.SysFont(None, 64)
                msg = "Congrats you just got blessed by Big Yahu."
                text_surf = big_font.render(msg, True, (255, 230, 150))
                tw, th = text_surf.get_size()
                overlay.blit(text_surf, ((width - tw) // 2, (height - th) // 2))
                screen.blit(overlay, (0, 0))
                # small hint to dismiss
                hint = font.render("Click or press any key to dismiss", True, (200,200,200))
                hw, hh = hint.get_size()
                screen.blit(hint, ((width - hw) // 2, (height - th) // 2 + th + 16))
            except Exception:
                pass
    except Exception:
        pass
    notif_y = height - 80 # Výchozí Y pozice v pravém dolním rohu
    active_notifications = []
    
    for notif in pickup_notifications:
        time_alive = current_time - notif['time']
        
        # Oznámení zůstane na obrazovce 3 sekundy
        if time_alive < 3.0:
            # Postupné blednutí (fade out) během poslední sekundy
            if time_alive > 2.0:
                notif['alpha'] = max(0, int(255 * (3.0 - time_alive)))
                
            # Připravíme text a barvu podle typu předmětu
            if notif['type'] == "Key":
                item_name = "Golden Key"
                notif_color = (255, 215, 0)
            elif notif['type'] == "Sword":
                item_name = "Sword"
                notif_color = (80, 160, 255)
            elif notif['type'] == "Spear":
                item_name = "Spear"
                notif_color = (0, 220, 220)
            elif notif['type'] == "Scythe":
                item_name = "Scythe"
                notif_color = (160, 80, 255)
            elif notif['type'] == "Feather":
                item_name = "Feather"
                notif_color = (240, 245, 255)
            else:
                item_name = notif['type']
                notif_color = (255, 255, 255)
            notif_text = health_font.render(f"+ {item_name}", True, notif_color)
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
                icon_copy = textura_klic_icon.copy()
                icon_copy.set_alpha(notif['alpha'])
                screen.blit(icon_copy, (draw_x + 10, notif_y + (bg_height - 50) // 2))
            elif notif['type'] == "Glitter Slime Ball":
                icon_copy = textura_glitter_ball.copy()
                icon_copy.set_alpha(notif['alpha'])
                screen.blit(icon_copy, (draw_x + 10, notif_y + (bg_height - 50) // 2))
            elif notif['type'] == "Feather":
                icon_copy = textura_feather_icon.copy()
                icon_copy.set_alpha(notif['alpha'])
                screen.blit(icon_copy, (draw_x + 10, notif_y + (bg_height - 50) // 2))
            elif notif['type'] == "Slime Blast":
                icon_copy = textura_slime_blast_icon.copy()
                icon_copy.set_alpha(notif['alpha'])
                screen.blit(icon_copy, (draw_x + 10, notif_y + (bg_height - 50) // 2))
            elif notif['type'] in WEAPON_TEXTURES:
                icon_copy = WEAPON_TEXTURES[notif['type']].copy()
                icon_copy.set_alpha(notif['alpha'])
                icon_copy = pygame.transform.scale(icon_copy, (50, 50))
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
        pygame.draw.rect(fps_bg, (30, 40, 70, 180), (0, 0, fps_bg.get_width(), fps_bg.get_height()), border_radius=8)
        pygame.draw.rect(fps_bg, (80, 140, 255), (0, 0, fps_bg.get_width(), fps_bg.get_height()), 2, border_radius=8)
        screen.blit(fps_bg, (width - fps_text.get_width() - 20, 10))
        screen.blit(fps_text, (width - fps_text.get_width() - 15, 13))

    # Brightness overlay (Překrytí obrazovky bílou barvou pro zvýšení jasu přes nastavení)
    if brightness > 0:
        brightness_overlay = pygame.Surface((width, height))
        brightness_overlay.fill((255, 255, 255))
        brightness_overlay.set_alpha(brightness) # Nastavení úrovně průhlednosti bílé plochy
        screen.blit(brightness_overlay, (0, 0))

    # --- Atmosférické částice (motes) ---
    for mote in atmospheric_motes:
        mote['y'] -= mote['speed']
        mote['wobble'] += 0.02
        mote['x'] += math.sin(mote['wobble']) * 0.4
        
        # Resetování pozice motes
        map_w = len(maze_layout[0]) * block_size
        map_h = len(maze_layout) * block_size
        if mote['y'] < 0: mote['y'] = map_h
        if mote['x'] < 0: mote['x'] = map_w
        if mote['x'] > map_w: mote['x'] = 0
        
        mx = int((mote['x'] - camera_x) * zoom)
        my = int((mote['y'] - camera_y) * zoom)
        if 0 < mx < width and 0 < my < height:
            pygame.draw.circle(screen, (100, 200, 255, mote['alpha']), (mx, my), int(mote['radius'] * zoom))

    draw_custom_cursor(screen, mouse_x, mouse_y)

    # Tato funkce vezme vše, co jsme během snímku nakreslili do paměti a plácne to na monitor naráz
    pygame.display.flip()

    # Navrácení původní pozice kamery (zrušení offsetu z otřesu pro další výpočty pohybu)
    camera_x, camera_y = temp_camera_x, temp_camera_y
    
    # Omezovač FPS - zajišťuje, že hra nepoběží rychleji než na určený cíl (target_fps)
    clock.tick(target_fps)

# Když se smyčka ukončí (running = False), bezpečně vypneme pygame okno
pygame.quit()