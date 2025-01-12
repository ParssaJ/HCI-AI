class SizeFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self):
        options = ["Mini (bis 25cm)", "Klein (bis 40cm)", "Mittel (bis 50cm)", "Mittelgroß (bis 60cm) ",
                   "Groß (über 60cm)"]
        size_label = self.config_parser["filters"]["size"]
        self.st_module.session_state.size = self.st_module.multiselect(
            size_label,
            options,
            default=[],
            placeholder=self.place_holder,
        )
