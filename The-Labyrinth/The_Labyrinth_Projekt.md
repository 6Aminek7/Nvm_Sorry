# The Labyrinth

## Popis

The Labyrinth je 2D hra vytvořená v Pygame, ve které hráč prozkoumává velký labyrint, hledá cestu ke východu, sbírá předměty a vyhýbá se nepřátelům.

## Cíl hry

- Najít cestu na konec labyrintu.
- Překonat zablokované oblasti a otevřít zamčené dveře pomocí klíčů.
- Přežít útoky nepřátel a spravovat svoje zdraví.

## Hratelnost a mechaniky

- Labyrint je tvořen jako mřížka, kde "W" představuje zdi a průchodnou cestu.
- Hráč může sbírat různé předměty, včetně klíčů, zbraní a léčivých platform.
- Inventář ukazuje nasbírané věci a zbraně, které lze vybavit.
- Pravým tlačítkem myši lze aktivovat dash, pokud je v inventáři "Feather".
- Levé tlačítko myši provádí útok, pokud je hráč vybaven zbraní.

## Ovládání

- `B` - otevřít inventář
- `SPACE` - sebrat předmět v dosahu
- `1`, `2`, `3` - přepínat mezi dostupnými zbraněmi
- `ESC` - pauza / nabídka
- levé tlačítko myši - útok
- pravé tlačítko myši - dash / rychlý přesun (pokud hráč vlastní "Feather")

## Požadavky

- Python 3
- Knihovna `pygame`

## Spuštění

1. Nainstalujte `pygame` pomocí `pip install pygame`.
2. Spusťte `The_Labyrinth/The_Labyrinth.py`.

## Struktura projektu

- `The_Labyrinth/The_Labyrinth.py` - hlavní herní skript
- `The_Labyrinth/Saves/` - adresář pro ukládání pozic a herních dat
- `The_Labyrinth/textures/` - grafické zdroje pro herní prvky

## Poznámky

Tento dokument vychází z projektu uvedeného v tomto repozitáři a z hlavního herního kódu. Hra je postavena jako první větší experiment v Pygame a kombinuje labyrintové procházení s prvky inventáře a boje.