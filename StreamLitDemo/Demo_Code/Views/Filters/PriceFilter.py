class PriceFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self, data):
        max_price = max([dog[2] for dog in data])
        min_price = min([dog[2] for dog in data])

        price_label = self.config_parser["filters"]["price"]
        price = self.st_module.slider(
            price_label,
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=1
        )

        if price:
            selected_min, selected_max = price
            working_copy = self.st_module.session_state.static_template_results
            working_copy_after_filter = [dog for dog in working_copy
                                         if selected_min <= dog[2] <= selected_max]
            self.st_module.session_state.static_template_results = working_copy_after_filter

            working_copy = self.st_module.session_state.llm_results
            working_copy_after_filter = [dog for dog in working_copy
                                         if selected_min <= dog[2] <= selected_max]
            self.st_module.session_state.llm_results = working_copy_after_filter

