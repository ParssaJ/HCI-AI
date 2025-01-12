class RightColumnView:
    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser

    def display_submit_button(self, container_head):
        with container_head:
            search_button = self.st_module.button(label="Submit", type="primary")

    def _display_images(self, column, results):
        with column:
            for (index,
                 category,
                 price,
                 breed,
                 gender,
                 age,
                 color,
                 birth_country,
                 description,
                 image_path,
                 website,
                 image_link,
                 age,
                 features) in results:
                html_code = """
                            <style>
                                img {
                                    border-radius: 5%;
                                }
                                button[data-testid="StyledFullScreenButton"] {
                                    visibility: hidden;
                                }
                            </style>
                            """
                self.st_module.write(html_code, unsafe_allow_html=True)
                self.st_module.image(image_path)

                with self.st_module.popover("Beschreibung durchlesen"):
                    self.st_module.write(description)
                    self.st_module.write("**Merkmale**:")
                    self.st_module.write(features)
                self.st_module.write(f"**Rasse:** {breed}")
                self.st_module.write(f"**Geschlecht:** {gender}")
                self.st_module.write(f"**Alter:** {age}")
                self.st_module.write(f"**Farbe:** {color}")
                self.st_module.write(f"**Preis**: {price} €")


    def display_static_template_search_results_text(self, container_body):
            header = self.config_parser["search_results"]["right_ai_header"]
            with container_body:
                self.st_module.header(header, divider="gray")

                results = self.st_module.session_state.results if "results" in self.st_module.session_state else ""
                if results:
                    left_results = results[0::2]
                    right_results = results[1::2]
                    left_col, right_col = self.st_module.columns(2, gap="large")

                    self._display_images(left_col, left_results)
                    self._display_images(right_col, right_results)
