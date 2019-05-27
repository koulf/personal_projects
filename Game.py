import time
import random
import os
import threading



#PENDING TASKS
 #Decide whether or not to add motors in speed attribute
 #Decide whether or not to add ships as stored objects, because of the cargo in the missions


#Class variables

galaxy = []
available = []
missions = []
alerts = []

users =[]
passwords = []

#Not stored variable
a = 0
solar_systems = 100

#-------------------------------------------------------------------------------------
#Subclasses of game

class planet:
    def __init__(self, size, planetType, s, p):
        self.name = "-"
        self.size = size
        self.planetType = planetType
        self.coordinates = [s, p]
        self.user = "-"
        #Resources
        self.metal = [300,0]
        self.no_metal = [300,0]
        self.gas = [200,0]
        self.energy = 0
        #Limits
        self.metal_limit = 1000
        self.no_metal_limit = 1000
        self.gas_limit = 1000
        #Buildings
        self.metal_mine = building(0, 100, 100, 0)
        self.no_metal_mine = building(0, 100, 100, 0)
        self.gas_refinery = building(0, 100, 100, 0)
        self.power_plant = building(0, 100, 100, 0)
        self.metal_repository = building(0, 500, 500, 0)
        self.no_metal_repository = building(0, 500, 500, 0)
        self.gas_tank = building(0, 500, 500, 0)
        self.shipyard = building(0, 1000, 1000, 0)
        self.fleet = {"Battleship":0, "Hunter":0, "Colonizer":0, "Spy":0, "Cargoship":0}
    def __repr__(self):
    	return "(" + str(self.planetType) + ", " + str(self.user) + ", " + str(self.name) + ")"
    def reclaim(self, user):
        t = int(time.time())
        self.user = user
        self.metal[1] = t
        self.no_metal[1] = t
        self.gas[1] = t
    def add_fleet(self, ship, amount):
        self.fleet[ship] += amount
    def rename(self, name):
        self.name = name

class building:
    def __init__(self, level, metalCost, nonmetalCost, powerCost):
        self.level = level
        self.metal_cost = metalCost
        self.no_metal_cost = nonmetalCost
        self.power_cost = powerCost
    def upgrade(self):
        self.level += 1
        self.metal_cost *= 2
        self.no_metal_cost *= 2

class research:
    def __init__(self, level, metalCost, nonmetalCost, gasCost):
        self.level = level
        self.metal_cost = metalCost
        self.no_metal_cost = nonmetalCost
        self.gas_cost = gasCost
    def upgrade(self):
        self.level += 1
        self.metal_cost *= 2
        self.no_metal_cost *= 2
        self.gas_cost *= 2

class ship:
    def __init__(self, name, attack, structure, speed, cargo, metal_cost, no_metal_cost, gas_cost):
        #Features
        self.name = name
        self.attack = attack
        self.structure = structure
        self.speed = speed
        self.cargo = cargo
        #Costs
        self.metal_cost = metal_cost
        self.no_metal_cost = no_metal_cost
        self.gas_cost  = gas_cost

class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.points = 0
        self.planets = []
        self.weapon = research(0, 100, 100, 100)
        self.structure = research(0, 200, 200, 200)
        self.motor = research(0, 500, 500, 500)
        self.colonize = research(0, 20_000, 20_000, 10_000)
        self.spying = research(0, 5_000, 5_000, 5_000)
    def reclaim(self, n):
    	self.planets.append(n)
    def __repr__(self):
        return self.username

class mission(threading.Thread):
    def __init__(self, duration, comeback, c1, c2, planet, fleet):
        threading.Thread.__init__(self)
        self.duration = duration
        self.comeback = comeback
        self.c1 = c1
        self.c2 = c2
        self.planet = planet
        self.fleet = fleet
    
    def run(self):
        if self.comeback:
            alerts.append("Coming soon")
        else:
            if galaxy[self.c1][self.c2].user == "-":
                while self.duration > 0:
                    self.duration -= 1
                    time.sleep(1)
                if galaxy[self.c1][self.c2].user == "-":
                    available.remove([self.c1, self.c2])
                    galaxy[self.c1][self.c2].reclaim(self.planet.user)
                    self.planet.user.reclaim(galaxy[self.c1][self.c2])
                    self.fleet[2] -= 1
                    for i in range(len(self.fleet)):
                        galaxy[self.c1][self.c2].fleet[list(self.planet.fleet.keys())[i]] += self.fleet[i]
                    alerts.append("Planet taken")
                else:
                    alerts.append("Planet was taken")
            else:
                alerts.append("Coming soon")
        missions.remove(self)

