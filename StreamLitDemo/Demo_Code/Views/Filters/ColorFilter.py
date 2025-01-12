class ColorFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self, colors):
        colors.sort()
        colors_label = self.config_parser["filters"]["colors"]
        selected_merkmale = self.st_module.multiselect(
            colors_label,
            colors,
            default=[],
            placeholder=self.place_holder
        )
