from game.core.tile import Tile
from game.entities.empty import Empty
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.items import Food
from game.entities.items import HealthyFood
from game.entities.creature import Creature
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from random import randint


class GameState(EventDispatcher):
    player_health = NumericProperty(10)
    game_over = BooleanProperty(False)

    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.grid = []
        self.player = Player((0, 0))
        self.current_actor = None

        self.enemy_spawn_timer = randint(5, 20)
        self.food_spawn_timer = randint(5, 20)

    def initialise_grid(self):
        for y in range(self.height):
            self.grid.append([])
            for x in range(self.width):
                self.grid[y].append(Tile(Empty()))

        (food_x, food_y) = (randint(0, 4), randint(0, 4))
        while (food_x, food_y) == (0, 0):
            (food_x, food_y) = (randint(0, 4), randint(0, 4))
        self.grid[food_y][food_x].entity = HealthyFood()

        (enemy_x, enemy_y) = (randint(0, 4), randint(0, 4))
        while ((enemy_x, enemy_y) == (0, 0)
               or (enemy_x, enemy_y) == (food_x, food_y)):
            (enemy_x, enemy_y) = (randint(0, 4), randint(0, 4))
        self.grid[enemy_y][enemy_x].entity = Enemy((enemy_x, enemy_y))

        (player_x, player_y) = self.player.position
        self.grid[player_y][player_x].entity = self.player

        self.player.curr_health = self.player_health
        self.player.on_health_changed = self._sync_health_from_player

        self.advance_time()

    def move_creature(self, creature, destination):
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

    def _sync_health_from_player(self):
        self.player_health = self.player.curr_health

    def interact_with_tile(self, tile_location):
        (tile_x, tile_y) = tile_location
        tile = self.grid[tile_y][tile_x]
        entity = tile.entity

        did_something = False
        if isinstance(entity, Empty):
            did_something = self.move_player(tile_location)
        elif isinstance(entity, Food):
            did_something = self.eat_food(tile_location)
        elif isinstance(entity, Creature):
            did_something = self.attack_creature(self.player, tile_location)

        if did_something:
            print("Player taking turn")
            self.end_turn()

    def enemy_turn(self):
        if self.current_actor is None:
            return
        self.current_actor.take_turn(self.player, self)
        # self.attack_creature(self.current_actor, self.player.position)
        self.end_turn()

    def end_turn(self):
        print(self.player_health, self.player.curr_health)
        actor = self.current_actor
        if actor is not None:
            actor.turn_meter -= 10
        self.current_actor = None
        if not self.player.is_alive:
            self.handle_player_death()
        self.remove_dead()

        print(self.enemy_spawn_timer)
        self.enemy_spawn_timer -= 1
        if self.enemy_spawn_timer == 0:
            self.spawn_enemy()
            self.enemy_spawn_timer = randint(5, 20)

        print(self.enemy_spawn_timer)
        self.food_spawn_timer -= 1
        if self.food_spawn_timer == 0:
            self.spawn_food()
            self.food_spawn_timer = randint(5, 20)

        self.advance_time()

    def spawn_enemy(self):
        spawned = False
        while not spawned:
            (enemy_x, enemy_y) = (randint(0, 4), randint(0, 4))
            entity = self.grid[enemy_y][enemy_x].entity
            if isinstance(entity, Empty):
                self.grid[enemy_y][enemy_x].entity = Enemy((enemy_x, enemy_y))
                spawned = True

    def spawn_food(self):
        spawned = False
        while not spawned:
            (food_x, food_y) = (randint(0, 4), randint(0, 4))
            entity = self.grid[food_y][food_x].entity
            if isinstance(entity, Empty):
                self.grid[food_y][food_x].entity = Food()
                spawned = True

    def handle_player_death(self):
        self.game_over = True

    def refresh_grid(self):
        self.remove_dead()

    def remove_dead(self):
        for y in range(self.height):
            for x in range(self.width):
                entity = self.grid[y][x].entity
                if isinstance(entity, Creature):
                    if not entity.is_alive:
                        self.grid[y][x].entity = Empty()

    def advance_time(self):
        for y in range(self.height):
            for x in range(self.width):
                entity = self.grid[y][x].entity
                if isinstance(entity, Creature):
                    entity.turn_meter += entity.speed
                    if entity.turn_meter >= 10:
                        self.current_actor = entity
                        if isinstance(entity, Enemy):
                            self.enemy_turn()
                        return

    def attack_creature(self, attacker, creature_location):
        (creature_x, creature_y) = creature_location
        attacker_position = attacker.position

        if (self.is_adjacent(attacker_position, creature_location)
                and self.in_bounds(creature_location)
                and attacker_position != creature_location):
            tile = self.grid[creature_y][creature_x]
            creature = tile.entity
            attacker.deal_damage(creature)

            return True

    def eat_food(self, food_location):
        (food_x, food_y) = food_location
        player_position = self.player.position

        if (self.is_adjacent(player_position, food_location)
                and self.in_bounds(food_location)):
            tile = self.grid[food_y][food_x]
            food = tile.entity
            self.power_up(food)

            tile.entity = Empty()
            return True

    def power_up(self, food):
        print("Yay (: Eating food...")
        self.player.heal(2)

    def move_player(self, destination):
        player = self.player
        grid = self.grid

        (origin_x, origin_y) = origin = player.position

        (destination_x, destination_y) = destination

        if (self.is_adjacent(origin, destination)
                and self.in_bounds(destination)):
            grid[destination_y][destination_x].entity = player
            player.position = destination

            grid[origin_y][origin_x].entity = Empty()

            return True
        else:
            return False

    def in_bounds(self, position):
        (x, y) = position
        return not (x < 0 or y < 0 or x >= self.width or y >= self.height)

    def is_adjacent(self, a, b):
        (ax, ay) = a
        (bx, by) = b
        dx = abs(bx - ax)
        dy = abs(by - ay)

        return dx <= 1 and dy <= 1
