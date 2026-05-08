# Flappy Bird – byggt med Python 🐦

Hej Alekh! 👋 Välkommen till ditt första Pygame-projekt! Den här README-filen guidar dig genom koden och förklarar allt på ett enkelt sätt. Du kommer att fatta det här – jag lovar!

---

## Innehållsförteckning

1. [Vad är Pygame?](#vad-är-pygame)
2. [Klasser – recept för figurer](#klasser--recept-för-figurer)
3. [Viktiga funktioner](#viktiga-funktioner)
4. [Färger och koordinater](#färger-och-koordinater)
5. [Hur du kör spelet](#hur-du-kör-spelet)
6. [Felsökning](#felsökning)

---

## Vad är Pygame?

Pygame är som en **verktygslåda för spel**. Precis som en snickare använder hammare och såg för att bygga ett hus, använder vi Pygame för att:

- **Rita figurer** på skärmen (fåglar, rör, bakgrund)
- **Lyssna efter knapptryck** (t.ex. SPACE-tangenten)
- **Skapa animationer** (fågeln rör sig, rören glider)

I toppen av filen skriver vi `import pygame` – det betyder "hämta verktygslådan så vi kan använda den".

---

## Klasser – recept för figurer

En **klass** är som ett **recept**. Om du vill baka en kaka behöver du ett recept som säger vad som ska vara i och hur det ska göras. I koden använder vi två klasser:

### Klassen `Bird` – receptet för fågeln 🐤

Klassen Bird beskriver allt om fågeln:

```python
class Bird:
    def __init__(self):
        self.x = 100        # var fågeln startar (höger/vänster)
        self.y = HEIGHT // 2  # var fågeln startar (upp/ner)
        self.radius = 15    # hur stor fågeln är
        self.vel_y = 0      # hastighet uppåt/nedåt (börjar stilla)
```

- **`__init__`** – det här är "receptets grund". När vi säger `Bird()` skapas en helt ny fågel med alla egenskaper ovan.
- **`self.x` och `self.y`** – fågelns position på skärmen. `x` är vänster-höger, `y` är upp-ner.
- **`self.radius`** – hur stor fågelns cirkel är.
- **`self.vel_y`** – hastigheten uppåt eller nedåt. Börjar på 0 (stilla).

### Klassen `Pipe` – receptet för rören 🌿

Klassen Pipe skapar hinder (rören) som fågeln måste undvika:

```python
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(120, HEIGHT - 200)
```

- Rören har en **öppning (gap)** på en slumpmässig höjd – därför ser det olika ut varje gång du spelar!
- Varje rör är egentligen **två rektanglar**: ett topprör (som hänger från taket) och ett bottenrör (som står på marken).
- Rören rör sig från **höger till vänster** – precis som i en biljard där bollen rullar mot dig.

---

## Viktiga funktioner

### `jump()` – fågeln flaxar! 🦅

```python
def jump(self):
    self.vel_y = JUMP_STRENGTH  # JUMP_STRENGTH = -8.5
```

När du trycker på SPACE ändras `vel_y` till **-8.5**. Minustecknet betyder **uppåt** (som att hissen går uppåt istället för neråt). Tänk på en boll du kastar upp i luften – först far den upp, sen stannar den, sen faller den ner. Det är precis så fågeln fungerar!

### `update()` – spelets motor ⚙️

```python
def update(self):
    self.vel_y += GRAVITY      # GRAVITY = 0.5
    self.y += self.vel_y
```

Det här anropas **varje bildruta** (60 gånger per sekund!). Tänk på det som en **slowmotion-film där varje bildruta är ett litet steg**:

1. **Gravity drar neråt**: Varje bildruta lägger vi till 0.5 till `vel_y`. Första rutan: 0 → 0.5. Andra rutan: 0.5 → 1.0. Tredje: 1.0 → 1.5. Det blir tyngre och tyngre – precis som i verkligheten!
2. **Fågeln flyttas**: `self.y += self.vel_y` flyttar fågeln baserat på hastigheten. Om `vel_y` är negativ → uppåt. Om `vel_y` är positiv → nedåt.

### `colliderect` – krockkollen 💥

```python
if bird.rect().colliderect(top) or bird.rect().colliderect(bottom):
    game_over = True
```

Datorn är inte smart – den ser inte former som vi gör. Istället ritar den en **osynlig rektangel runt fågeln** och en **osynlig rektangel runt varje rör**. Sen kollar den: "Nuddar någon av rektanglarna varandra?"

- **`bird.rect()`** – hämtar fågelns osynliga låda
- **`colliderect(other_rect)`** – kollar om två lådor nuddar varandra

Det är som när du leker med kartonglådor – om två lådor rör vid varandra har du en krock!

---

## Färger och koordinater

### Koordinatsystemet 🎯

I datorspel börjar **punkt (0,0) längst upp i vänstra hörnet** – inte nere till vänster som i matteboken!

```
(0,0) ──────────→ x (ökar höger)
  │
  │
  ↓
  y (ökar NERÅT)
```

Så om du vill placera något längre ner på skärmen ökar du `y`. Vill du flytta höger ökar du `x`.

### RGB-färger 🎨

Alla färger på datorn blandas av **rött, grönt och blått** (RGB). Varje färg får ett värde mellan 0 och 255:

| Färg | RGB |
|------|-----|
| Svart | `(0, 0, 0)` |
| Vitt | `(255, 255, 255)` |
| Gul (fågeln) | `(255, 230, 50)` – mycket rött och grönt, lite blått |
| Himmelblå | `(135, 206, 235)` |

Du kan experimentera: ändra siffrorna och se vad som händer! Testa `GREEN = (255, 0, 0)` så blir rören röda istället – förstår du varför? (Ledtråd: mycket rött, inget grönt!)

---

## Hur du kör spelet

### Steg 1: Installera Pygame

Öppna terminalen (PowerShell på Windows) och skriv:

```bash
pip install pygame
```

Det är som att ladda ner en app – du gör det bara en gång, sen finns Pygame på din dator för alltid.

### Steg 2: Kör spelet

I terminalen, navigera till mappen där filen finns och skriv:

```bash
python flappy_bird.py
```

Byt ut `flappy_bird.py` mot vad du nu har döpt filen till.

### Steg 3: Spela!

- **SPACE** – fågeln flaxar uppåt
- **SPACE (efter game over)** – starta om
- **ESC** – avsluta spelet

---

## Felsökning

| Problem | Lösning |
|---------|---------|
| "pip finns inte" | Prova `pip3 install pygame` eller `python -m pip install pygame` |
| "module not found" | Du har inte installerat Pygame. Kör `pip install pygame` igen |
| Spelet startar inte | Kolla att du är i rätt mapp i terminalen. Skriv `dir` för att se filerna |
| Fågeln rör sig inte | Är du i `game_over`-läge? Tryck SPACE för att starta om |

---

Lycka till, Alekh! 🎉 Du fixar det här. Om något känns krångligt – läs en gång till, testa att ändra en siffra i koden, och se vad som händer. Det är så alla lär sig – genom att experimentera!

**Du är grym som ger dig på det här!** 💪