#-------------------------------------------------------------------------------------
#Game functions

def generate_universe(systems_spots):
    for s in range(systems_spots):
        system = []
        for p in range(15):
            if random.randrange(0, 2) == 1:
                pl = planet(random.randrange(100, 150), random.randrange(4), s, p)
                system.append(pl)
                available.append([s, p])
            else:
                system.append("")
        galaxy.append(system)

def save():
    #PENDING FUNCTION
    print("pending")

def regenerate_universe(g, u , p):
    #PENDING FUNCTION
    l = list(map(int, input().rstrip().split()))

def rand_assign(user):
    pc = random.choice(available)
    available.remove(pc)
    galaxy[pc[0]][pc[1]].reclaim(user)
    user.reclaim(galaxy[pc[0]][pc[1]])

def build(planet, building):
    f, t, balance, balance2, balance3 = resources(planet)
    if balance >= building.metal_cost:
        if balance2 >= building.no_metal_cost:
            planet.metal[0] = balance - building.metal_cost
            planet.no_metal[0] = balance2 - building.no_metal_cost
            planet.metal[1] = planet.no_metal[1] = t
            if building == planet.metal_repository:
            	planet.metal_limit *= 2
            if building == planet.no_metal_repository:
            	planet.no_metal_limit *= 2
            if building == planet.gas_tank:
            	planet.gas_limit *= 2
            if building == planet.gas_refinery or building == planet.gas_tank:
                planet.gas[0] = balance3
                planet.gas[1] = t
            if building.level == 0:
                if building == planet.power_plant:
                    planet.energy = 300
                elif building == planet.metal_mine or building == planet.no_metal_mine or building == planet.gas_refinery:
                    building.power_cost = 100
            else:
                if building == planet.power_plant:
                    planet.energy *= 2
                elif building == planet.metal_mine or building == planet.no_metal_mine or building == planet.gas_refinery:
                    building.power_cost *= 2
            building.upgrade()
            print("Upgrade succesful")
        else:
            print("Insufficient no-metal")
    else:
        print("Insufficient metal")

def build_fleet(planet, user, ship, amount):
    if ship.name == "Battleship" and (planet.shipyard.level < 1 or user.weapon.level < 2 or user.structure.level < 2 or user.motor.level < 2):
        print("Unfulfilled requirement")
    elif ship.name == "Hunter" and (planet.shipyard.level < 5 or user.weapon.level < 5 or user.structure.level < 5 or user.motor.level < 5):
        print("Unfulfilled requirement")
    elif ship.name == "Colonizer" and (planet.shipyard.level < 4 or user.colonize.level < 1 or user.structure.level < 4 or user.motor.level < 4):
        print("Unfulfilled requirement")
    elif ship.name == "Spy" and (planet.shipyard.level < 3 or user.spying.level < 1 or user.structure.level < 2 or user.motor.level < 3):
        print("Unfulfilled requirement")
    elif ship.name == "Cargoship" and (planet.shipyard.level < 3 or user.structure.level < 4 or user.motor.level < 3):
        print("Unfulfilled requirement")
    else:
        f, t, balance, balance2, balance3 = resources(planet)
        if balance >= (ship.metal_cost * amount):
            if balance2 >= (ship.no_metal_cost * amount):
                if balance3 >= (ship.gas_cost * amount):
                    planet.metal[0] = balance - ship.metal_cost
                    planet.no_metal[0] = balance2 - ship.no_metal_cost
                    planet.gas[0] = balance3 - ship.gas_cost
                    planet.metal[1] = planet.no_metal[1] = planet.gas[1] = t
                    planet.add_fleet(ship.name, amount)
                    print("Fleet was built")
                else:
                    print("Insufficient gas")
            else:
                print("Insufficient no-metal")
        else:
            print("Insufficient metal")

