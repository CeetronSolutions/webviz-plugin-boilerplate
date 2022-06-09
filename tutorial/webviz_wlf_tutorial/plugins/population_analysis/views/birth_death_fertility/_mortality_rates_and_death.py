from typing import List, Tuple, Type, Union

from dash import callback, Input, Output
from dash.development.base_component import Component
import pandas as pd
import plotly.colors
from webviz_config.webviz_plugin_subclasses import ViewABC, ViewElementABC
import webviz_core_components as wcc

from ..._element_ids import ElementIds
from ..._utils import create_figure


class Graph(ViewElementABC):
    def __init__(self) -> None:
        super().__init__()

    def inner_layout(self) -> Union[str, Type[Component]]:
        return wcc.Graph(
            id=self.register_component_unique_id(ElementIds.GRAPH),
            config={"displayModeBar": False},
            style={"height": "43vh", "min-height": "300px"},
        )


class MortalityRatesAndNumberOfDeaths(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Mortality rates and number of deaths")

        self.df_death_rates = population_df[
            population_df["Indicator Code"] == "SP.DYN.CDRT.IN"
        ]

        self.df_mortality_rates_adults = population_df[
            population_df["Indicator Code"].isin(["SP.DYN.AMRT.FE", "SP.DYN.AMRT.MA"])
        ]

        self.df_mortality_rates_infants = population_df[
            population_df["Indicator Code"].isin(
                ["SP.DYN.IMRT.IN", "SP.DYN.IMRT.FE.IN", "SP.DYN.IMRT.MA.IN"]
            )
        ]

        self.df_mortality_rates_neonatal = population_df[
            population_df["Indicator Code"] == "SH.DYN.NMRT"
        ]

        self.df_mortality_rates_under_five_years = population_df[
            population_df["Indicator Code"].isin(
                ["SH.DYN.MORT", "SH.DYN.MORT.FE", "SH.DYN.MORT.MA"]
            )
        ]

        column = self.add_column()

        column.add_view_element(
            Graph(),
            ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.DEATH_RATE,
        )

        first_row = column.make_row()
        first_row.add_view_element(
            Graph(),
            ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_ADULTS,
        )
        first_row.add_view_element(
            Graph(),
            ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_INFANTS,
        )

        second_row = column.make_row()
        second_row.add_view_element(
            Graph(),
            ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_NEONATAL,
        )
        second_row.add_view_element(
            Graph(),
            ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_UNDER_FIVE,
        )

    def set_callbacks(self) -> None:
        @callback(
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.DEATH_RATE
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_ADULTS
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_INFANTS
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_NEONATAL
                )
                .component_unique_id(ElementIds.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    ElementIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.MORTALITY_RATE_UNDER_FIVE
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
        ) -> Tuple[dict, dict, dict, dict, dict]:
            death_rates = {
                "data": [
                    {
                        "x": list(
                            self.df_death_rates.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_death_rates.loc[
                                self.df_death_rates["Country Name"] == x
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
                    "title": "Death rate, crude (per 1,000 people)",
                    "xaxis": {"range": years},
                },
            }

            colors = plotly.colors.DEFAULT_PLOTLY_COLORS

            mortality_rates_adults = {
                "data": [
                    {
                        "x": list(
                            self.df_mortality_rates_adults.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_adults.loc[
                                self.df_mortality_rates_adults["Country Name"] == x
                            ]
                            .loc[
                                self.df_mortality_rates_adults["Indicator Code"]
                                == "SP.DYN.AMRT.FE"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, female",
                        "line": {"color": colors[i % len(colors)], "dash": "dot"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_mortality_rates_adults.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_adults.loc[
                                self.df_mortality_rates_adults["Country Name"] == x
                            ]
                            .loc[
                                self.df_mortality_rates_adults["Indicator Code"]
                                == "SP.DYN.AMRT.MA"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, male",
                        "line": {"color": colors[i % len(colors)], "dash": "dash"},
                    }
                    for i, x in enumerate(countries)
                ],
                "layout": {
                    "title": "Mortality rate, adult (per 1,000 people of respective sex)",
                    "xaxis": {"range": years},
                },
            }

            mortality_rates_infants = {
                "data": [
                    {
                        "x": list(
                            self.df_mortality_rates_infants.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_infants.loc[
                                self.df_mortality_rates_infants["Country Name"] == x
                            ]
                            .loc[
                                self.df_mortality_rates_infants["Indicator Code"]
                                == "SP.DYN.IMRT.FE.IN"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, female",
                        "line": {"color": colors[i % len(colors)], "dash": "dot"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_mortality_rates_infants.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_infants.loc[
                                self.df_mortality_rates_infants["Country Name"] == x
                            ]
                            .loc[
                                self.df_mortality_rates_infants["Indicator Code"]
                                == "SP.DYN.IMRT.MA.IN"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, male",
                        "line": {"color": colors[i % len(colors)], "dash": "dash"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_mortality_rates_infants.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_infants.loc[
                                self.df_mortality_rates_infants["Country Name"] == x
                            ]
                            .loc[
                                self.df_mortality_rates_infants["Indicator Code"]
                                == "SP.DYN.IMRT.IN"
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
                    "title": "Mortality rate, infant (per 1,000 live births)",
                    "xaxis": {"range": years},
                },
            }

            mortality_rates_neonatal = {
                "data": [
                    {
                        "x": list(
                            self.df_mortality_rates_neonatal.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_neonatal.loc[
                                self.df_mortality_rates_neonatal["Country Name"] == x
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}",
                    }
                    for i, x in enumerate(countries)
                ],
                "layout": {
                    "title": "Mortality rate, neonatal (per 1,000 live births)",
                    "xaxis": {"range": years},
                },
            }

            mortality_rates_under_five = {
                "data": [
                    {
                        "x": list(
                            self.df_mortality_rates_under_five_years.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_under_five_years.loc[
                                self.df_mortality_rates_under_five_years["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_mortality_rates_under_five_years[
                                    "Indicator Code"
                                ]
                                == "SH.DYN.MORT.FE"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, female",
                        "line": {"color": colors[i % len(colors)], "dash": "dot"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_mortality_rates_under_five_years.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_under_five_years.loc[
                                self.df_mortality_rates_under_five_years["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_mortality_rates_under_five_years[
                                    "Indicator Code"
                                ]
                                == "SH.DYN.MORT.MA"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, male",
                        "line": {"color": colors[i % len(colors)], "dash": "dash"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_mortality_rates_under_five_years.dropna(
                                axis="columns", how="all"
                            ).columns[4:]
                        ),
                        "y": list(
                            self.df_mortality_rates_under_five_years.loc[
                                self.df_mortality_rates_under_five_years["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_mortality_rates_under_five_years[
                                    "Indicator Code"
                                ]
                                == "SH.DYN.MORT"
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
                    "title": "Mortality rate, infant (per 1,000 live births)",
                    "xaxis": {"range": years},
                },
            }

            return (
                death_rates,
                mortality_rates_adults,
                mortality_rates_infants,
                mortality_rates_neonatal,
                mortality_rates_under_five,
            )
