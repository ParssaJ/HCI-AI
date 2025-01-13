class AgeFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self):
        age_label = self.config_parser["filters"]["age"]
        max_weeks = max([dog[5] // 4 for dog in self.st_module.session_state.working_copy])
        min_weeks = min([dog[5] // 4 for dog in self.st_module.session_state.working_copy])

        age = self.st_module.slider(
            age_label,
            min_value=min_weeks,
            max_value=max_weeks,
            value=(min_weeks, max_weeks),
            step=1
        )

        if age:
            selected_min_weeks, selected_max_weeks = age
            working_copy = self.st_module.session_state.working_copy
            working_copy_after_filter = [dog for dog in working_copy
                                         if selected_min_weeks <=
                                         dog[5] // 4
                                         <= selected_max_weeks]
            self.st_module.session_state.working_copy = working_copy_after_filter