def show(planet):
    f, t, balance, balance2, balance3 = resources(planet)
    print("Metal = " + str(balance) + "/" + str(planet.metal_limit) +
          " | No-metal = " + str(balance2) + "/" + str(planet.no_metal_limit) +
          " | Gas = " + str(balance3) + "/" + str(planet.gas_limit) +
          " | Energy = " + str(planet.energy - planet.metal_mine.power_cost - planet.no_metal_mine.power_cost - planet.gas_refinery.power_cost) +
          "/" + str(planet.energy))

def do_research(planet, research):
    f, t, balance, balance2, balance3 = resources(planet)
    if balance >= research.metal_cost:
        if balance2 >= research.no_metal_cost:
            if balance3 >= research.gas_cost:
                planet.metal[0] = balance - research.metal_cost
                planet.no_metal[0] = balance2 - research.no_metal_cost
                planet.gas[0] = balance3 - research.gas_cost
                planet.metal[1] = planet.no_metal[1] = planet.gas[1] = t
                research.upgrade()
                print("Research complete")
            else:
                print("Insufficient gas")
        else:
            print("Insufficient no-metal")
    else:
        print("Insufficient metal")

def exec_mission(c1, c2, fleet, missionType, gasCost, duration, planet):
    _, t, _, _, balance3 = resources(planet)
    if balance3 >= gasCost:
        if missionType == "Attack":
            print("Coming soon")
        elif missionType == "Transport":
            print("Coming soon")
        elif missionType == "Colonize":
            if galaxy[c1][c2].user == "-":
                if fleet[2] >= 1:
                    planet.gas[0] = balance3 - gasCost
                    planet.gas[1] = t
                    for i in range(len(fleet)):
                        planet.fleet[list(planet.fleet.keys())[i]] -= fleet[i]
                    missions.append(mission(duration, False, c1, c2, planet, fleet))
                    missions[len(missions)-1].start()
                    print("Mission started")
                else:
                    print("U need to send a colonizer")
            else:
                print("Planet occupated")
        elif missionType == "Spy":
            print("Coming soon")
    else:
        print("Insufficient gas")

def resources(planet):
    f = 10
    t = int(time.time())
    if planet.power_plant.level <= max(planet.metal_mine.level, planet.no_metal_mine.level, planet.gas_refinery.level):
        try:
            power_balance = planet.energy / (planet.metal_mine.power_cost + planet.no_metal_mine.power_cost + planet.gas_refinery.power_cost)
        except:
            power_balance = 0
    else:
        power_balance = 1
    balance = int((t - planet.metal[1])*planet.metal_mine.level*f*power_balance) + planet.metal[0]
    if balance >= planet.metal_limit:
        balance = planet.metal_limit
    balance2 = int((t - planet.no_metal[1])*planet.no_metal_mine.level*f*power_balance) + planet.no_metal[0]
    if balance2 >= planet.no_metal_limit:
        balance2 = planet.no_metal_limit
    balance3 = int((t - planet.gas[1])*planet.gas_refinery.level*f*power_balance) + planet.gas[0]
    if balance3 >= planet.gas_limit:
        balance3 = planet.gas_limit
    return f, t, balance, balance2, balance3

