from .Filters.PriceFilter import PriceFilter
from .Filters.GenderFilter import GenderFilter
from .Filters.SizeFilter import SizeFilter
from .Filters.AgeFilter import AgeFilter
from .Filters.BreedsFilter import BreedsFilter
from .Filters.FeatureFilter import FeatureFilter
from .Filters.ColorFilter import ColorFilter


class LeftColumnView:

    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser
        self.dogs_data_original = st_module.session_state.results if "results" in st_module.session_state else None
        self.price_filter = PriceFilter(st_module, configparser)
        self.gender_filter = GenderFilter(st_module, configparser)
        self.size_filter = SizeFilter(st_module, configparser)
        self.age_filter = AgeFilter(st_module, configparser)
        self.breeds_filter = BreedsFilter(st_module, configparser)
        self.feature_filter = FeatureFilter(st_module, configparser)
        self.color_filter = ColorFilter(st_module, configparser)

    def display_front_image(self, container_head):
        with container_head:
            image_path = "../Assets/static/images/front_logo.png"
            self.st_module.image(image_path, use_column_width=True)

    def display_filters(self, container_body):
        self.st_module.session_state.working_copy = self.dogs_data_original
        with container_body:
            filter_header = self.config_parser["filters"]["header"]
            self.st_module.write(filter_header)

            self.price_filter.display(self.dogs_data_original,)
            self.gender_filter.display()
            self.size_filter.display()
            self.age_filter.display()

            breeds = []
            features = []
            colors = []
            for dog in self.dogs_data_original:
                breeds.append(dog[3])
                colors.append(dog[6])
                for feature in dog[13].split(","):
                    features.append(feature)

            breeds = list(set(breeds))
            self.breeds_filter.display(breeds)

            features = list(set(features))
            self.feature_filter.display(features)

            colors = list(set(colors))
            self.color_filter.display(colors)
