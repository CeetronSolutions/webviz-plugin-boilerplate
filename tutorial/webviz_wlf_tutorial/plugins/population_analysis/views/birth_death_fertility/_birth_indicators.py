import pandas as pd
from webviz_config.webviz_plugin_subclasses import ViewABC

class BirthIndicators(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Birth indicators")

        self.population_df = population_df
