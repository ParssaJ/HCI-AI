class ColorFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self, colors):
        colors.sort()
        colors_label = self.config_parser["filters"]["colors"]
        colors_selected = self.st_module.multiselect(
            colors_label,
            colors,
            default=[],
            placeholder=self.place_holder
        )

        if colors_selected:
            working_copy = self.st_module.session_state.working_copy
            working_copy_after_filter = [dog for dog in working_copy
                                         if dog[6] in colors_selected]
            self.st_module.session_state.working_copy = working_copy_after_filter
