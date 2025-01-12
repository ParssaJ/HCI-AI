class PriceFilter:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.place_holder = configparser["filters"]["place_holder"]

    def display(self, data):
        max_price = max([dog[2] for dog in data])
        min_price = min([dog[2] for dog in data])

        price_label = self.config_parser["filters"]["price"]
        self.st_module.session_state.price = self.st_module.slider(
            price_label,
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=1
        )
