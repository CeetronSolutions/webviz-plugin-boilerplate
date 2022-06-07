from typing import List, Type

from dash import callback, Input, Output
from dash.development.base_component import Component
import pandas as pd
from webviz_config.webviz_plugin_subclasses import SettingsGroupABC
import webviz_core_components as wcc

from .._element_ids import ElementIds

class CountrySelection(SettingsGroupABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Countries")

        self.countries = population_df.drop_duplicates(subset=["Country Name"])["Country Name"].to_list()

    def layout(self) -> List[Component]:
        return wcc.Select(
            id=self.register_component_unique_id(ElementIds.SharedSettings.CountrySelection.SELECTOR_COMPONENT), 
            options=[{"label": i, "value": i} for i in self.countries],
            value=self.countries,
            multi=True,
            size=min(15, len(self.countries)),
        )

    def set_callbacks(self) -> None:
        @callback(
            Output(self.get_store_unique_id(ElementIds.Stores.SELECTED_COUNTRIES), "data"),
            Input(self.component_unique_id(ElementIds.SharedSettings.CountrySelection.SELECTOR_COMPONENT).to_string(), "value")
        )
        def _set_countries(countries: List[str]) -> List[str]:
            return countries