def start(user):
    a = 0
    p = user.planets[0]
    clear()
    while True:
        print("\nPlanet " + "(" + str(p.coordinates[0]+1) + ", " + str(p.coordinates[1]+1) + "): " + p.name)
        print("Missions:  " + str(len(missions)) + "\n")
        print("What do u wanna do?\n" +
              "[1] Build\n" +
              "[2] Research\n" +
              "[3] Explore\n" +
              "[4] Ship\n" +
              "[5] Inform\n" +
              "[6] Switch\n" +
              "[7] Rename\n" +
              "[8] Logout\n")
        a = enter()
        clear()
        if a == 1:
            print("What do u wanna build?\n" +
                  "[1] Buildings\n" +
                  "[2] Ships\n")
            a = enter()
            clear()
            if a == 1:
                print("What do u wanna build?\n" +
                      "[1] Metal mine\n" +
                      "[2] No metal mine\n" +
                      "[3] Gas Refinery\n" +
                      "[4] Power plant\n" +
                      "[5] Metal repository\n" +
                      "[6] No metal repository\n" +
                      "[7] Gas tank\n" +
                      "[8] Shipyard\n")
                a = enter()
                clear()
                if a == 1:
                    b = p.metal_mine
                elif a == 2:
                    b = p.no_metal_mine
                elif a == 3:
                    b = p.gas_refinery
                elif a == 4:
                    b = p.power_plant
                elif a == 5:
                    b = p.metal_repository
                elif a == 6:
                    b = p.no_metal_repository
                elif a == 7:
                    b = p.gas_tank
                elif a == 8:
                    b = p.shipyard
                else:
                    print("Invalid input")
                    continue
                print("Are u sure? [1] Sí  |  [0] No\n")
                print("Metal cost = " + str(b.metal_cost) + " | No-metal cost = " + str(b.no_metal_cost) + "\n")
                a = enter()
                clear()
                if a == 1:
                    build(p, b)
                elif a == 0:
                    print("Any change made")
                else:
                    print("Invalid input")
            elif a == 2:
                print("What do u wanna build?\n" +
                      "[1] Battleship\n" +
                      "[2] Hunter\n" +
                      "[3] Colonizer\n" +
                      "[4] Spy\n" +
                      "[5] Cargoship\n")
                a = enter()
                clear()
                if a == 1:
                    ship = battleship
                    req = "Requirements: Shipyard level 1, Weapon level 2, Structure level 2, Motor level 2"
                elif a == 2:
                    ship = hunter
                    req = "Requirements: Shipyard level 5, Weapon level 5, Structure level 5, Motor level 5"
                elif a == 3:
                    ship = colonizer
                    req = "Requirements: Shipyard level 4, Colonize level 1, Structure level 4, Motor level 4"
                elif a == 4:
                    ship = spy
                    req = "Requirements: Shipyard level 3, Spying level 1, Structure level 2, Motor level 3"
                elif a == 4:
                    ship = cargoship
                    req = "Requirements: Shipyard level 3, Structure level 4, Motor level 3"
                else:
                    print("Invalid input")
                    continue
                print("How many?")
                am = enter()
                clear()
                if am == -1:
                    print("Invalid input")
                    continue
                print("Are u sure? [1] Sí  |  [0] No\n")
                print(req)
                print("Metal cost = " + str(ship.metal_cost) + " | No-metal cost = " + str(ship.no_metal_cost) + " | Gas cost = " + str(ship.gas_cost) + "\n")
                a = enter()
                clear()
                if a == 1:
                    build_fleet(p, user, ship, am)
                elif a == 0:
                    print("Any change made")
                else:
                    print("Invalid input")
            else:
                print("Invalid input")
        elif a == 2:
            print("What do u wanna research?\n" + 
                  "[1] Weapon\n"+
                  "[2] Structure\n" +
                  "[3] Motor\n" +
                  "[4] Colonize\n" +
                  "[5] Spying\n")
            a = enter()
            clear()
            if a == 1:
                r = user.weapon
            elif a == 2:
                r = user.structure
            elif a == 3:
                r = user.motor
            elif a == 4:
                r = user.colonize
            elif a == 5:
                r = user.spying
            else:
                print("Invalid input")
                continue
            print("Are u sure? [1] Sí  |  [0] No\n")
            print("Metal cost = " + str(r.metal_cost) + " | No-metal cost = " + str(r.no_metal_cost) + " | Gas cost = " + str(r.gas_cost) + "\n")
            a = enter()
            clear()
            if a == 1:
                do_research(p, r)
            elif a == 0:
                print("Any change made")
            else:
                print("Invalid input")
        elif a == 3:
            _, t, _, _, balance3 = resources(p)
            if balance3 >= 500:
                p.gas[0] = balance3 - 500
                p.gas[1] = t
                b = p.coordinates[0]
                while True:
                    print("\n{" + str(b+1) + "}")
                    for i in range(len(galaxy[b])):
                        print(str(i+1) + "..." + str(galaxy[b][i]))
                    print("What do u wanna do?\n" +
                          "[1] Previous\n" +
                          "[2] Next\n" +
                          "[3] Go back\n")
                    a = enter()
                    clear()
                    if a == 1:
                        b -= 1
                        if b < 0:
                            b = len(galaxy) - 1
                    elif a == 2:
                        b += 1
                        if b > len(galaxy):
                            b = 0
                    elif a == 3:
                        break
                    else:
                        print("Invalid input")
                        continue
            else:
                print("Insufficient gas")
        elif a == 4:
            if sum(p.fleet.values()) == 0:
                print("U dont have a fleet in this planet")
                continue
            print("What system u wanna go to?\n")
            s = enter()
            clear()
            if s < 1 or s > len(galaxy):
                print("Invalid input")
                continue
            print("What planet u wanna go to?\n")
            pl = enter()
            clear()
            if pl < 1 or pl > 15:
                print("Invalid input")
                continue
            elif galaxy[s-1][pl-1] == "":
                print("Invalid destiny")
                continue
            i = 0
            am = []
            speeds = []
            while i < len(p.fleet):
                amount = p.fleet[list(p.fleet.keys())[i]]
                if amount > 0:
                    print("\nHow many " + list(p.fleet.keys())[i] + " u wanna send?\n")
                    a = enter()
                    clear()
                    if a < 0:
                        print("Invalid input")
                        continue
                    elif a > amount:
                        print("U dont have enough ships")
                        continue
                    else:
                        am.append(a)
                        speeds.append(ships[i].speed)
                else:
                    am.append(0)
                i += 1
            print("what do u wanna do?\n" +
                  "[1] Attack\n" +
                  "[2] Transport\n" +
                  "[3] Colonize\n" +
                  "[4] Spy\n")
            m = enter()
            clear()
            if m < 1 or m > 4:
                print("Invalid input")
                continue
            if m == 1:
                m = "Attack"
            elif m == 2:
                m = "Transport"
            elif m == 3:
                m = "Colonize"
            else:
                m = "Spy"
            minspeed = min(speeds)
            if p.coordinates[0] == (s-1):
                distance = abs(p.coordinates[1] - (pl - 1))
            else:
                distance = (angular(p.coordinates[0], s - 1) - 1)*31 + 1 + (15 - pl) + (14 - p.coordinates[1])
            print("Are u sure? [1] Sí  |  [0] No\n")
            print("Destiny: (" + str(s) + ", " + str(pl) + ")")
            st = "Fleet: "
            for i in range(len(p.fleet)):
                st += str(am[i]) + " " +  list(p.fleet.keys())[i] + ", "
            print(st[:len(st)-2])
            print("Distance: " + str(distance))
            print("Gas cost: " + str(distance * 100))
            print("Duration: " + str(int((distance / minspeed) * 60)))
            print("Mission: " + m + "\n")
            a = enter()
            clear()
            if a == 1:
                exec_mission(s-1, pl-1, am, m, distance*100, int((distance / minspeed) * 60), p)
            elif a == 0:
                print("Any change made")
            else:
                print("Invalid input")
        elif a == 5:
            print("What do u wanna know?\n" +
                  "[1] Resources\n" +
                  "[2] Buildings\n" +
                  "[3] Researches\n" +
                  "[4] Fleet\n"
                  "[5] Alerts\n")
            a = enter()
            clear()
            if a == 1:
                show(p)
            elif a == 2:
                print("Metal mine           " + str(p.metal_mine.level) + "\n" +
                      "No-metal mine        " + str(p.no_metal_mine.level) + "\n" +
                      "Gas refinery         " + str(p.gas_refinery.level) + "\n" +
                      "Power plant          " + str(p.power_plant.level) + "\n" +
                      "Metal repository     " + str(p.metal_repository.level) + "\n" +
                      "No-metal repository  " + str(p.no_metal_repository.level) + "\n" +
                      "Gas tank             " + str(p.gas_tank.level) + "\n" +
                      "Shipyard             " + str(p.shipyard.level) + "\n")
            elif a == 3:
                print("Weapon     " + str(user.weapon.level) + "\n" +
                      "Structure  " + str(user.structure.level) + "\n" +
                      "Motor      " + str(user.motor.level) + "\n" +
                      "Colonize   " + str(user.colonize.level) + "\n" +
                      "Spying     " + str(user.spying.level) + "\n")
            elif a == 4:
                print(p.fleet)
            elif a == 5:
                print("...Alerts...\n")
                for i in alerts:
                    print(i)
                del alerts[:len(alerts)]
            else:
                print("Invalid input")
        elif a == 6:
            print("What planet u wanna go to?\n")
            for i in range(len(user.planets)):
                print("[" + str(i+1) + "] " + user.planets[i].name)
            print()
            a = enter()
            clear()
            if a == -1 or a > len(user.planets):
                print("Invalid input")
            else:
                p = user.planets[a-1]
        elif a == 7:
            print("What's the new name?\n")
            a = input()
            p.rename(a)
            clear()
        elif a == 8:
            break
        else:
            print("Invalid input")

