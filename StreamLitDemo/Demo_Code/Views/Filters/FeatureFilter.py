class FeatureFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self, features):
        features.sort()
        features_label = self.config_parser["filters"]["features"]
        selected_merkmale = self.st_module.multiselect(
            features_label,
            features,
            default=[],
            placeholder=self.place_holder
        )
