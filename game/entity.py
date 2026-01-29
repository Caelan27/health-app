class Entity:
    def __init__(self, start_coordinates):
        self.coordinates = start_coordinates

    def go_to(self, destination_coordinates):
        self.coordinates = destination_coordinates

    def can_walk_to(self, destination_coordinates):
        (current_x, current_y) = self.coordinates
        (destination_x, destination_y) = destination_coordinates

        change_in_x = abs(destination_x - current_x)
        change_in_y = abs(destination_y - current_y)

        if change_in_y <= 1 and change_in_x <= 1:
            return True
        else:
            return False


class Player(Entity):
    def __init__(self, start_coordinates):
        super().__init__(start_coordinates)
        self.background_unpressed = self.default_image_unpressed = "images/player.png"
        self.background_pressed = self.default_image_unpressed = "images/player.png"

    def travel_to(self, destination_coordinates):
        if self.can_walk_to(destination_coordinates):
            self.go_to(destination_coordinates)
            return True
        else:
            return False


class Empty(Entity):
    def __init__(self, start_coordinates):
        super().__init__(start_coordinates)
        self.background_unpressed = self.default_image_unpressed = "atlas://data/images/defaulttheme/button"
        self.background_pressed = self.default_image_unpressed = "atlas://data/images/defaulttheme/button_pressed"
