class Settings:
    def __init__(self,
                 background_home="",
                 background_home_value_box="bg-gradient-green-blue",
                 vb_showcase_layout="left center"
                 ):
        self.gradients = {
            "green_blue":   "bg-gradient-green-blue",
            "blue_green":   "bg-gradient-blue-green",
            "green_purple": "bg-gradient-green-purple",
            "purple_green": "bg-gradient-purple-green",
            "green_pink":   "bg-gradient-green-pink",
            "pink_green":   "bg-gradient-pink-green",
            "green_red":    "bg-gradient-green-red",
            "red_green":    "bg-gradient-red-green",
            "green_orange": "bg-gradient-green-orange",
            "orange_green": "bg-gradient-orange-green",
            "green_yellow": "bg-gradient-green-yellow",
            "yellow_green": "bg-gradient-yellow-green",
            "green_teal":   "bg-gradient-green-teal",
            "teal_green":   "bg-gradient-teal-green",
            "green_cyan":   "bg-gradient-green-cyan",
            "cyan_green":   "bg-gradient-cyan-green",
        }

        self.background_home = background_home
        self.background_home_value_box = self.gradients["purple_green"] #background_home_value_box
        self.vb_showcase_layout = vb_showcase_layout

    def change_back_ground_home(self, new_color):
        self.background_home = new_color

    def change_back_ground_home_valuebox(self, new_color):
        if new_color not in self.gradients.values():
            raise ValueError(
                "La nouvelle couleur doit être parmis celles disponibles"
            )
        self.background_home_value_box = new_color
