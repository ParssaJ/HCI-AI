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

        if selected_merkmale:
            working_copy = self.st_module.session_state.static_template_results
            working_copy_after_filter = [dog for dog in working_copy
                                         if dog[3] in selected_merkmale]
            self.st_module.session_state.static_template_results = working_copy_after_filter

            working_copy = self.st_module.session_state.llm_results
            working_copy_after_filter = [dog for dog in working_copy
                                         if dog[3] in selected_merkmale]
            self.st_module.session_state.llm_results = working_copy_after_filter
