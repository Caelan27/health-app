from game.core.tile import Tile
from game.entities.empty import Empty
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.items import Item
from game.entities.creature import Creature
from game.core.entity_factory import EntityFactory
from game.helpers import is_adjacent
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from random import randint, choice
from kivy.core.audio import SoundLoader


class GameState(EventDispatcher):
    """
    A subclass of EventDispatcher to handle most of the game's logic.

    Attributes:
        curr_player_health (NumericProperty):
            Stores the player's current health
        max_player_health (NumericProperty):
            Stores the player's maximum health
        player_speed (NumericProperty):
            Stores the player's speed
        player_attack_damage (NumericProperty):
            Stores the player's attack damage
        game_over (BooleanProperty):
            Stores whether or not the game is finished

        width (int):
            The number of columns on the screen
        height (int):
            The number of rows on the screen
        grid (list[list[Tile]]):
            Stores the tiles on the screen, displayed in a grid
        current_actor (Entity):
            Stores the entity whose turn it is currently
        entity_factory (EntityFactory):
            An EntityFactory used to create entities
        player (Entity):
            The player entity
        enemy_spawn_timer (int):
            The number of turns until a new enemy will spawn
        item_spawn_timer (int):
            The number of turns until a new item will spawn

        eating_sound (Sound):
            The sound to play when the player eats
        punch_sound (Sound):
            The sound to play when the player punches
    """

    curr_player_health = NumericProperty()
    max_player_health = NumericProperty()
    player_speed = NumericProperty()
    player_attack_damage = NumericProperty()
    score = NumericProperty(0)

    eating_sound = SoundLoader.load("game/audio/eating.wav")
    punch_sound = SoundLoader.load("game/audio/punch.wav")

    def __init__(self, width, height):
        """
        Initialises the GameState.

        Args:
            width (int):
                The number of columns in the screen
            height (int):
                The number of rows in the screen

        Actions:
            - Initialises self.width and self.height
            - Creates an empty grid
            - Sets the current actor to None
            - Creates an EntityFactory
            - Create the player at the position (0, 0)
            - Start enemy and item spawn timers
            - Initialises the grid
        """
        super().__init__()

        self.width = width
        self.height = height

        self.grid = []

        self.current_actor = None

        self.entity_factory = EntityFactory()

        self.player = self.entity_factory.create_player((0, 0))

        self.enemy_spawn_timer = randint(5, 20)
        self.item_spawn_timer = randint(5, 20)

        self.curr_player_health = self.player.curr_health
        self.max_player_health = self.player.max_health
        self.player_speed = self.player.speed
        self.player_attack_damage = self.player.attack_damage

        self.initialise_grid()

    def initialise_grid(self):
        """
        Initialises the grid.

        Actions:
            - Adds the correct number of buttons to the grid
            - Adds the player to the grid
            - Adds an item to the grid
            - Adds an enemy to the grid
            - Starts the game by advancing time
        """
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[y].append(Tile(Empty()))

        (player_x, player_y) = self.player.position
        self.grid[player_y][player_x].entity = self.player

        self.spawn_item()

        self.spawn_enemy()

        self.advance_time()

    def move_creature(self, creature, destination):
        """
        Moves a creature entity to another position.

        Args:
            - creature (Entity):
                The entity to be moved
            - destination (tuple[int, int]):
                The position to move to

        Actions:
            - Checks the destination is within the grid
            - Checks the destination is empty
            - Changes the entity of the destination tile to the creature
            - Updates the creature's position attribute
            - Makes the creature's original position empty

        Returns:
            - boolean:
                True if the creature successfully moved, False if not
        """
        (origin_x, origin_y) = creature.position
        (destination_x, destination_y) = destination

        if not self.in_bounds(destination):
            return False

        if not isinstance(self.grid[destination_y][destination_x].entity, Empty):
            return False

        self.grid[destination_y][destination_x].entity = creature
        creature.position = destination
        self.grid[origin_y][origin_x].entity = Empty()

        return True

    def interact_with_tile(self, tile_location):
        """
        Handles the player trying to interact with a tile.

        Args:
            - tile_location (tuple[int, int]):
                The position of the tile the player tried to interact with

        Actions:
            - Checks that it is the player's turn
            - Goes through each entity type and decides the action based on it.
                If it's Empty, the player should move there.
                If it's an Item, the player should use that item.
                If it's a Creature, the player should attack the creature
            - If the player did something:
                - Play the appropriate sound
                - Handle the player's stat decay
                - Handle the end of turn operations.
        """

        (tile_x, tile_y) = tile_location
        tile = self.grid[tile_y][tile_x]
        entity = tile.entity

        did_something = False
        if self.current_actor == self.player:
            if isinstance(entity, Empty):
                did_something = self.move_player(tile_location)
            elif isinstance(entity, Item):
                did_something = self.use_item(tile_location)
                if did_something:
                    self.eating_sound.play()
            elif isinstance(entity, Creature):
                did_something = self.attack_creature(
                    self.player, tile_location)
                if did_something:
                    self.punch_sound.play()

        if did_something:
            self.handle_decay()
            self.end_turn()

    def enemy_turn(self):
        """
        Performs the enemy's turn.

        Actions:
            - Makes the enemy take a turn
            - Handle the end of turn operations
        """
        self.current_actor.take_turn(self)
        self.end_turn()

    def handle_decay(self):
        """
        Handles the player's stat decay.

        Actions:
            - Decays the players stats
            - Decreases the countdowns on the player's decay wearing out
        """
        self.player.decay()
        self.player.decay_countdown()

    def end_turn(self):
        """
        Handles end of turn operations.

        Actions:
            - Decreases the turn meter of the entity that took a turn
            - Resets the current actor
            - If the player died, handle their death
            - Remove any dead entities from the grid
            - Decrease the enemy and item spawn timers
            - Spawn an enemy / item and reset the timer if they ran out
            - Advance time
        """
        actor = self.current_actor

        if actor is not None:
            actor.turn_meter -= 100

        self.current_actor = None

        if not self.player.is_alive:
            self.handle_player_death()

        self.remove_dead()

        self.enemy_spawn_timer -= 1
        if self.enemy_spawn_timer == 0:
            self.spawn_enemy()
            self.enemy_spawn_timer = randint(5, 20)

        self.item_spawn_timer -= 1
        if self.item_spawn_timer == 0:
            self.spawn_item()
            self.item_spawn_timer = randint(5, 20)

        self.advance_time()

    def random_empty_space(self):
        """
        Returns the position of a random empty tile.

        Actions:
            - Gets all empty space positions in a list
            - If there are no empty spaces, return
            - Return a random position

        Returns:
            - boolean:
                True if there was an empty space
                False if not
            - tuple[int, int]:
                The random empty position
        """
        empty_spaces = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if isinstance(self.grid[y][x].entity, Empty)
        ]

        if not empty_spaces:
            return False, None

        return True, choice(empty_spaces)

    def spawn_entity(self, entity, position):
        """
        Spawns an entity in a specific position on the grid

        Args:
            - entity (Entity):
                The entity to spawn
            - position (tuple[int, int]):
                - The position to spawn the entity at
        """
        (x, y) = position

        self.grid[y][x].entity = entity

    def spawn_enemy(self):
        """
        Spawns a random enemy in a random position on the grid

        Actions:
            - Selects a random empty position
            - Creates an enemy at that position with the correct stats
            - Spawns the enemy
        """
        (success, position) = self.random_empty_space()
        if success:
            enemy = self.entity_factory.random_enemy(position)
            enemy.adjust_stats(self.score)

            self.spawn_entity(enemy, position)

    def spawn_item(self):
        """
        Spawns a random item in a random position on the grid

        Actions:
            - Gets the position of a random empty space
            - Creates a random item
            - Spawns the item at the position
        """
        (success, position) = self.random_empty_space()

        if success:
            item = self.entity_factory.random_item()

            self.spawn_entity(item, position)

    def handle_player_death(self):
        """
        Handles the player's death.

        Actions:
            - Sets the game_over BooleanProperty to True
        """
        self.game_over = True

    def remove_dead(self):
        """
        Removes dead creatures from the grid

        Actions:
            - Goes through each space in the grid, checking if it is a Creature
            - If it's a creature, check if it's alive
            - If it's not alive, remove it from the grid
        """
        for y in range(self.height):
            for x in range(self.width):
                entity = self.grid[y][x].entity
                if isinstance(entity, Creature):
                    if not entity.is_alive:
                        self.grid[y][x].entity = Empty()

    def advance_time(self):
        """
        Advances time.

        Actions:
            - Keeps looping until something stops it
            - If the player is dead, stop looping
            - Reset the entities who need to take their turns
            - Go through each creature in the grid
            - Update their turn meter
            - If the creature has enough turn meter charge:
                - Set the current actor to that creature
                - Make them take their turn
                - Stop advancing time
        """
        for y in range(self.height):
            for x in range(self.width):
                entity = self.grid[y][x].entity
                if isinstance(entity, Creature):
                    print(entity)
                    print(entity.turn_meter)
        while True:
            if not self.player.is_alive:
                break

            for y in range(self.height):
                for x in range(self.width):
                    entity = self.grid[y][x].entity
                    if isinstance(entity, Creature):
                        entity.turn_meter += entity.speed
                        if entity.turn_meter >= 100:
                            self.current_actor = entity
                            if isinstance(self.current_actor, Enemy):
                                self.enemy_turn()
                                return
                            elif isinstance(self.current_actor, Player):
                                return

    def attack_creature(self, attacker, creature_location):
        """
        Does an attack action

        Args:
            attacker (Entity):
                The entity that will perform the attack
            creature_loaction (tuple[int, int]):
                The location of the creature that should be attacked

        Actions:
            - Checks that the target is close enough and within the grid
            - Checks the target is not attacking itself
            - Deals damage to the creature

        - Returns:
            boolean:
                True if the creature was successfully attacked
                False if nto
        """
        (creature_x, creature_y) = creature_location
        attacker_position = attacker.position

        if (is_adjacent(attacker_position, creature_location)
                and self.in_bounds(creature_location)
                and attacker_position != creature_location):
            tile = self.grid[creature_y][creature_x]
            creature = tile.entity
            attacker.attack_creature(creature)

            return True
        else:
            return False

    def use_item(self, item_location):
        """
        Handles the player trying to use an item.

        Args:
            - item_location (tuple[int, int]):
                The location of the item the player is trying to use

        Actions:
            - Checks that the item is close enough and within the grid
            - Handles the player's stat changes from using the item
            - Removes the item from the grid

        Returns:
            - boolean:
                True if the item was successfully used
                False if not
        """
        (item_x, item_y) = item_location
        player_position = self.player.position

        if (is_adjacent(player_position, item_location)
                and self.in_bounds(item_location)):
            tile = self.grid[item_y][item_x]
            item = tile.entity
            self.power_up(item)

            tile.entity = Empty()
            return True
        else:
            return False

    def power_up(self, item):
        """
        Handles the player's stat changes from using an item.

        Args:
            - item (Item):
                The item the player is using

        Actions:
            - Updates the player's health, speed and attack damage
            - Heals the player
            - Updates the player's stat decay
            - Increases the score
            - Syncs the stats from the player
        """
        self.player.max_health += item.max_health_boost
        self.player.speed += item.speed_boost
        self.player.attack_damage += item.attack_boost

        self.player.heal(item.curr_health_boost)

        self.player.attack_damage_decay.append(item.attack_decay)
        self.player.speed_decay.append(item.speed_decay)
        self.player.max_health_decay.append(item.max_health_decay)
        self.player.decay_duration_left.append(item.decay_duration)

        self.score += item.score_boost

    def move_player(self, destination):
        """
        Moves the player to an adjacent space on the grid.

        Args:
            - destination (tuple[int, int]):
                The position the player is trying to move to.

        Actions:
            - Checks the space is close enough and inside the grid
            - Updates the player's position
            - Replaces the old position with an empty space

        Returns:
            - boolean:
                True if the player successfully moved
                False if not
        """
        player = self.player
        grid = self.grid

        (origin_x, origin_y) = origin = player.position

        (destination_x, destination_y) = destination

        if (is_adjacent(origin, destination)
                and self.in_bounds(destination)):
            grid[destination_y][destination_x].entity = player
            player.position = destination

            grid[origin_y][origin_x].entity = Empty()

            return True
        else:
            return False

    def in_bounds(self, position):
        """
        Checks that a position is within the boundaries of the grid.

        Args:
            - position (bool[int, int]):
                The position to check

        Returns:
            - boolean:
                True if it is in bounds
                False if not
        """
        (x, y) = position
        return not (x < 0 or y < 0 or x >= self.width or y >= self.height)
