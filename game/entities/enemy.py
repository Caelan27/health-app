from game.entities.creature import Creature


class Enemy(Creature):
    def __init__(self, position):
        super().__init__(10, 10, 1, 4)
        self.position = position
        self.sprite_name = "enemy"

    def move_towards_player(self, player, game_state):
        (player_x, player_y) = player.position
        (self_x, self_y) = self.position

        dx_to_player = player_x - self_x
        dy_to_player = player_y - self_y

        dx_to_destination = sign(dx_to_player)
        dy_to_destination = sign(dy_to_player)

        destination_x = self_x + dx_to_destination
        destination_y = self_y + dy_to_destination
        destination = (destination_x, destination_y)

        return game_state.move_creature(self, destination)

    def handle_death(self):
        super().handle_death()

    def attack_creature(self, creature):
        (creature_x, creature_y) = creature.position

        if (self.is_adjacent(creature.position)
                and self.position != creature.position):
            self.deal_damage(creature)

            return True
        else:
            return False

    def take_turn(self, player, game_state):
        print("Enemy taking turn")

        successful = False

        while not successful:
            if self.is_adjacent(player.position):
                successful = self.attack_creature(player)
            else:
                self.move_towards_player(player, game_state)
                successful = True

    def is_adjacent(self, location):
        (ax, ay) = self.position
        (bx, by) = location
        dx = abs(bx - ax)
        dy = abs(by - ay)

        return dx <= 1 and dy <= 1


def sign(number):
    return (number > 0) - (number < 0)
