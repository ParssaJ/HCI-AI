class MiddleColumnView:

    def __init__(self, st_module, configparser):
        self.st_module = st_module
        self.config_parser = configparser

    def display_search_text_input(self, container_head):
        with container_head:
            label = self.config_parser["search_input"]["label"]
            placeholder = self.config_parser["search_input"]["placeholder"]
            self.st_module.session_state.search_input = self.st_module.text_input(
                label=label,
                placeholder=placeholder,
            )

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
                 size,
                 features) in results:

                html_code = """
                        <style>
                            img {
                                border-radius: 5%;
                            }
                            button[data-testid="StyledFullScreenButton"] {
                                visibility: hidden;
                            }
                            div[data-testid="InputInstructions"] {
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
                self.st_module.write(f"**Alter:** {age // 4} Monate")
                self.st_module.write(f"**Farbe:** {color}")
                self.st_module.write(f"**Preis**: {price} €")
                self.st_module.write(f"**Größe**: {size}")
                self.st_module.write(f"**Herkunft**: {birth_country}")

    def display_sqi_search_results_text(self, container_body):
        with container_body:
            header = self.config_parser["search_results"]["left_ai_header"]
            self.st_module.header(header, divider="gray")

            results = self.st_module.session_state.llm_results if "llm_results" in self.st_module.session_state else self.st_module.session_state.default_results

            if results:
                left_results = self.st_module.session_state.llm_results[0::2]
                right_results = self.st_module.session_state.llm_results[1::2]
                left_col, right_col = self.st_module.columns(2)

                self._display_images(left_col, left_results)
                self._display_images(right_col, right_results)
