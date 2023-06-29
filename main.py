import pygame
import random
import pickle
import time

pygame.init()
# Define the map size
MAP_WIDTH = 11
MAP_HEIGHT = 10

# Define the tile size
TILE_SIZE = 100
BACKGROUND_COLOR = (0, 0, 0)  # Black
# Set up the Pygame window
window_width = MAP_WIDTH * TILE_SIZE
window_height = MAP_HEIGHT * TILE_SIZE
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("RPG Game")



# Define the colors for map elements
#COLOR_TREE = (34, 139, 34)  # Green
image_tree = pygame.image.load(("../map_with_player/tree#9.png")).convert_alpha()
#COLOR_TREE = image.get_rect()
#COLOR_FLOWER = (255, 20, 147)  # Pink
image_flower = pygame.image.load(("../map_with_player/Natural/foxglove.png")).convert_alpha()

image_water = pygame.image.load(("../map_with_player/water/water_tileset.png")).convert_alpha()

im_t = pygame.image.load(("../map_with_player/treasure/chest2.png")).convert_alpha()
image_treasure_chest = pygame.transform.scale(im_t, (70, 70))
#COLOR_TREASURE = (255, 215, 0)  # Gold

image_player = pygame.image.load(("../map_with_player/player/walk1.png")).convert_alpha()
#COLOR_PLAYER = (255, 0, 0)  # Red

image_m = pygame.image.load(("../map_with_player/mobs/mintaur.png")).convert_alpha()
image_mob = pygame.transform.scale(image_m, (90, 90))

image_m2 = pygame.image.load(("../map_with_player/mobs/mintaur.png")).convert_alpha()
image_mob_ork = pygame.transform.scale(image_m2, (90, 90))

# Define the weather conditions
WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Stormy"]





def generate_weapon_loot():
    attributes = {
        "Type": random.choice(["Sword", "Axe", "Bow", "Staff"]),
        "Material": random.choice(["Iron", "Steel", "Wood", "Obsidian"]),
        "Damage": random.randint(10, 50),
        "Durability": random.randint(50, 100),
        "Element": random.choice(["None", "Fire", "Ice", "Lightning"]),
        "Elemental Damage": random.randint(5, 20),
        "Rarity": random.choice(["Common", "Uncommon", "Rare", "Legendary"]),
    }
    return attributes

