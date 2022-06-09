from typing import List, Tuple, Type, Union

from dash import callback, Input, Output, State
from dash.development.base_component import Component
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors
from webviz_config.webviz_plugin_subclasses import (
    ViewABC,
    ViewElementABC,
    SettingsGroupABC,
)
import webviz_core_components as wcc

from ..._element_ids import ElementIds


class Graph(ViewElementABC):
    def __init__(self) -> None:
        super().__init__()

    def inner_layout(self) -> Union[str, Type[Component]]:
        return wcc.Graph(
            id=self.register_component_unique_id(ElementIds.GRAPH),
            config={"displayModeBar": True, "topojsonUrl": "localhost"},
            style={"height": "43vh", "min-height": "300px"},
        )


class BirthIndicators(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Birth indicators")

        self.df_birth_rates = population_df[
            population_df["Indicator Code"] == "SP.DYN.CBRT.IN"
        ]
        self.df_fertility_rates = population_df[
            population_df["Indicator Code"] == "SP.DYN.TFRT.IN"
        ]

        self.df_life_expectancy = population_df[
            population_df["Indicator Code"].isin(
                ["SP.DYN.LE00.IN", "SP.DYN.LE00.FE.IN", "SP.DYN.LE00.MA.IN"]
            )
        ]

        self.df_sex_ratio = population_df[
            population_df["Indicator Code"] == "SP.POP.BRTH.MF"
        ]

        column = self.add_column()

        first_row = column.make_row()
        first_row.add_view_element(
            Graph(), ElementIds.BirthDeathFertility.BirthIndicators.BIRTH_RATES
        )
        first_row.add_view_element(
            Graph(), ElementIds.BirthDeathFertility.BirthIndicators.FERTILITY_RATES
        )

        second_row = column.make_row()
        second_row.add_view_element(
            Graph(), ElementIds.BirthDeathFertility.BirthIndicators.LIFE_EXPECTANCY
        )
        second_row.add_view_element(
            Graph(), ElementIds.BirthDeathFertility.BirthIndicators.SEX_RATIO
        )

    def set_callbacks(self) -> None:
        @callback(
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.BirthIndicators.BIRTH_RATES
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.BirthIndicators.FERTILITY_RATES
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.BirthIndicators.LIFE_EXPECTANCY
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.BirthIndicators.SEX_RATIO
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Input(
                self.get_store_unique_id(ElementIds.Stores.SELECTED_COUNTRIES), "data"
            ),
            Input(self.get_store_unique_id(ElementIds.Stores.SELECTED_YEARS), "data"),
        )
        def _update_plots(
            countries: List[str], years: List[int]
        ) -> Tuple[dict, dict, dict, dict]:
            birth_rates = {
                "data": [
                    {
                        "x": list(
                            self.df_birth_rates.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_birth_rates.loc[
                                self.df_birth_rates["Country Name"] == x
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": x,
                    }
                    for x in countries
                ],
                "layout": {
                    "title": "Birth rate, crude (per 1,000 people)",
                    "xaxis": {"range": years},
                },
            }

            fertility_rates = {
                "data": [
                    {
                        "x": list(
                            self.df_fertility_rates.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_fertility_rates.loc[
                                self.df_fertility_rates["Country Name"] == x
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": x,
                    }
                    for x in countries
                ],
                "layout": {
                    "title": "Fertility rate, total (births per woman)",
                    "xaxis": {"range": years},
                },
            }

            colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            life_expectancy = {
                "data": [
                    {
                        "x": list(
                            self.df_life_expectancy.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_life_expectancy.loc[
                                self.df_life_expectancy["Country Name"] == x
                            ]
                            .loc[
                                self.df_life_expectancy["Indicator Code"]
                                == "SP.DYN.LE00.FE.IN"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, female",
                        "line": {"color": colors[i % len(colors)], "dash": "dash"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_life_expectancy.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_life_expectancy.loc[
                                self.df_life_expectancy["Country Name"] == x
                            ]
                            .loc[
                                self.df_life_expectancy["Indicator Code"]
                                == "SP.DYN.LE00.MA.IN"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, male",
                        "line": {"color": colors[i % len(colors)], "dash": "dot"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_life_expectancy.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_life_expectancy.loc[
                                self.df_life_expectancy["Country Name"] == x
                            ]
                            .loc[
                                self.df_life_expectancy["Indicator Code"]
                                == "SP.DYN.LE00.IN"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, total",
                        "line": {"color": colors[i % len(colors)]},
                    }
                    for i, x in enumerate(countries)
                ],
                "layout": {
                    "title": "Life expectancy at birth (years)",
                    "xaxis": {"range": years},
                },
            }

            sex_ratio = {
                "data": [
                    {
                        "x": list(
                            self.df_sex_ratio.dropna(axis="columns", how="all").columns[
                                4:
                            ]
                        ),
                        "y": list(
                            self.df_sex_ratio.loc[
                                self.df_sex_ratio["Country Name"] == x
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": x,
                    }
                    for x in countries
                ],
                "layout": {
                    "title": "Sex ratio at birth (male births per female births)",
                    "xaxis": {"range": years},
                },
            }

            return (birth_rates, fertility_rates, life_expectancy, sex_ratio)