#Auxiliar functions
def clear():
    global cl
    if cl:
        os.system('cls')

def enter():
    try:
        a = int(input())
    except:
        a = -1
    return a

def angular(a, b):
    global solar_systems
    if abs(a - b) > int((solar_systems + 1) / 2):
        return solar_systems + 1 - abs(a - b)
    else:
        return abs(a - b)

#-------------------------------------------------------------------------------------
#Testing of game

generate_universe(solar_systems)
u = user("reluro", "kk12345")
rand_assign(u)
#Objects of class
#Ships
battleship = ship("Battleship", 100, 1_000, .5, 100, 500, 500, 300)
hunter = ship("Hunter", 1_000, 5_000, 1, 1_000, 2_000, 2_000, 1_500)
colonizer = ship("Colonizer", 0, 2_500, 1/3, 3_000, 20_000, 20_000, 15_000)
spy = ship("Spy", 0, 500, 12, 0, 3_000, 0, 1_000)
cargoship = ship("Cargoship", 100, 5_000, .2, 15_000, 2_000, 2_000, 2_000)
ships = [battleship, hunter, colonizer, cargoship, spy]
cl = False
if input() == "0":
    cl = True
start(u)

#-------------------------------------------------------------------------------------
#Game beginning

##try:
##    uf = open("users.game", "r+")
##    gf = open("game.game", "r+")
##    pf = open("password.game", "r+")
##except:
##    print("Data not found...\n" +
##          "Your username will be created in a new game file.")
##    uf = open("users.game", "w+")
##    gf = open("game.game", "w+")
##    pf = open("password.game", "w+")
##    a = 3
##while True:
##    if a == 0:
##        print("What do u wanna do?\n" +
##              "[0] Login\n" +
##              "[1] Register\n" +
##              "[2] Exit\n")
##        a = enter()
##    if a == 0 or  a == 1 or a == 3:
##        print("Enter username:")
##        u = input()
##        if u == "" or u == "-":
##            print("Invalid user. Try again")
##            a = 0
##            continue
##        print("Enter password:")
##        p = input()
##		clear()
##        if a != 3:
##            ufd = uf.read()
##            gfd = gf.read()
##            pfd = pf.read()
##            if a == 0:
##                if ufd.find(u) == -1 or pfd.find(p) == -1:
##                    print("Username or password error")
##                    continue
##            else:
##                if ufd.find(u) != -1:
##                    print("Username already exists")
##                    continue
##            regenerate_universe(gfd, ufd, pfd)
##        else:
##            generate_universe(100)
##            start()
##    elif a == 2:
##        print("Thanks for playing")
##        break
##    else:
##        print("Unknown answer\n")
