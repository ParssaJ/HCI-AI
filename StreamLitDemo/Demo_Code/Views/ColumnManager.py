from .LeftColumnView import LeftColumnView
from .MiddleColumnView import MiddleColumnView
from .RightColumnView import RightColumnView
from configparser import ConfigParser


class ColumnManager:
    def __init__(self, st_module):
        self.st_module = st_module
        config_parser = ConfigParser()
        config_parser.read("../Assets/static/strings/labels.ini")
        self.left_column_view = LeftColumnView(self.st_module, config_parser)
        self.middle_column_view = MiddleColumnView(self.st_module, config_parser)
        self.right_column_view = RightColumnView(self.st_module, config_parser)

    def display_head_container(self):
        with self.st_module.container():
            col_head_left, col_head_middle, col_head_right = self.st_module.columns([0.6, 3, 1], vertical_alignment="bottom")

            self.left_column_view.display_front_image(col_head_left)
            self.middle_column_view.display_search_text_input(col_head_middle)
            self.right_column_view.display_submit_button(col_head_right)

    def display_body_container(self):
        with self.st_module.container():
            col_body_left, col_body_middle, col_body_right = self.st_module.columns([0.6, 2, 2])

            self.left_column_view.display_filters(col_body_left)
            self.middle_column_view.display_sqi_search_results_text(col_body_middle)
            self.right_column_view.display_static_template_search_results_text(col_body_right)
