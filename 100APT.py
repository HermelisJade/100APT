# 100APT — Apartment Builder Simulator

import random, sys
import os
from datetime import datetime

# --- Game Constants ---
TOTAL_WEEKS = 52  # test; final - 52
ACTIONS_PER_WEEK = 7 # test; final - 7
STARTING_CAPITAL = 500
MAX_FLOORS = 100  # test; final - 100
PREF_BONUS = 0.10
BANKRUPT_LIMIT = -50

APT_TYPES = [
    "Desert Suite","Ocean Chamber","Forest Cabin","Factory Loft","Snowfield Hut","Hogwarts Nook",
    "Cyberpunk Pod","Space Capsule","Underworld Den","Sky Garden","Steampunk Room","Sakura Retreat",
    "Zen Chamber","Arctic Ice Room","Volcano Forge","Jungle Bungalow","Aquarium Dome",
    "Grand Library","Music Studio","Gamer's Den"
]

TYPE_BUILD_COST = {
    "Desert Suite":90,"Ocean Chamber":120,"Forest Cabin":80,"Factory Loft":110,"Snowfield Hut":85,
    "Hogwarts Nook":140,"Cyberpunk Pod":130,"Space Capsule":150,"Underworld Den":115,"Sky Garden":125,
    "Steampunk Room":120,"Sakura Retreat":95,"Zen Chamber":100,"Arctic Ice Room":130,"Volcano Forge":140,
    "Jungle Bungalow":105,"Aquarium Dome":135,"Grand Library":120,"Music Studio":110,"Gamer's Den":100
}

