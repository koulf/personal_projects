import time
import _thread
import random

#Subclasses of game
class planet:
    def __init__(self, size, planetType, s, p):
        self.size = size
        self.planetType = planetType
        self.coordenates = [s, p]
        self.user = 0
    def __repr__(self):
    	return "(" + str(self.coordenates) + ", " + str(self.size) + ", " + str(self.planetType) + ")"
    def reclaim(self, user):
    	self.user = user

class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.points = 0
        self.planets = []
    def reclaim(self, n):
    	self.planets.append(n)

class ship:
    def __init__(self, shipname, shield, speed, metalCost, nonmetalCost, gasCost):
        self.shipname = shipname
        self.power = power
        self.speed = speed
        self.metalCost = metalCost
        self.nonmetalCost = nonmetalCost
        self.gasCost = gasCost

class mission:
    def __init__(self, missionType):
        self.missionType = missionType

class building:
    def __init__(self, buildingType, level, metalCost, nonmetalCost, gasCost):
        self.buildingType = buildingType
        self.level = level
        self.metalCost = metalCost
        self.nonmetalCost = nonmetalCost
        self.gasCost = gasCost

class research:
    def __init__(self, name, level, metalCost, nonmetalCost, gasCost):
        self.name = name
        self.level = level
        self.metalCost = metalCost
        self.nonmetalCost = nonmetalCost
        self.gasCost = gasCost

def counts():
    while life:
        time.sleep(1)
        counter[0] += 1

def generate_universe(ss):
    try:
        _thread.start_new_thread(counts,())
    except:
         "Error with thread"
    for s in range(ss):
        system = []
        for p in range(15):
            if random.randrange(0, 2) == 1:
                pl = planet(random.randrange(100, 120), random.randrange(4), s, p)
                system.append(pl)
                avaliable.append([s, p])
            else:
                system.append(0)
                galaxy.append(system)

def assign(user):
    pc = random.choice(avaliable)
    avaliable.remove(pc)
    galaxy[pc[0]][pc[1]].reclaim(user)
    user.reclaim(galaxy[pc[0]][pc[1]])

#Class variables
galaxy = []
available = []
counter = [0]

users =[]
passwords = []

a = 0
life = False

#Game staring
try:
    uf = open("users.game", "r+")
    pf = open("passwords.game", "r+")
    gf = open("game.game", "r+")
except:
    print("Data not found...\n" +
          "Your username will be created in a new game file.")
    uf = open("users.game", "w+")
    pf = open("passwords.game", "w+")
    gf = open("game.game", "w+")
    a = 1
while True:
    if a == 0:
        print("What do u wanna do?\n" +
              "[0] Login\n" +
              "[1] Register")
        try:
            a = int(input())
        except:
            a = 3
    if a == 0 or a == 1:
        print("Enter username:")
        u = input()
        print("Enter password:")
        p = input()
        if a == 0:
            
        else:
            
    else:
        print("Wrong answer. Try again.")

print("Thanks for playing")
