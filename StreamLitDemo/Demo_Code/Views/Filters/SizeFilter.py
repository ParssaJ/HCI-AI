class SizeFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self):
        #options = ["Mini (bis 25cm)", "Klein (bis 40cm)", "Mittel (bis 50cm)", "Mittelgroß (bis 60cm) ",
        #          "Groß (über 60cm)"]
        options = [dog[12] for dog in self.st_module.session_state.working_copy]
        size_label = self.config_parser["filters"]["size"]
        size = self.st_module.multiselect(
            size_label,
            options,
            default=[],
            placeholder=self.place_holder,
        )

        if size:
            working_copy = self.st_module.session_state.static_template_results
            working_copy_after_filter = [dog for dog in working_copy
                                         if dog[12] in size]
            self.st_module.session_state.static_template_results = working_copy_after_filter

            working_copy = self.st_module.session_state.llm_results
            working_copy_after_filter = [dog for dog in working_copy
                                         if dog[12] in size]
            self.st_module.session_state.llm_results = working_copy_after_filter
