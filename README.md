# Roadcross

A retro-inspired, arcade Frogger-style game built with Python and Pygame where you navigate a turtle across busy roads to rescue captured hatchlings from alien kidnappers.

All graphics—including the player, vehicles, stone obstacles, cutscenes, and environments—are rendered **100% programmatically** using Pygame shapes and mathematical functions, requiring zero external image or asset files.

---

## Key Features

* **Procedural Graphics:** Built entirely without asset files. No missing textures, rotation artifacts, or background box clipping.
* **Cinematic Rescue Scenes:** Successfully reaching the top triggers a sequence where your turtle rescues a hatchling, fights off the alien captor, and sends their UFO flying.
* **Dynamic World & Themes:** Smooth vertical transitions through distinct thematic biomes including Suburbs, Golden Hour, Night City, Desert, Arctic, and Cyberpunk.
* **Escalating Difficulty:** Traffic speeds scale as you save more turtles, featuring bidirectional two-way traffic (after 20 saves) and random stone obstacles (after 40 saves).
* **Story & Cutscenes:** Features an animated main menu with flying UFOs, level banners, custom HUD elements, interactive win/lose screens, and alien dialogue.

---

## File Structure

```text
.
├── main.py          # Game loop, state machine, and main application entry point
├── constants.py     # Screen dimensions, lane coordinates, and theme color palettes
├── player.py        # Player turtle class, 4-way movement, and collision bounds
├── cars.py          # Procedural car generators (Sedan, SUV, Taxi, Truck, Sportscar) and traffic manager
├── finish_scene.py  # Animated rescue sequence state machine and UFO/alien rendering
├── endings.py       # Cinematic Game Over sequence and 100-turtle victory screen
├── stones.py        # Procedural stone obstacle generator and collision logic
├── road.py          # Background and road lane renderer per theme
└── ui.py            # HUD, start menu, level banner overlay, and Game Over panel

```

---

## Prerequisites

* Python 3.8 or higher
* Pygame 2.0 or higher

---

## Installation & Setup

1. **Clone or download the repository** to your local machine.
2. **Install Pygame** using pip:
```bash
pip install pygame

```


3. **Run the game**:
```bash
python main.py

```



---

## How to Play

### Controls

* **Arrow Keys ($\uparrow, \downarrow, \leftarrow, \rightarrow$):** Move your turtle up, down, left, or right.
* **SPACE:** Start the game, advance dialogue/cutscenes, or restart after a game over.

### Objective

1. Dodge oncoming vehicles and stone hazards to reach the top safe zone.
2. Trigger the rescue sequence to defeat the alien and save the hatchling.
3. Advance through rotating environments and test your reaction speed as traffic speeds increase.
