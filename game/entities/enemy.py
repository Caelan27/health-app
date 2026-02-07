from game.entities.creature import Creature
from game.helpers import is_adjacent, sign


class Enemy(Creature):
    """
    A Creature representing an enemy

    Attributes:
        - position (tuple[int, int]):
            The creature's current position.
    """

    def __init__(self, position, **kwargs):
        """
        Initialises the enemy.

        Args:
            - position (tuple[int, int]):
                The enemy's position
            - **kwargs:
                Keyword arguments for the parent Creature class
        """
        super().__init__(**kwargs)
        self.position = position

    def move_towards_player(self, game_state):
        """
        Calculates where to move towards the player.

        Args:
            - game_state (GameState):
                The current game state

        Actions:
            - Calculates the position to move to towards the player
            - Moves to that position
        """
        (player_x, player_y) = game_state.player.position
        (self_x, self_y) = self.position

        # Calculates the distance to the player in the x and y directions
        dx_to_player = player_x - self_x
        dy_to_player = player_y - self_y

        # Calculates one space in the right x and y directions
        # If they have the same x or y coordinate, it will be 0
        dx_to_destination = sign(dx_to_player)
        dy_to_destination = sign(dy_to_player)

        # Calculates the final destination towards the player
        destination_x = self_x + dx_to_destination
        destination_y = self_y + dy_to_destination
        destination = (destination_x, destination_y)

        return game_state.move_creature(self, destination)

    def take_turn(self, game_state):
        """
        Performs the enemy's turn.

        Args:
            - game_state (GameState):
                The current game state

        Actions:
            - If the player is close enough, attack the player
            - If not, try to move towards the player
        """
        if is_adjacent(self.position, game_state.player.position):
            self.attack_creature(game_state.player)
        else:
            self.move_towards_player(game_state)

    def adjust_stats(self, score):
        """
        Adjusts the enemy's stats based on the player's score

        Args:
            - score (int):
                The player's score

        Actions:
            - Adjusts all of the stats using the following formula:
                new_stat = base_stat + scale * score

        """
        self.max_health = round(self.base_health + self.health_scale * score)
        self.curr_health = self.max_health
        self.speed = round(self.base_speed + self.speed_scale * score)
        self.attack_damage = round(
            self.base_attack + self.attack_scale * score)
