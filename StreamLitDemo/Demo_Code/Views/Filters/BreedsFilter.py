class BreedsFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self, breeds):
        breeds.sort()
        breed_label = self.config_parser["filters"]["race"]
        selected_merkmale = self.st_module.multiselect(
            breed_label,
            breeds,
            default=[],
            placeholder=self.place_holder
        )
