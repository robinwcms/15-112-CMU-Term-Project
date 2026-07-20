#Citation

#https://en.wikipedia.org/wiki/Diamond-square_algorithm
#Diamond square algorithm english explanation/visual explanation

#demo4-editing-pixels.py
#Generating a map based on pixels RGB

#https://www.piskelapp.com/p/create/sprite
#Used to draw sprites

#https://academy.cs.cmu.edu/exercise/25257
#used getRadiusAndAngleToEndpoint function from the dot splotter homework

#https://cooltext.com/Render-Image?RenderID=463165902034317&LogoId=4631659020
#Used for texts

from cmu_graphics import *
import math
import random
from PIL import Image
import os

# Load assets relative to this file so the game runs on any machine
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))
def loadImage(*parts):
    return CMUImage(Image.open(os.path.join(ASSET_DIR, *parts)))

#Background
normalGrass = loadImage("background", "grass.png")

#Trees
trunk = loadImage("background", "trees", "treetrunk.png")
leaves = loadImage("background", "trees", "leaves.png")
#crate
unbrokenCrate = loadImage("background", "crates", "crate.png")
brokenCrate = loadImage("background", "crates", "crate(broken).png")
crateButton = loadImage("background", "crates", "crateButton.png")

#Player 
player = loadImage("sprites", "player", "player(passive).png")
player1 = loadImage("sprites", "player", "player(rifle).png")
player2 = loadImage("sprites", "player", "player(grenadelauncher).png")


playerPunch = loadImage("sprites", "player", "player(punch)100.png")
playerList = [player,player1,player2]

#Zombie 
zombiePassive = loadImage("sprites", "Zombies", "zombie(passive).png")
zombiePunch = loadImage("sprites", "Zombies", "zombie(punch2).png")

#Bullet
bullet = loadImage("sprites", "Bullet", "bullet.png")

#Powerups
shotShell = loadImage("sprites", "powerups", "shell.png")
rifleShell = loadImage("sprites", "powerups", "rifleAmmo.png")
healing = loadImage("sprites", "powerups", "hp.png")

#Screens
gameStartBackdrop = loadImage("screens", "Intro", "intro.png")
gameStartText = loadImage("screens", "Intro", "introTitle.png")
playButton = loadImage("screens", "Intro", "playButton.png")

gameOverBackdrop = loadImage("screens", "gameover", "gameover.png")
gameOverText = loadImage("screens", "gameover", "gameOver Text.png")

#
class Trees:
    def __init__(self,treeX,treeY):
        self.treeX = treeX
        self.treeY = treeY

class Crates:
    def __init__(self,crateX,crateY,broken,close):
        self.crateX = crateX
        self.crateY = crateY
        self.broken = broken
        self.close = close

class Zombies:
    def __init__(self,zombieX,zombieY,timer,angle,zombieDx,zombieDy,close,health):
        
        self.zombieX = zombieX
        self.zombieY = zombieY
        self.timer = timer
        self.angle = angle
        self.zombieDx = zombieDx
        self.zombieDy = zombieDy
        self.close = close
        self.health = health

class Bullet:
    def __init__ (self,bulletX,bulletY,angle,bulletDx,bulletDy):

        self.bulletX = bulletX
        self.bulletY = bulletY
        self.angle = angle
        self.bulletDx = bulletDx
        self.bulletDy = bulletDy

class Pellet(Bullet):
    def __init__ (self,bulletX,bulletY,angle,bulletDx,bulletDy):
        super().__init__ (bulletX,bulletY,angle,bulletDx,bulletDy)

#Powerup's happy family
class Powerup():
    def __init__(self,powerupX,powerupY):
        self.powerupX = powerupX
        self.powerupY = powerupY    
class Shellammo(Powerup):
    def __init__ (self,powerupX,powerupY):
        super().__init__(powerupX,powerupY)

class Rifleammo(Powerup):
    def __init__(self,rifleammoX,rifleammoY):
        super().__init__(rifleammoX,rifleammoY)

class Medkit(Powerup):
    def __init__(self,medkitX,medkitY):
        super().__init__(medkitX,medkitY)

        

def getRadiusAndAngleToEndpoint(cx, cy, targetX, targetY):
    angle = math.degrees(math.atan2(cy-targetY, targetX-cx)) % 360
    return (angle)
  

