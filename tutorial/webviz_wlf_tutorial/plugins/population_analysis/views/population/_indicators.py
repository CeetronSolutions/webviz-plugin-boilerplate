import pandas as pd
from webviz_config.webviz_plugin_subclasses import ViewABC

class PopulationIndicators(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Population indicators")

        self.population_df = population_df
