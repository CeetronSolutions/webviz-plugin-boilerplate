from typing import List

from dash import callback, Input, Output
from dash.development.base_component import Component
import pandas as pd
from webviz_config.webviz_plugin_subclasses import SettingsGroupABC
import webviz_core_components as wcc

from .._plugin_ids import PluginIds


class Filter(SettingsGroupABC):
    class Ids:
        COUNTRY_SELECT = "country-select"
        YEAR_SLIDER = "year-slider"

    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Filter")

        self.countries = population_df.drop_duplicates(subset=["Country Name"])[
            "Country Name"
        ].to_list()

        self.years = population_df.iloc[:, 4:].columns.to_list()

    def layout(self) -> List[Component]:
        return [
            wcc.SelectWithLabel(
                id=self.register_component_unique_id(Filter.Ids.COUNTRY_SELECT),
                label="Countries",
                options=[{"label": i, "value": i} for i in self.countries],
                value=[self.countries[0]],
                multi=True,
                size=min(15, len(self.countries)),
            ),
            wcc.RangeSlider(
                id=self.register_component_unique_id(Filter.Ids.YEAR_SLIDER),
                label="Years",
                marks={y: int(y) for y in self.years[::25]},
                min=int(self.years[0]),
                max=int(self.years[-1]),
                step=1,
                value=[int(self.years[0]), int(self.years[-1])],
                tooltip=True,
                updatemode="drag",
            ),
        ]

    def set_callbacks(self) -> None:
        @callback(
            Output(
                self.get_store_unique_id(PluginIds.Stores.SELECTED_COUNTRIES), "data"
            ),
            Input(
                self.component_unique_id(Filter.Ids.COUNTRY_SELECT).to_string(),
                "value",
            ),
        )
        def _set_countries(countries: List[str]) -> List[str]:
            return countries

        @callback(
            Output(self.get_store_unique_id(PluginIds.Stores.SELECTED_YEARS), "data"),
            Input(
                self.component_unique_id(Filter.Ids.YEAR_SLIDER).to_string(),
                "value",
            ),
        )
        def _set_years(years: List[int]) -> List[int]:
            return years