#Procedral Generation Code
def diamondGeneration(n):
    mapSize = 2**n + 1
    newMap = [[0] * mapSize for i in range(mapSize)]
    
    index = mapSize

    highrandomness = 0.2
    lowrandomness = -0.2

    newMap[0][0] = random.uniform(lowrandomness,highrandomness)
    newMap[0][mapSize - 1] = random.uniform(lowrandomness,highrandomness)
    newMap[mapSize - 1][0] = random.uniform(lowrandomness,highrandomness)
    newMap[mapSize - 1][mapSize - 1] = random.uniform(lowrandomness,highrandomness)

    while index > 1:
        index = index // 2
        startIndex = index
        
        # diamond step
        for row in range (startIndex,mapSize - 1,index * 2):
            for col in range(startIndex,mapSize - 1,index * 2):
                topL = newMap[row - index][col - index]
                topR = newMap[row - index][col + index]
                bottomL = newMap[row + index][col - index]
                bottomR = newMap[row + index][col + index]

                average = (topL + topR + bottomL + bottomR) / 4
                finalV = average + random.uniform(lowrandomness,highrandomness)

                newMap[row][col] = (finalV)
        # square step  
        for x in range(0, mapSize, index):
            for y in range((x + index) % (index * 2), mapSize, index * 2):
                total = 0
                count = 0
                if x - index >= 0:
                    total += newMap[x - index][y]
                    count += 1
                if x + index < mapSize:
                    total += newMap[x + index][y]
                    count += 1
                if y - index>= 0:
                    total += newMap[x][y - index]
                    count += 1
                if y + index < mapSize:
                    total += newMap[x][y + index]
                    count += 1

                if count > 0:
                    avg = total / count
                    newMap[x][y] = (avg + random.uniform(lowrandomness,highrandomness))

    return(newMap)


#Converting to noise map
def imageConverter(L):
    newImage = Image.new(mode='RGB', size=(len(L),len(L[0])))

    for x in range(newImage.width):
        for y in range(newImage.height):
            r,g,b = L[x][y]
            
            col = int(r)

            newImage.putpixel((x,y),(col,col,col))

    return newImage

def calcRGBValues(app):
    resultL = []
    for i in range(len(noiseMap)):
        line = []
        for j in range(len(noiseMap[0])):
            rgbvalue = int(noiseMap[i][j] * 255)

            rgbvalue %= 255
            if rgbvalue >= 60:
                rgbvalue = rgbvalue * 0.5

            line.append((rgbvalue,rgbvalue,rgbvalue))
        resultL.append(line)
    return resultL

#Gets the good spawn coordinates
def spawnCoordinates(i, j):
    return ((i * 200) - 12800,(j * 200) - 12800)

#Generates possible zombies
def zombieListGenerator(L,level):
    zombies = []
    for i in range(len(noiseMap)):
        for j in range(len(noiseMap[0])):
            val = str(noiseMap[i][j])
            if val[-1] == '1' and val[-2] == '2':
                zombies.append(Zombies(*spawnCoordinates(i, j),0,getRadiusAndAngleToEndpoint(i,j,500,500),0,0,False,100))
                
        
    return zombies

def crateListGenerator(L):
    crates = []
    for i in range(len(noiseMap)):
        for j in range(len(noiseMap[0])):
            val = str(noiseMap[i][j])
            if val[-1] == '1':
                crates.append(Crates(*spawnCoordinates(i, j),False,False))
                
        
    return crates

def treesListGenerator(L):
    trees = []
    for i in range(len(noiseMap)):
        for j in range(len(noiseMap[0])):
            val = str(noiseMap[i][j])
            # Bugfix: removed dead condition (val[-2] == '-1' could never be
            # True since val[-2] is a single character) — spawn rate unchanged
            if val[-1] == '2':
                
                trees.append(Trees(*spawnCoordinates(i, j)))
                
                
        
    return trees

def powerupGenerator():
    medkit = []
    rifleammo = []
    shellammo = []
    for i in range(len(noiseMap)):
        for j in range(len(noiseMap[0])):
            val = str(noiseMap[i][j])
            if val[-1] == '1':
                if int(val[-3]) < 4:
                    rifleammo.append(Rifleammo(*spawnCoordinates(i, j)))
                elif int(val[-3]) < 8:
                    shellammo.append(Shellammo(*spawnCoordinates(i, j)))
                elif int(val[-3]) == 9:
                    medkit.append(Medkit(*spawnCoordinates(i, j)))
                # Mimic crate: sometimes a "loot" tile spawns a zombie instead
                else: zombies.append(Zombies(*spawnCoordinates(i, j),0,getRadiusAndAngleToEndpoint(i,j,500,500),0,0,False,100))

    return rifleammo,shellammo,medkit
