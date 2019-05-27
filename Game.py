import timeimport randomimport os#PENDING TASK. TEST SHIPS AND BUILDING#Class variablesgalaxy = []available = []users =[]passwords = []#Not stored variablea = 0f = 10#Subclasses of gameclass planet:    def __init__(self, size, planetType, s, p):        self.name = "planet"        self.size = size        self.planetType = planetType        self.coordinates = [s, p]        self.user = 0        #Resources        self.metal = [300,0]        self.no_metal = [300,0]        self.gas = [200,0]        self.energy = 0        #Limits        self.metal_limit = 1000        self.no_metal_limit = 1000        self.gas_limit = 1000        #Buildings        self.metal_mine = building(0, 100, 100, 0)        self.no_metal_mine = building(0, 100, 100, 0)        self.gas_refinery = building(0, 100, 100, 0)        self.power_plant = building(0, 100, 100, 0)        self.metal_repository = building(0, 500, 500, 0)        self.no_metal_repository = building(0, 500, 500, 0)        self.gas_tank = building(0, 500, 500, 0)        self.shipyard = building(0, 1000, 1000, 0)        self.fleet = {"Battleship":0, "Hunter":0, "Colonizer":0, "Spy":0}    def __repr__(self):    	return "(" + str(self.coordinates) + ", " + str(self.size) + ", " + str(self.planetType) + ")"    def reclaim(self, user):        t = int(time.time())        self.user = user        self.metal[1] = t        self.no_metal[1] = t        self.gas[1] = t    def add_fleet(self, ship, amount):        self.fleet[ship] += amount    def rename(self, name):        self.name = nameclass building:    def __init__(self, level, metalCost, nonmetalCost, powerCost):        self.level = level        self.metal_cost = metalCost        self.no_metal_cost = nonmetalCost        self.power_cost = powerCost    def upgrade(self):        self.level += 1        self.metal_cost *= 2        self.no_metal_cost *= 2class research:    def __init__(self, level, metalCost, nonmetalCost, gasCost):        self.level = level        self.metal_cost = metalCost        self.no_metal_cost = nonmetalCost        self.gas_cost = gasCost    def upgrade(self):        self.level += 1        self.metal_cost *= 2        self.no_metal_cost *= 2        self.gas_cost *= 2class ship:    def __init__(self, name, attack, structure, speed, colonyModule, metal_cost, no_metal_cost, gas_cost):        #Features        self.name = name        self.attack = attack        self.structure = structure        self.speed = speed        self.colony_module = colonyModule        #Costs        self.metal_cost = metal_cost        self.no_metal_cost = no_metal_cost        self.gas_cost  = gas_costclass mission:    def __init__(self, missionType):        self.missionType = missionTypeclass user:    def __init__(self, username, password):        self.username = username        self.password = password        self.points = 0        self.planets = []        self.weapon = research(0, 100, 100, 100)        self.motor = research(0, 500, 500, 500)        self.structure = research(0, 200, 200, 200)        self.colonize = research(0, 20_000, 20_000, 10_000)        self.spying = research(0, 5_000, 5_000, 5_000)    def reclaim(self, n):    	self.planets.append(n)def generate_universe(systems_spots):    for s in range(systems_spots):        system = []        for p in range(15):            if random.randrange(0, 2) == 1:                pl = planet(random.randrange(100, 150), random.randrange(4), s, p)                system.append(pl)                available.append([s, p])            else:                system.append(0)        galaxy.append(system)def save():    print("pending")def regenerate_universe(g, u , p):    l = list(map(int, input().rstrip().split()))def rand_assign(user):    pc = random.choice(available)    available.remove(pc)    galaxy[pc[0]][pc[1]].reclaim(user)    user.reclaim(galaxy[pc[0]][pc[1]])def build(planet, building):    f, t, power_balance = resources(planet)    balance = int((t - planet.metal[1])*planet.metal_mine.level*f*power_balance) + planet.metal[0]    if balance >= planet.metal_limit:        balance = planet.metal_limit    if building.metal_cost <= balance:        balance2 = int((t - planet.no_metal[1])*planet.no_metal_mine.level*f*power_balance) + planet.no_metal[0]        if balance2 >= planet.no_metal_limit:            balance2 = planet.no_metal_limit        if building.no_metal_cost <= balance2:            planet.metal[0] = balance - building.metal_cost            planet.no_metal[0] = balance2 - building.no_metal_cost            planet.metal[1] = planet.no_metal[1] = t            if building == planet.metal_repository:            	planet.metal_limit *= 2            if building == planet.no_metal_repository:            	planet.no_metal_limit *= 2            if building == planet.gas_tank:            	planet.gas_limit *= 2            if building.level == 0:                if building == planet.power_plant:                    planet.energy = 300                elif building == planet.metal_mine or building == planet.no_metal_mine or building == planet.gas_refinery:                    building.power_cost = 100            else:                if building == planet.power_plant:                    planet.energy *= 2                elif building == planet.metal_mine or building == planet.no_metal_mine or building == planet.gas_refinery:                    building.power_cost *= 2            building.upgrade()            print("Upgrede succesful")        else:            print("Insufficient no-metal")    else:        print("Insufficient metal")def build_fleet(planet, user, ship, amount):    f, t, power_balance = resources(planet)    balance = int((t - planet.metal[1])*planet.metal_mine.level*f*power_balance) + planet.metal[0]    if balance >= planet.metal_limit:        balance = planet.metal_limit    balance2 = int((t - planet.no_metal[1])*planet.no_metal_mine.level*f*power_balance) + planet.no_metal[0]    if balance2 >= planet.no_metal_limit:        balance2 = planet.no_metal_limit    balance3 = int((t - planet.gas[1])*planet.gas_tank.level*f*power_balance) + planet.gas[0]    if balance3 >= planet.gas_limit:        balance3 = planet.gas_limit    if ship.name == "Battleship" and (planet.shipyard.level < 1 or user.weapon.level < 2 or user.structure.level < 2 or user.motor.level < 2):        print("Unfulfilled requirement")    elif ship.name == "Hunter" and (planet.shipyard.level < 5 or user.weapon.level < 5 or user.structure.level < 5 or user.motor.level < 5):        print("Unfulfilled requirement")    elif ship.name == "Colonizer" and (planet.shipyard.level < 4 or user.colonize.level < 1 or user.structure.level < 4 or user.motor.level < 4):        print("Unfulfilled requirement")    elif ship.name == "Spy" and (planet.shipyard.level < 3 or user.spying.level < 1 or user.structure.level < 2 or user.motor.level < 2):        print("Unfulfilled requirement")    else:        if balance >= (ship.metal_cost * amount):            if balance2 >= (ship.no_metal_cost * amount):                if balance3 >= (ship.gas_cost * amount):                    planet.metal[0] = balance - ship.metal_cost                    planet.no_metal[0] = balance2 - ship.no_metal_cost                    planet.gas[0] = balance3 - ship.gas_cost                    planet.metal[1] = planet.no_metal[1] = planet.gas[1] = t                    planet.add_fleet(ship.name, amount)                    planet("Fleet was built")                else:                    print("Insufficient gas")            else:                print("Insufficient no-metal")        else:            print("Insufficient metal")def show(planet):    f, t, power_balance = resources(planet)    balance = int((t - planet.metal[1])*planet.metal_mine.level*f*power_balance) + planet.metal[0]    if balance >= planet.metal_limit:        balance =  planet.metal_limit    balance2 = int((t - planet.no_metal[1])*planet.no_metal_mine.level*f*power_balance) + planet.no_metal[0]    if balance2 >= planet.no_metal_limit:        balance2 =  planet.no_metal_limit    balance3 = int((t - planet.gas[1])*planet.gas_refinery.level*f*power_balance) + planet.gas[0]    if balance3 >= planet.gas_limit:        balance3 =  planet.gas_limit    print("Metal = " + str(balance) + "/" + str(planet.metal_limit) + " | No-metal = " + str(balance2) + "/" + str(planet.no_metal_limit) + " | Gas = " + str(balance3) + "/" + str(planet.gas_limit))def resources(planet):    global f    try:        power_balance = planet.energy / (planet.metal_mine.power_cost + planet.no_metal_mine.power_cost + planet.gas_refinery.power_cost)    except:        power_balance = 0    return f, int(time.time()), power_balance    def clear():    a = False    if a:        os.system('clear')def enter():    try:        a = int(input())    except:        a = -1    return adef start(user):    a = 0    p = user.planets[0]    while True:        print("\nPlanet " + str(p.coordinates) + ": " + p.name + "\n")        print("What do u wanna do?\n" +              "[1] Build\n" +              "[2] Research\n" +              "[3] Explore\n" +              "[4] Ship\n" +              "[5] Inform\n" +              "[6] Switch\n" +              "[7] Rename\n" +              "[8] Logout\n")        a = enter()        clear()        if a == 1:            print("What do u wanna build?\n" +                  "[1] Buildings\n" +                  "[2] Shipping\n")            a = enter()            clear()            if a == 1:                print("What do u wanna build?\n" +                      "[1] Metal mine\n" +                      "[2] No metal mine\n" +                      "[3] Gas Refinery\n" +                      "[4] Power plant\n" +                      "[5] Metal repository\n" +                      "[6] No metal repository\n" +                      "[7] Gas tank\n" +                      "[8] Shipyard\n")                a = enter()                clear()                if a == 1:                    b = p.metal_mine                elif a == 2:                    b = p.no_metal_mine                elif a == 3:                    b = p.gas_refinery                elif a == 4:                    b = p.power_plant                elif a == 5:                    b = p.metal_repository                elif a == 6:                    b = p.no_metal_repository                elif a == 7:                    b = p.gas_tank                elif a == 8:                    b = p.shipyard                else:                    print("Invalid input")                    continue                print("Are u sure? [1] Sí  |  [0] No\n")                print("Metal cost = " + str(b.metal_cost) + " | No metal cost = " + str(b.no_metal_cost) + "\n")                a = enter()                clear()                if a == 1:                    build(p, b)                elif a == 0:                    print("Any change made")                else:                    print("Invalid input")            elif a == 2:                print("What do u wanna build?\n" +                      "[1] Battleship\n" +                      "[2] Hunter\n" +                      "[3] Colonizer\n" +                      "[4] Spy\n")                a = enter()                clear()                if a == 1:                    ship = battleship                    req = "Requirements: Shipyard level 1, Weapon level 2, Structure level 2, Motor level 2"                elif a == 2:                    ship = hunter                    req = "Requirements: Shipyard level 5, Weapon level 5, Structure level 5, Motor level 5"                elif a == 3:                    ship = colonizer                    req = "Requirements: Shipyard level 4, Colonize level 1, Structure level 4, Motor level 4"                elif a == 4:                    ship = spy                    req = "Requirements: Shipyard level 3, Spying level 1, Structure level 2, Motor level 2"                else:                    print("Invalid input")                    continue                print("How many?")                am = enter()                clear()                if am == -1:                    print("Invalid input")                    continue                print("Are u sure? [1] Sí  |  [0] No\n")                print(req)                a = enter()                clear()                if a == 1:                    build_fleet(p, user, ship, am)                elif a == 0:                    print("Any change made")                else:                    print("Invalid input")            else:                print("Invalid input")        elif a == 2:            print("Coming soon")        elif a == 3:            print("Coming soon")        elif a == 4:            print("Coming soon")        elif a == 5:            print("What do u wanna know?\n" +                  "[1] Resources\n" +                  "[2] Fleet\n")            a = enter()            clear()            if a == -1:                print("Invalid input")            elif a == 1:                show(p)            elif a == 2:                print(p.fleet)        elif a == 6:            print("What planet u wanna go to?\n")            for i in range(len(user.planets)):                print("[" + str(i) + "] " + user.planets[i].name)            print()            a = enter()            if a == -1 or a >= len(user.planets):                print("Invalid input")            else:                p = user.planets[a]        elif a == 7:            print("What's the new name?\n")            a = input()            p.rename(a)        elif a == 8:            break        else:            print("Invalid input")#Testing of gamegenerate_universe(100)u = user("reluro", "kk12345")rand_assign(u)#Objects of classbattleship = ship("Battleship", 100, 1_000, 5, False, 500, 500, 300)hunter = ship("Hunter", 1000, 5_000, 10, False, 2_000, 2_000, 1_500)colonizer = ship("Colonizer", 0, 2_500, 2, True, 20_000, 20_000, 15_000)spy = ship("Spy", 0, 500, 30, False, 3_000, 0, 1_000)start(u)#Game beginning##try:##    uf = open("users.game", "r+")##    gf = open("game.game", "r+")##    pf = open("password.game", "r+")##except:##    print("Data not found...\n" +##          "Your username will be created in a new game file.")##    uf = open("users.game", "w+")##    gf = open("game.game", "w+")##    pf = open("password.game", "w+")##    a = 3##while True:##    if a == 0:##        print("What do u wanna do?\n" +##              "[0] Login\n" +##              "[1] Register\n" +##              "[2] Exit\n")##        a = enter()##    if a == 0 or  a == 1 or a == 3:##        print("Enter username:")##        u = input()##        if u == "" or u == "-":##            print("Invalid user. Try again")##            a = 0##            continue##        print("Enter password:")##        p = input()##		clear()##        if a != 3:##            ufd = uf.read()##            gfd = gf.read()##            pfd = pf.read()##            if a == 0:##                if ufd.find(u) == -1 or pfd.find(p) == -1:##                    print("Username or password error")##                    continue##            else:##                if ufd.find(u) != -1:##                    print("Username already exists")##                    continue##            regenerate_universe(gfd, ufd, pfd)##        else:##            generate_universe(100)##            start()##    elif a == 2:##        print("Thanks for playing")##        break##    else:##        print("Unknown answer\n")