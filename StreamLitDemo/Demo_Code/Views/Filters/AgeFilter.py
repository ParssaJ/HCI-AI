class AgeFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self):
        age_label = self.config_parser["filters"]["age"]
        options = ["Welpe (bis 3 Monate)", "Junghund (bis 6 Monate)", "Subadult (bis 1 Jahr)",
                   "Jung Erwachsen (bis 3 Jahre)", "Erwachsen (ab 3 Jahre)"]
        self.st_module.session_state.age = self.st_module.multiselect(
            age_label,
            options,
            default=[],
            placeholder=self.place_holder,
        )