#Setting classes
noiseMap = diamondGeneration(7)
zombies = zombieListGenerator(noiseMap,0)
bullets = []
pellets = []
crates = crateListGenerator(noiseMap)
trees = treesListGenerator(noiseMap)
rifleammo,shellammo,medkit = powerupGenerator()
##################################
# Start Screen
##################################
def startScreen_onAppStart(app):
    pass
def startScreen_redrawAll(app):
    drawImage(gameStartBackdrop,-25,0)
    drawImage(gameStartText,100,100)
    drawImage(playButton,500,700,align = 'center')

def startScreen_onMousePress(app,mouseX,mouseY):
    if distance(500,mouseX,700,mouseY) < 100:
        setActiveScreen('playScreen')
##################################
# End Screen
##################################
def gameOver_onAppStart(app):
    pass
def gameOver_redrawAll(app):
    drawImage(gameOverBackdrop,-25,0)
    drawImage(gameOverText,200,200)

##################################
# Play Screen
##################################
def playScreen_onAppStart(app):

    #Board Dimensions
    app.size = 100
    app.width = 1000
    app.height = 1000

    #Noise Map Config
    app.pixels = calcRGBValues(app)
    app.noiseMap = CMUImage(imageConverter(app.pixels))
   
    
    #Player Config
    app.rx = -app.size
    app.ry = -app.size

    app.playerAngle = 0
    app.playerSpeed = 10
    app.playerSlot = 0
    app.playerSlots = [player,player1,player2]
    app.hp = 100
    app.playerPunch = False
    app.playerTimer = 0

    app.kills = 0
    
    #Scrolling Config
    app.horizDisplacement = 0
    app.vertDisplacement = 0

    #Ammo Config:
    app.shotgun = 15
    app.currentShotgun = 5

    app.rifle = 60
    app.currentRifle = 20

    

def playScreen_redrawAll(app):
    
    #Map Drawing
    for i in range(app.rx,app.rx + 1101,app.size):
        for j in range(app.ry,app.ry + 1101,app.size):
            row = i // app.size
            col = j // app.size
            r,g,b = app.pixels[row][col]
            drawImage(normalGrass, i + app.horizDisplacement, j + app.vertDisplacement)
    #Player Drawing
    if app.playerPunch and app.playerSlot == 0:
        drawImage(playerPunch,500,500,align = 'center',rotateAngle = app.playerAngle)
        
    else:
        drawImage(app.playerSlots[app.playerSlot],500,500,align = 'center',rotateAngle = app.playerAngle)

    #Zombie Drawing
    zombieIndex = 0
    while zombieIndex < len(zombies):
        zombie = zombies[zombieIndex]
        if distance(zombie.zombieX,500 - app.horizDisplacement,zombie.zombieY,500 - app.vertDisplacement) < 700:
            if zombie.close:
                drawImage(zombiePunch,zombie.zombieX + app.horizDisplacement,zombie.zombieY + app.vertDisplacement,rotateAngle = - zombie.angle - 90,align = 'center')
    
            else:
                drawImage(zombiePassive,zombie.zombieX + app.horizDisplacement,zombie.zombieY + app.vertDisplacement,rotateAngle = - zombie.angle - 90,align = 'center')
        zombieIndex += 1   

    #Crates Drawing
    for powerup in shellammo:
        if distance(powerup.powerupX,500 - app.horizDisplacement,powerup.powerupY,500 - app.vertDisplacement) < 700:
            drawImage(shotShell,powerup.powerupX + app.horizDisplacement,powerup.powerupY + app.vertDisplacement,align = 'center')
    for powerup in rifleammo:
        if distance(powerup.powerupX,500 - app.horizDisplacement,powerup.powerupY,500 - app.vertDisplacement) < 700:
            drawImage(rifleShell,powerup.powerupX + app.horizDisplacement,powerup.powerupY + app.vertDisplacement,align = 'center')
    for powerup in medkit:
        if distance(powerup.powerupX,500 - app.horizDisplacement,powerup.powerupY,500 - app.vertDisplacement) < 700:
            drawImage(healing,powerup.powerupX + app.horizDisplacement,powerup.powerupY + app.vertDisplacement,align = 'center')
        


    for crate in crates:
        if distance(crate.crateX,500 - app.horizDisplacement,crate.crateY,500 - app.vertDisplacement) < 700:
            if crate.broken:
                drawImage(brokenCrate,crate.crateX + app.horizDisplacement,crate.crateY + app.vertDisplacement,align = 'center')
            else:
                drawImage(unbrokenCrate,crate.crateX + app.horizDisplacement,crate.crateY + app.vertDisplacement,align = 'center')
            # if crate.close and crate.broken == False:
            #     drawImage(crateButton,crate.crateX + app.horizDisplacement,crate.crateY + app.vertDisplacement + 40,align = 'center')

    for tree in trees:
        if distance(tree.treeX,500 - app.horizDisplacement,tree.treeY,500 - app.vertDisplacement) < 700:
            drawImage(trunk,tree.treeX + app.horizDisplacement,tree.treeY + app.vertDisplacement,align = 'center')
            drawImage(leaves,tree.treeX + app.horizDisplacement,tree.treeY + app.vertDisplacement,align = 'center',opacity = 50)
    
    #ammo drawing
    if app.playerSlot == 1:
        drawLabel(f'{app.currentRifle} / {app.rifle}',900,900,size = 60)
        bulletCollisionFunction(bullets)

    if app.playerSlot == 2:
        drawLabel(f'{app.currentShotgun} / {app.shotgun}',900,900,size = 60)
        bulletCollisionFunction(pellets)

    #Health bar drawing:
    drawRect(25,925,400,50,fill = 'black')
    drawRect(35,935,380,30,fill = 'white')
    if app.hp <= 0:
        return
    drawRect(35,935,app.hp * 3.8,30,fill = 'red')

    #kills Drawing
    drawLabel(f'Kills: {app.kills}',900,50, size = 60)