# Maintenance base
TYPE_BASE_MAINT = {k: max(5, v//15 + 4) for k, v in TYPE_BUILD_COST.items()}

TENANTS = [
    ("Alice","Sakura Retreat"),("Bob","Factory Loft"),("Charlie","Grand Library"),("Diana","Zen Chamber"),
    ("Ethan","Music Studio"),
    ("Mermaid","Ocean Chamber"),("Elf","Forest Cabin"),("Werewolf","Jungle Bungalow"),("Witch","Hogwarts Nook"),
    ("Vampire","Underworld Den"),("Dragon","Volcano Forge"),("Phoenix","Sky Garden"),
    ("Goblin","Factory Loft"),("Fairy","Sakura Retreat"),("Dwarf","Steampunk Room"),("Giant","Space Capsule"),
    ("Wizard","Hogwarts Nook"),("Nymph","Aquarium Dome"),("Kraken","Ocean Chamber"),
    ("Yeti","Arctic Ice Room"),("Djinn","Desert Suite"),("Satyr","Music Studio"),("Valkyrie","Sky Garden"),
    ("Golem","Factory Loft"),("Chimera","Volcano Forge"),("Naga","Aquarium Dome"),
    ("Bard","Music Studio"),("Monk","Zen Chamber"),("Ranger","Forest Cabin"),
    ("Astronaut","Space Capsule"),("Blacksmith","Volcano Forge"),("Librarian","Grand Library"),
    ("Programmer","Gamer's Den"),
    ("Wanderer",None),("Hermit",None)
]

LABEL = {
    "Desert Suite":"DSR","Ocean Chamber":"OCN","Forest Cabin":"FST","Factory Loft":"FAC","Snowfield Hut":"SNW",
    "Hogwarts Nook":"HWG","Cyberpunk Pod":"CBR","Space Capsule":"SPC","Underworld Den":"UDN","Sky Garden":"SKY",
    "Steampunk Room":"STP","Sakura Retreat":"SKR","Zen Chamber":"ZEN","Arctic Ice Room":"ARC","Volcano Forge":"VOL",
    "Jungle Bungalow":"JNG","Aquarium Dome":"AQM","Grand Library":"LIB","Music Studio":"MUS","Gamer's Den":"GAM"
}

# --- Classes ---
class Apartment:
    def __init__(self, floor, apt_type, base_rent):
        self.floor = floor
        self.apt_type = apt_type
        self.base_rent = base_rent
        self.tenant = None

class Tenant:
    def __init__(self,name,preference):
        self.name=name
        self.preference=preference

class Building:
    def __init__(self, starting_capital=STARTING_CAPITAL):
        self.capital = starting_capital
        self.floors = []
        self.week = 1
        self.income_history = []
        self.build_log = {}
        self.movein_log = {}
        self.tower_name = ""

    def total_floors(self):
        return len(self.floors)

    def add_floor(self, apt_type):
        if self.total_floors() >= MAX_FLOORS:
            print("❌ Cannot build more floors.")
            return False
        cost = TYPE_BUILD_COST[apt_type]
        if self.capital < cost:
            print("❌ Not enough capital.")
            return False

        base = int(cost * 0.6)
        floor_num = self.total_floors() + 1
        self.floors.append(Apartment(floor_num, apt_type, base))
        self.capital -= cost

        self.build_log.setdefault(self.week, []).append({
            "floor": floor_num, "type": apt_type, "cost": cost
        })

        print(f"✅ Built Floor {floor_num}: {apt_type} | Cost {cost} | Capital {self.capital}")
        return True

    def assign_tenant(self, tenant, floor_no):
        if floor_no < 1 or floor_no > self.total_floors():
            print("❌ Invalid floor.")
            return False
        apt = self.floors[floor_no-1]
        if apt.tenant:
            print("❌ Floor already occupied.")
            return False
        apt.tenant = tenant

        self.movein_log.setdefault(self.week, []).append({
            "floor":floor_no,"tenant":tenant.name
        })

        print(f"✅ {tenant.name} moved into Floor {floor_no}")
        return True

    def weekly_maintenance(self):
        ground = 20 + self.total_floors()
        cost = 0
        for apt in self.floors:
            cost += TYPE_BASE_MAINT[apt.apt_type] + int(1.5 * apt.floor)
        return ground + cost

    def settle_week(self):
        income = 0
        for apt in self.floors:
            if apt.tenant:
                rent = apt.base_rent
                if apt.tenant.preference == apt.apt_type and apt.tenant.preference:
                    rent = int(rent * (1 + PREF_BONUS))
                income += rent

        maint = self.weekly_maintenance()
        net = income - maint
        self.capital += net
        self.income_history.append(self.capital)
        return income, maint, net
    
    def save_week_log(self, week, income, maint, net):
        with open("game_log.txt", "a", encoding="utf-8") as f:
            # write title of week log of each round in week1
            if week == 1:
                f.write("\n" + "="*50 + "\n")
                f.write(f"🏢 Building: {self.tower_name}\n")
                f.write(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"💵 Starting Capital: {self.start_capital}\n")
                f.write("="*50 + "\n")
            
            f.write(f"\n===== Week {week} =====\n")
            f.write(f"Income: {income}, Maintenance: {maint}, Net: {net}, Capital: {self.capital}\n\n")

            f.write("[Build Log]\n")
            for r in self.build_log.get(week, []):
                f.write(f" Built Floor {r['floor']} {r['type']} (Cost {r['cost']})\n")
            if week not in self.build_log:
                f.write(" None\n")

            f.write("\n[Move-in Log]\n")
            for r in self.movein_log.get(week, []):
                f.write(f" {r['tenant']} -> Floor {r['floor']}\n")
            if week not in self.movein_log:
                f.write(" None\n")

    def print_week_log(self, week, income, maint, net):
        print("\n[Weekly Build Log]")
        for r in self.build_log.get(week, []):
            print(f" Built Floor {r['floor']} {r['type']} (Cost {r['cost']})")
        if week not in self.build_log:
            print(" None")

        print("\n[Move-in Log]")
        for r in self.movein_log.get(week, []):
            print(f" {r['tenant']} -> Floor {r['floor']}")
        if week not in self.movein_log:
            print(" None")

        print(f"\n[Weekly Summary]")
        print(f"Income {income} | Maintenance {maint} | Net {net} | Capital {self.capital}")

    # ====== Tower Display ======
    def draw(self, width: int = 22, indent: int = 4, quiet: bool = False):
        IND = " " * indent
        inner = width - 2

        top_border  = IND + "┌" + "─" * (width - 2) + "┐"
        mid_border  = IND + "├" + "─" * (width - 2) + "┤"

        # ground same width as building
        ground_line = IND + "▒" * width

        def block(a="", b=""):
            '''
            Draw a block in the tower display.
            a: Tenant name (left)
            b: Apartment type (right)
            '''
            print(IND + "|" + a.center(inner) + "|")
            print(IND + "|" + b.center(inner) + "|")
        if not quiet:
            print(f"\n========== Week {self.week} ==========")
        print(top_border)

        for apt in reversed(self.floors):
            room = apt.apt_type
            tenant_name = apt.tenant.name if apt.tenant else "---"
            tenant_display = f"Tenant: {tenant_name}"
            block(room, tenant_display)
            print(mid_border)


        block("GROUND FLOOR", f'<< {self.tower_name} >>')
        print(ground_line)
        if not quiet:
            total = len(self.floors)
            empty = sum(1 for apt in self.floors if apt.tenant is None)
            print(f"\n{IND}🏢 Units: {total}  |  Empty: {empty}/{total}")
            print(f"{IND}💰 Capital: {self.capital}\n")

# --- Input helpers ---
def ask_yes(q):
    while True:
        c = input(q).strip().lower()

        # Allow exit
        if c in ("q", "quit", "exit"):
            print("\n👋 Exiting game. Goodbye!\n")
            sys.exit(0)

        if c in ("y", "yes"):
            return True
        elif c in ("n", "no"):
            return False

        print("Enter y/yes or n/no (or q to quit)")

def safe_int(prompt,low,high):
    s = input(prompt).strip().lower()

    # quit support
    if s in ("q", "quit"):
        print("\n👋 Exiting game early. See you next time!\n")
        sys.exit(0)

    # must be number
    if not s.isdigit():
        print("❌ Invalid input. Please enter a valid number.")
        return None

    v = int(s)
    if low <= v <= high:
        return v

    print(f"❌ Invalid input. Please enter a valid number from {low} to {high}")
    return None

def pick3(arr): 
    return random.sample(arr,3)

def choose_build():
    cancel_count = 0
    while True:
        opts = pick3(APT_TYPES)
        print("Select apartment type to build:")
        for i, o in enumerate(opts, 1):
            print(f"  {i}. {o} (Cost {TYPE_BUILD_COST[o]})")
        print("  0. Cancel (max 3)")

        c = safe_int("> ", 0, len(opts))

        # Invalid — no penalty
        if c is None:
            print("❌ Invalid input. Try again.")
            continue
        
        # Cancel logic
        if c == 0:
            cancel_count += 1
            if cancel_count >= 3:
                print("⚠️ Too many cancellations. Action consumed.")
                return "FORCE_SPEND"
            print(f"🔙 Returning to action selection... Choose again. \n⚠️ Only 3 cancellations allowed.({cancel_count}/3).")
            continue

        # Valid selection
        return opts[c - 1]

def choose_tenant():
    cancel_count = 0
    while True:
        cand = pick3(TENANTS)
        objs = [Tenant(n, p) for n, p in cand]
        print("Choose tenant:")
        for i, t in enumerate(objs, 1):
            pref = t.preference if t.preference else "None"
            print(f"  {i}. {t.name} (Pref {pref})")
        print("  0. Cancel (3 max)")

        c = safe_int("> ", 0, len(objs))

        # invalid input: not counted, no penalty
        if c is None:
            print("❌ Invalid input. Not counted. Try again.")
            continue

        # cancel selection
        if c == 0:
            cancel_count += 1
            if cancel_count >= 3:
                print("⚠️ Too many cancellations. Action consumed.")
                return "FORCE_SPEND", None
            print(f"🔙 Returning to action selection... Choose again. \n⚠️ Only 3 cancellations allowed.({cancel_count}/3).")
            continue

        # valid selection
        return objs[c - 1]

# --- Game ---
def play(starting_capital=STARTING_CAPITAL, skip_intro=False):
    if not skip_intro:
        print(f"""
Welcome to 100APT — Apartment Builder Simulator!

Goal: Build floors, assign tenants, and manage finances.
Each week you have {ACTIONS_PER_WEEK} actions to grow your building and maximize profit.

💡 Tip: Assigning a tenant to their preferred apartment theme grants a +{int(PREF_BONUS*100)}% rent bonus.

Good luck — your real-estate journey starts now! 🏙️
""")
        
    if not ask_yes("Start game? (y/n) "):
        print("\n👋 Thanks for checking out 100APT — Apartment Builder Simulator!")
        print("Maybe next time you'll build a legendary skyscraper. 🏙️✨\n")
        sys.exit(0)
    
    tower_name = input("Name your apartment tower: ").strip()
    if tower_name == "":
        tower_name = "Unnamed Tower"
    print(f"\n🏢 Tower: {tower_name}\n")


    b = Building(starting_capital)
    b.tower_name = tower_name
    b.start_capital = starting_capital  # save for game_log

    for wk in range(1, TOTAL_WEEKS+1):
        b.week = wk
        b.draw()

        actions = 0
        while actions < ACTIONS_PER_WEEK:
            print(f"\n📍 Event {actions+1}/{ACTIONS_PER_WEEK}")
            print("Choose an action (1/2/3/4):")
            print(" 1) Build floor")
            print(" 2) Assign tenant")
            print(" 3) Skip turn")
            print(" 4) Fast-forward to end of year")

            choice = input("> ").strip()
            if choice in ("q", "quit"):
                print("\n👋 Exiting game early. See you next time!\n")
                sys.exit(0)
            
            # fast-forward to end of year
            if choice == "4":
                for remain in range(wk, TOTAL_WEEKS+1):
                    b.week = remain
                    income, maint, net = b.settle_week()
                    b.save_week_log(remain, income, maint, net)
                print("\n⏩ Fast-forward activated! Skipped to year end.")
                return b.capital
            
            if choice not in ("1","2","3"):
                print("❌ Invalid input (no action spent).")
                continue
            
            # build floor: is_full situation
            if choice == "1" and b.total_floors() >= MAX_FLOORS:
                print("🏢 Maximum floors reached.")

                empty_units = sum(1 for apt in b.floors if apt.tenant is None)

                if empty_units > 0:
                    # Floors full, still vacancies
                    print(f"📌 There are still {empty_units} empty units.")
                    if ask_yes("Do you want to continue leasing this year? (y/n) "):
                        print("🔙 Continue finding tenants.")
                        continue
                    else:
                        # player chooses skip leasing and fast-forward
                        for remain in range(wk, TOTAL_WEEKS+1):
                            b.week = remain
                            income, maint, net = b.settle_week()
                            b.save_week_log(remain, income, maint, net)
                        print("\n⏩ Fast-forwarded to year end.")
                        return b.capital
                else:
                    # Floors and tenants both full — perfect state
                    print("🎉 Building is fully constructed AND fully occupied!")
                    if ask_yes("Skip to year end? (y/n) "):
                        for remain in range(wk, TOTAL_WEEKS+1):
                            b.week = remain
                            income, maint, net = b.settle_week()
                            b.save_week_log(remain, income, maint, net)
                        print("\n⏩ Everything full — fast-forwarded to year end!")
                        return b.capital
                    print("🔙 Returning to action selection... (no action spent)")
                    continue

            # assign tenant: is_full situation
            if choice == "2" and b.total_floors() >= MAX_FLOORS and all(apt.tenant for apt in b.floors):
                print("🎉 Building is fully constructed AND fully occupied!")
                if ask_yes("Skip to year end? (y/n) "):
                    for remain in range(wk, TOTAL_WEEKS+1):
                        b.week = remain
                        income, maint, net = b.settle_week()
                        b.save_week_log(remain, income, maint, net)
                    print("\n⏩ Everything full — fast-forwarded to year end!")
                    return b.capital
                else:
                    print("🔙 Returning to action selection... (no action spent)")
                    continue

            # normal situation
            # build floor
            if choice == "1":
                t = choose_build()

                # forced action spend
                if t == "FORCE_SPEND":
                    actions += 1
                    continue

                # normal cancel
                if not t:
                    print("🔙 Returning to action selection... (no action spent)")
                    continue

                # valid build
                if b.add_floor(t):
                    actions += 1

            # assign tenant
            elif choice == "2":
                if b.total_floors()==0:
                    print("❌ No floors yet.")
                    print("🔙 Returning to action selection... (no action spent)")
                    continue

                # check if all floors are occupied
                if all(apt.tenant for apt in b.floors):
                    print("❌ No available apartments for tenants right now.")
                    print("🔙 Returning to action selection... (no action spent)")
                    continue

                tenant = choose_tenant()
                if tenant == "FORCE_SPEND":
                    actions += 1
                    continue

                if not tenant:
                    print("🔙 Returning to action selection... (no action spent)")
                    continue

                # show tower before selection
                print("\nCurrent Building:")
                b.draw(quiet=True)  # only show tower blueprint

                # floor selection loop
                while True:
                    fl = safe_int(f"Select floor (1-{b.total_floors()}): ",1,b.total_floors())

                    if fl is None:
                        continue

                    if b.assign_tenant(tenant, fl):
                        actions += 1
                    break

            else:  # choice == "3"
                print("⏭️ Skip turn")
                actions+=1

        try:
            income, maint, net = b.settle_week()
            b.save_week_log(wk, income, maint, net)  # Save weekly log to file
        except:
            print("Settlement error.")
        
        # show weekly log
        if ask_yes("View weekly log? (y/n) "):
            b.print_week_log(wk, income, maint, net)

    return b.capital

if __name__ == "__main__":
    try:
        capital = STARTING_CAPITAL  # initialize capital
        first_game = True  # flag
        
        while True:
            if not first_game:
                print(f"💼 You start this project with capital carried over: ${capital}")
            
            round_start = capital  # start capital for this round, used for review

            result = play(capital, skip_intro=not first_game)  # only first round show intro
            capital = result  # carry over capital
            first_game = False  # skip intro after first round
            
            print(f"💰 Final Capital: {result}")
            if capital <= BANKRUPT_LIMIT:
                print(f"\n💥 Bankruptcy detected! Resetting capital to ${STARTING_CAPITAL}")
                print("📉 Real estate is tough... but every tycoon starts somewhere. Try again!")
                capital = STARTING_CAPITAL
            else:
                # Capital review
                print(f"\n🎉 Year complete!")
                if capital < round_start:
                    print("🏙️ You survived the year — not easy in real estate! Keep improving.")
                elif capital == round_start:
                    print("⚖️ Broke even — safe play! Maybe take some risks next time.")
                else:  # capital > round_start
                    print("💼 Great job, developer! Your building thrived and tenants flourished!")

            # Show log path after each finished building cycle
            log_path = os.path.join(os.getcwd(), "game_log.txt")
            print(f"📁 Log saved at: {log_path}")

            # Ask if user wants another run
            if not ask_yes("\n🏢 Start a new apartment building? (y/n) "):
                print("\n👋 Thanks for playing 100APT — See you next time!")
                sys.exit(0)

            # Capital carry-over logic
            # if the player is bankrupt, reset capital
            print("Preparing your next building...")
            print("🎉 Your new building awaits!\n")

    except KeyboardInterrupt:
        print("\nExit"); sys.exit(0)

