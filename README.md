Game Description:
Zombie Wars is a top down game that features a procedurally generated map. Sprites such as trees, zombies, loot crates, and possible loot are all procedurally generated and differ every time. The objective of the game is to get as many kills as possible without dying.

Instructions:

W: Forward
S: Backward
A: Left
D: Right

Press 1: Switch weapon to rifle
Press 2: Switch weapon to shotgun
Double press 1 or 2: Unequip any weapon and switch to melee

Aim/shoot:
Move mouse cursor to aim
Left click to shoot

Press E to open crates when you are in range

Press E again to pick up the item in the crate (if there is any) 

Possible loot:
Blue circle (+ 10 ammo for rifle)
Red Circle (+ 5 ammo for shotgun)
Green Circle (+ 10 health)









---

Setup (fixed version):
1. pip install cmu-graphics pillow
2. Keep termproject.py in the same folder as background/, sprites/, and screens/
3. python termproject.py

Changelog (bugfixes, gameplay unchanged):
- Asset paths are now relative to the script instead of hardcoded to C:/Users/robin, so the game runs on any machine
- Pressing E with no crate nearby no longer secretly checked the last crate in the world (index -1 guard)
- Switching weapons now actually clears bullets/pellets (was assigning to a local variable)
- Two "==" typos in the rifle/shotgun reload edge cases changed to "=" assignments
- isLegal's zombie collision check used crate.crateY left over from the crate loop; now uses zombie.zombieY
- Zombie attack timer reset was writing to an unused app.zombieTimer attribute; now resets zombie.timer
- Removed an impossible condition in the tree generator (val[-2] == '-1' can never be true for a single character)