def bulletCollisionFunction(L):
    index = 0
    while index < len(L):
            
        if distance(L[index].bulletX,500,L[index].bulletY,500) > 700:
            L.pop(index)

        else:
            drawImage(bullet,L[index].bulletX,L[index].bulletY,rotateAngle = -L[index].angle - 90,align = 'center')
            index += 1


def playScreen_onKeyPress(app,key):
    close, textX, textY, index = isClose(app)
    if key == 'l':
        for zombie in zombies:
            print(zombie.zombieX,zombie.zombieY)
        print(zombies)
    if key == 'e' and close:
        crates[index].broken = True
    
    # Bugfix: previously checked crates[index] even when index was -1 (no crate
    # nearby), which silently checked the *last* crate in the world
    if key == 'e' and close and crates[index].broken:
        shellIndex = 0
        while shellIndex < len(shellammo):
            powerup = shellammo[shellIndex]
            if distance(powerup.powerupX,500 - app.horizDisplacement,powerup.powerupY,500 - app.vertDisplacement) < 50:
                if app.shotgun != 0:
                    app.shotgun += 5
                else:
                    app.currentShotgun += 5

                shellammo.pop(shellIndex)
            else:
                shellIndex += 1
        rifleIndex = 0
        while rifleIndex < len(rifleammo):
            powerup = rifleammo[rifleIndex]
            if distance(powerup.powerupX,500 - app.horizDisplacement,powerup.powerupY,500 - app.vertDisplacement) < 50:
                if app.rifle != 0:
                    app.rifle += 10
                else:
                    app.currentRifle += 10

                rifleammo.pop(rifleIndex)
            else:
                rifleIndex += 1
        medkitIndex = 0
        while medkitIndex < len(medkit):
            powerup = medkit[medkitIndex]
            if distance(powerup.powerupX,500 - app.horizDisplacement,powerup.powerupY,500 - app.vertDisplacement) < 50:
                if app.hp >= 90:
                    app.hp = 100
                else:
                    app.hp += 10
                medkit.pop(medkitIndex)
            else:
                medkitIndex += 1
            
            
            
    if key == '1':
        # Bugfix: "bullets = []" only made a local variable and never cleared
        # the real list — clear() mutates the module-level lists in place
        bullets.clear()
        pellets.clear()
        if app.playerSlot == 1:
            app.playerSlot = 0
            return
        app.playerSlot = 1

    if key == '2':
        bullets.clear()
        pellets.clear()
        if app.playerSlot == 2:
            app.playerSlot = 0
            return
        app.playerSlot = 2
    
    

