class GenderFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self):
        options = ['Rüde', 'Hüdin']
        gender_label = self.config_parser["filters"]["gender"]
        gender = self.st_module.multiselect(
            gender_label,
            options,
            default=[],
            placeholder=self.place_holder,
        )

        if gender:
            working_copy = self.st_module.session_state.working_copy
            working_copy_after_filter = [dog for dog in working_copy
                                         if dog[4] in gender]
            self.st_module.session_state.working_copy = working_copy_after_filter


