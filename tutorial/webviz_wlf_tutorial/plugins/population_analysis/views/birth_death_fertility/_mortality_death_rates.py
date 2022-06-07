import pandas as pd
from webviz_config.webviz_plugin_subclasses import ViewABC

class MortalityDeathRates(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Mortality and death rates")

        self.population_df = population_df