def playScreen_onKeyHold(app,keys):
    close, textX, textY, index = isClose(app)
    if close and crates[index]:
        crates[index].close = True

    if 'd' in keys:
            if isLegal(app,-10,0):
                app.horizDisplacement -= app.playerSpeed
        
                if app.horizDisplacement % app.size == 0:
                    app.rx += app.size

    if 'a'in keys:
            if isLegal(app,10,0):
                app.horizDisplacement += app.playerSpeed
        
                if app.horizDisplacement % app.size == 0:
                    app.rx -= app.size

    if 's' in keys:
            if isLegal(app,0,-10):
                app.vertDisplacement -= app.playerSpeed
                if app.vertDisplacement % app.size == 0:
                    app.ry += app.size

    if 'w' in keys:
            if isLegal(app,0,10):
                app.vertDisplacement += app.playerSpeed
                if app.vertDisplacement % app.size == 0:
                    app.ry -= app.size



    if 'tab' in keys:
        app.map = True
    else:
        app.map = False

def playScreen_onMousePress(app,mouseX,mouseY):
    
    app.playerTimer = 0
    app.playerPunch = True

    for zombie in zombies:
        if distance(zombie.zombieX,500 - app.horizDisplacement,zombie.zombieY,500 - app.vertDisplacement) < 120 and app.playerSlot == 0:
            zombie.health -= 15

    if app.playerSlot == 1:
        if app.rifle == -1 and app.currentRifle == 1:
            app.currentRifle = 0  # Bugfix: was "==" (a comparison, did nothing)

        elif app.currentRifle == 1 and app.rifle != 0:
            app.currentRifle = 20
            app.rifle = app.rifle - 20
            
            
        elif app.rifle > -1 and app.currentRifle != 0:
            app.currentRifle -= 1
        else:
            app.currentRifle = 0
            app.rifle = 0
        
        if app.currentRifle > 0 or app.rifle > 0:
            bullets.append(Bullet(500,500,getRadiusAndAngleToEndpoint(mouseX,mouseY,500,500),0,0))

    if app.playerSlot == 2:
        if app.shotgun == -1 and app.currentShotgun == 1:
            app.currentShotgun = 0  # Bugfix: was "==" (a comparison, did nothing)

        elif app.currentShotgun == 1 and app.shotgun != 0:
            app.currentShotgun = 5
            app.shotgun = app.shotgun - 5
            
            
        elif app.shotgun > -1 and app.currentShotgun != 0:
            app.currentShotgun -= 1
        else:
            app.currentShotgun = 0
            app.shotgun = 0
        
        if app.currentShotgun > 0 or app.shotgun > 0:
            for i in range(0,5):  
                pellets.append(Pellet(500,500,getRadiusAndAngleToEndpoint(mouseX - 40 + i * 20,mouseY - 40 + i * 25,500,500),0,0))
        
    

    

def playScreen_onMouseHold(app,mouseX,mouseY):
    app.playerAngle = 90 - getRadiusAndAngleToEndpoint(500,500,mouseX,mouseY)  

def playScreen_onMouseMove(app, mouseX,mouseY):
    app.playerAngle = 90 - getRadiusAndAngleToEndpoint(500,500,mouseX,mouseY)  

def playScreen_onMouseDrag(app,mouseX,mouseY):
    app.playerAngle = 90 - getRadiusAndAngleToEndpoint(500,500,mouseX,mouseY)  


def playScreen_onStep(app):
    playScreen_takeStep(app)