# Generate a random map
def generate_map():
    # Create an empty map
    map_data = [[" " for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    # Place trees randomly on the map
    for _ in range(random.randint(5, 10)):
         x = random.randint(0, MAP_WIDTH - 1)
         y = random.randint(0, MAP_HEIGHT - 1)
         map_data[y][x] = "T"

    # Generate initial water sources (ponds)
    for _ in range(random.randint(2, 4)):
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)
        map_data[y][x] = "W"

    # Run cellular automaton iterations to simulate water spreading
    num_iterations = 5
    for _ in range(num_iterations):
        new_map_data = [[" " for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                # Check the neighboring cells for water presence
                water_neighbors = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and map_data[ny][nx] == "W":
                            water_neighbors += 1

                # Determine the next state of the cell based on water neighbor count
                if map_data[y][x] == "W" or (map_data[y][x] == " " and water_neighbors >= 4):
                    new_map_data[y][x] = "W"
                else:
                    new_map_data[y][x] = " "

        map_data = new_map_data

    # Place flowers randomly on the map
    for _ in range(random.randint(10, 20)):
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)
        map_data[y][x] = "F"

    # Place water randomly on the map
    for _ in range(random.randint(2, 5)):
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)
        map_data[y][x] = "W"

    # Place the treasure randomly on the map
    x = random.randint(0, MAP_WIDTH - 1)
    y = random.randint(0, MAP_HEIGHT - 1)
    map_data[y][x] = "X"

    return map_data

# Player class
class Player1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            self.x = new_x
            self.y = new_y

    def pickup_treasure(self):
        if map_data[self.y][self.x] == "X":
            self.inventory.append("Treasure")
            map_data[self.y][self.x] = " "
            loot = generate_weapon_loot()
            print(f"You picked up the treasure!, Your treasure is {loot}")

        if map_data[self.y][self.x] == "F":
            self.inventory.append("Flower")
            map_data[self.y][self.x] = " "
            print("You picked a flower!")

class Player:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = max_health
        self.inventory = []

    def move(self, dx, dy):
        # Move the player
        self.x += dx
        self.y += dy

    def take_damage(self, damage):
        # Reduce the player's health by the given amount
        self.health -= damage

        # Check if the player's health has reached zero or below
        if self.health <= 0:
            self.health = 0
            print("Player has been defeated!")

    def draw(self, window):
        # Draw the player on the game window
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def pickup_treasure(self):
        if map_data[self.y][self.x] == "X":
            self.inventory.append("Treasure")
            map_data[self.y][self.x] = " "
            loot = generate_weapon_loot()
            print(f"You picked up the treasure!, Your treasure is {loot}")

        if map_data[self.y][self.x] == "F":
            self.inventory.append("Flower")
            map_data[self.y][self.x] = " "
            print("You picked a flower!")

class Mob1:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            self.x = new_x
            self.y = new_y

# Mob class
class Mob:
    def __init__(self, name, x, y, health, attack_damage, image):
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.attack_damage = attack_damage
        self.image = image

        # Ranged attack properties
        self.attack_range = 200
        self.attack_cooldown = 60  # Number of frames between each attack
        self.attack_timer = 0


    def move(self):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            self.x = new_x
            self.y = new_y

    def attack(self, target):
        if self.attack_timer <= 0:
            # Check if the target is within the attack range
            distance = ((self.x - target.x) ** 2 + (self.y - target.y) ** 2) ** 0.5
            if distance <= self.attack_range:
                # Create a projectile or perform the ranged attack
                # Here, we'll just print a message for demonstration purposes
                print(f"The {self.name} attacks with a ranged attack!")

                # Reset the attack timer
                self.attack_timer = self.attack_cooldown

    def update(self):
        # Update the attack timer
        if self.attack_timer > 0:
            self.attack_timer -= 1

    def draw(self, window):
        # Draw the mob on the game window
        window.blit(self.image, (self.x, self.y))

class Projectile:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage

    def update(self):
        # Move the projectile
        self.x += self.speed

    def check_collision(self, target):
        # Check for collision with the target (e.g., player)
        if self.x < target.x + target.width and self.x + self.width > target.x and self.y < target.y + target.height and self.y + self.height > target.y:
            return True
        return False


# Function to save the game
def save_game(player):
    data = {
        "player": player,
    }

    with open("savegame.dat", "wb") as file:
        pickle.dump(data, file)

# Function to load the game
def load_game():
    try:
        with open("savegame.dat", "rb") as file:
            data = pickle.load(file)
            return data["player"]
    except FileNotFoundError:
        print("No save file found.")
        return None

# Create the player object
player = Player(x=0, y=0, width=50, height=50, max_health=100)

# Save the game
save_game(player)
print("Game saved.")

# Load the game
loaded_player = load_game()
if loaded_player is not None:
    print("Player position:", loaded_player.x, loaded_player.y)
    print("Player inventory:", loaded_player.inventory)

# Initialize Pygame
pygame.init()

# Set up the Pygame window
window_width = MAP_WIDTH * TILE_SIZE
window_height = MAP_HEIGHT * TILE_SIZE
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("RPG Map")

# Generate the map data
map_data = generate_map()
weather = random.choice(WEATHER_CONDITIONS)



# Set the delay between mob movements
MOVEMENT_DELAY = 0.5  # Adjust this value to control the speed of the mob

# Create the mob object

mob = Mob(name="ork", x=0, y=20, health=10, attack_damage=20, image=image_mob_ork)
# Initialize the start time
start_time = time.time()

# Define the projectiles list
projectiles = []

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            elif event.key == pygame.K_UP:
                player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
            elif event.key == pygame.K_SPACE:
                player.pickup_treasure()
    # Update the mob's position with delay
    #if time.time() - start_time >= MOVEMENT_DELAY:
    #    mob.move()
    #    start_time = time.time()

    # Clear the window
    window.fill((40, 150, 0))  # green

    # Draw the map elements
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == "T":
                window.blit(image_tree, (x * TILE_SIZE, y * TILE_SIZE))
                    #(window, COLOR_TREE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == "F":
                window.blit(image_flower, (x * TILE_SIZE, y * TILE_SIZE))
                #pygame.draw.rect(window, COLOR_FLOWER, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == "W":
                window.blit(image_water, (x * TILE_SIZE, y * TILE_SIZE))
                #pygame.draw.rect(window, COLOR_WATER, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == "X":
                window.blit(image_treasure_chest, (x * TILE_SIZE, y * TILE_SIZE))


                #pygame.draw.rect(window, COLOR_TREASURE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw the player

    window.blit(image_player, (player.x * TILE_SIZE, player.y * TILE_SIZE))
    #window.blit(image_mob, (mob.x * TILE_SIZE, mob.y * TILE_SIZE))

    # Update and draw the mob
    mob.move()
    mob.draw(window)
    mob.update()



    #pygame.draw.rect(window, COLOR_PLAYER, (player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Update and check collisions for projectiles
    for projectile in projectiles:
        projectile.update()

        # Check collision with the player
        if projectile.check_collision(player):
            player.take_damage(projectile.damage)
            projectiles.remove(projectile)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()


