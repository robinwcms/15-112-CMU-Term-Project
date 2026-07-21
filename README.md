# Zombie Wars

A top-down survival shooter built in **Python** as my term project for **Carnegie Mellon's 15-112 (Fundamentals of Programming and Computer Science)**.

Every map is procedurally generated with the **diamond-square algorithm**, so no two playthroughs are the same. The goal is simple: rack up as many kills as you can before the zombies get you.

## About this project

I built Zombie Wars entirely in the **CMU Graphics library** (the `cmu-graphics` animation framework taught in 15-112). It's a deliberately minimal, education-focused library — it has no game engine, no physics, no built-in collision system, no asset pipeline, and no sprite tooling like you'd get in Unity or GameMaker. Everything here — the game loop, collision detection, weapon systems, enemy AI, procedural map generation, and inventory — is implemented from scratch on top of a basic drawing API. I also hand-drew all the sprites and environment art in Piskel.

Working inside those constraints was the point: it forced me to actually understand how the underlying systems work rather than calling an engine's built-in functions.

## Features

- **Procedurally generated maps** — I generate a 129×129 heightmap with the diamond-square algorithm, then use that noise map as a spawn distribution: the values determine where trees, zombies, crates, and loot appear. Because diamond-square produces smooth, spatially-correlated terrain (rather than uniform randomness), the world clusters naturally and looks different every run.
- **Multiple weapons** — rifle, shotgun, and melee, each with its own ammo and behavior.
- **Loot system** — open crates to find ammo and health pickups.
- **Enemy AI and combat** — zombies pursue the player; combat, collisions, and scoring are all custom-built.
- **Original pixel art** — all sprites and backgrounds hand-drawn in Piskel.

## Controls

| **Input**               | **Action**                               |
|-------------------------|------------------------------------------|
| `W` `A` `S` `D`         | Move (forward / left / back / right)     |
| Mouse                   | Aim                                      |
| Left Click              | Shoot                                    |
| `1`                     | Switch to rifle                          |
| `2`                     | Switch to shotgun                        |
| Double-tap `1` or `2`   | Unequip and switch to melee              |
| `E` (near a crate)      | Open crate                               |
| `E` (again)             | Pick up the item inside (if available)   |

### Loot types

- 🔵 **Blue circle** — +10 rifle ammo
- 🔴 **Red circle** — +5 shotgun ammo
- 🟢 **Green circle** — +10 health

## Setup

```bash
pip install cmu-graphics pillow
```

Keep `termproject.py` in the same folder as the `background/`, `sprites/`, and `screens/` directories, then run:

```bash
python termproject.py
```

## Changelog

Recent fixes to make the project run cleanly on any machine (gameplay unchanged):

- Asset paths are now relative to the script instead of hardcoded to a local user directory, so the game runs anywhere.
- Fixed a bug where pressing `E` with no crate nearby silently checked the last crate in the world (added an index guard).
- Switching weapons now correctly clears active bullets/pellets (previously assigned to a local variable and had no effect).
- Corrected two `==` / `=` typos in the rifle and shotgun reload edge cases.
- Fixed a collision-check bug where zombie collision used a leftover crate coordinate instead of the zombie's own position.
- Fixed a zombie attack-timer reset that was writing to an unused attribute.
- Removed a dead condition in the tree generator that could never evaluate true (spawn rate unchanged).

---

*Built solo for CMU 15-112, Summer 2024.*