def playScreen_takeStep(app):
    if app.hp <= 0:
        setActiveScreen('gameOver')
    app.playerTimer += 1
    for zombie in zombies:
        zombie.timer += 1
    
        zombie.angle = getRadiusAndAngleToEndpoint(500 - app.horizDisplacement,500 - app.vertDisplacement,zombie.zombieX,zombie.zombieY)

        zombie.zombieDx = 4 * math.cos(math.radians(zombie.angle)) 
        zombie.zombieDy = 4 * math.sin(math.radians(zombie.angle))
    
        if distance(zombie.zombieX,500 - app.horizDisplacement,zombie.zombieY,500 - app.vertDisplacement) < 120:
            if zombie.timer > 10:
                zombie.close = True
                zombie.timer = 0
            else:
                if zombie.timer > 5:
                    zombie.close = False
        else:
            zombie.close = False    

        if app.playerTimer > 2:
        
            app.playerPunch = False
            app.playerTimer = 0
    
        if distance(zombie.zombieX,500 - app.horizDisplacement,zombie.zombieY,500 - app.vertDisplacement) < 100 and zombie.timer < 5:
            app.hp -= 1

        if isZombieLegal(app, zombie):
            zombie.zombieX -= zombie.zombieDx 
            zombie.zombieY += zombie.zombieDy
        else:
            zombie.zombieX += zombie.zombieDx 
            zombie.zombieY -= zombie.zombieDy

        if zombie.timer > 11:
            zombie.timer = 0  # Bugfix: was app.zombieTimer, which nothing ever read

        if app.playerTimer > 11:
            app.playerTimer = 0


    bulletIndex = 0
    while bulletIndex < len(bullets):
        currentBullet = bullets[bulletIndex]

        
        currentBullet.bulletDx = 30 * math.cos(math.radians(currentBullet.angle)) 
        currentBullet.bulletDy = 30 * math.sin(math.radians(currentBullet.angle))

        collision = False
        
        for zombie in zombies:
            
            if bulletZombCollision(zombie.zombieX + app.horizDisplacement,currentBullet.bulletX,zombie.zombieY + app.vertDisplacement,currentBullet.bulletY):
                
                collision = True
                zombie.health -= 20
                
                break
        if collision:
            bullets.pop(bulletIndex)
        else:
            currentBullet.bulletX -= currentBullet.bulletDx
            currentBullet.bulletY += currentBullet.bulletDy
            bulletIndex += 1

    pelletIndex = 0

    while pelletIndex < len(pellets):
        currentBullet = pellets[pelletIndex]

        currentBullet.bulletDx = 30 * math.cos(math.radians(currentBullet.angle)) 
        currentBullet.bulletDy = 30 * math.sin(math.radians(currentBullet.angle))

        collision = False
        for zombie in zombies:
            if bulletZombCollision(zombie.zombieX + app.horizDisplacement,currentBullet.bulletX,zombie.zombieY + app.vertDisplacement,currentBullet.bulletY):
                
                collision = True
                zombie.health -= 10
                break
        if collision:
            pellets.pop(pelletIndex)
        else:
            currentBullet.bulletX -= currentBullet.bulletDx
            currentBullet.bulletY += currentBullet.bulletDy
            pelletIndex += 1
    

    #Zombie Elimination
    zombieIndex = 0
    while zombieIndex < len(zombies):
        zombie = zombies[zombieIndex]
        if zombie.health <= 0:
            zombies.pop(zombieIndex)
            app.kills += 1
        else:
            zombieIndex += 1

    


    
def isLegal(app,horV,verV):
    newH = app.horizDisplacement + horV
    newV = app.vertDisplacement + verV
    
    for crate in crates:

        if distance(crate.crateX,500 - newH,crate.crateY,500 - newV) < 100 and not crate.broken:
            return False
        
    for tree in trees:

        if distance(tree.treeX,500 - newH, tree.treeY,500 - newV) < 85:
            return False
        
    for zombie in zombies:
        # Bugfix: was crate.crateY (leftover variable from the crate loop above)
        if distance(zombie.zombieX,500 - newH,zombie.zombieY,500 - newV) < 150:
            return False
    return True

def isZombieLegal(app, zombie):
    newX = zombie.zombieX - zombie.zombieDx
    newY = zombie.zombieY - zombie.zombieDy
    if distance(newX,500 - app.horizDisplacement,newY,500 - app.vertDisplacement) >= 800: return True
    for crate in crates:

        if distance(crate.crateX,newX,crate.crateY,newY) < 110 and not crate.broken:
            return False
        
    for tree in trees:

        if distance(tree.treeX,newX, tree.treeY,newY) < 85:
            return False
        
    # for other in zombies:
    #     if other.zombieX == zombie.zombieX and other.zombieY == zombie.zombieY: continue
    #     if distance(other.zombieX,newX,other.zombieY,newY) < 150:
    #         return False
    
    return distance(newX,500 - app.horizDisplacement,newY,500 - app.vertDisplacement) >= 80

def isClose(app):
    for crateIndex in range(len(crates)):
        currentCrate = crates[crateIndex]
        if distance(currentCrate.crateX,500 - app.horizDisplacement,currentCrate.crateY,500 - app.vertDisplacement) < 150:
            return (True,currentCrate.crateX,currentCrate.crateY,crateIndex)
    return (False,-1,-1,-1)

def distance(x1,x2,y1,y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def bulletZombCollision(zx,bx,zy,by):
    if distance(zx,bx,zy,by) < 80:
        return True
    return False

def main():
    runAppWithScreens(initialScreen='startScreen')
main() 


