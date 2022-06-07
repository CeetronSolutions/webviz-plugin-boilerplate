from typing import Type, Union

from dash import callback, Input, Output
from dash.development.base_component import Component
import pandas as pd
from webviz_config.webviz_plugin_subclasses import ViewABC, ViewElementABC
import webviz_core_components as wcc

from ..._element_ids import ElementIds
from ..._utils import create_figure

class Graph(ViewElementABC):
    def __init__(self):
        super().__init__()

    def inner_layout(self) -> Union[str, Type[Component]]:
        return wcc.Graph(
            id=self.register_component_unique_id(
                ElementIds.GRAPH
            ),
            config={"displayModeBar": False},
        )

class BirthIndicators(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Birth indicators")

        self.population_df = population_df

        self.df_birth_rates = population_df[population_df["Indicator Code"] == "SP.DYN.CBRT.IN"]
        self.df_fertility_rates = population_df[population_df["Indicator Code"] == "SP.DYN.TFRT.IN"]

        self.df_life_expectancy = population_df[population_df["Indicator Code"].isin(["SP.DYN.LE00.MA.IN", "SP.DYN.LE00.FE.IN"])]

        self.df_sex_ratio = population_df[population_df["Indicator Code"] == "SP.POP.BRTH.MF"]

        column = self.add_column()
        column.add_view_element(Graph(), ElementIds.BirthDeathFertility.BirthIndicators.BIRTH_RATES)

    def set_callbacks(self) -> None:
        @callback(
            Output(self.view_element(ElementIds.BirthDeathFertility.BirthIndicators.BIRTH_RATES).component_unique_id(ElementIds.GRAPH).to_string(), "figure"),
            Input(self.get_store_unique_id(ElementIds.Stores.SELECTED_COUNTRIES), "data")
        )
        def _adjust_plots(countries: list) -> dict:
            x_values = list(self.df_birth_rates.columns[4:])
            return {
                "data": [
                    {"x": x_values, "y": list(self.df_birth_rates.loc[self.df_birth_rates["Country Name"] == x].iloc[:, 4:].values.tolist()[0]), "type": "line", "name": x}
                for x in countries],
                "layout": {
                    "title": "Birth rate, crude (per 1,000 people)"
                }
            }
