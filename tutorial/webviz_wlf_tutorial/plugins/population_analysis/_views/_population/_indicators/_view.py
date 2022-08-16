from typing import List, Tuple

from dash import callback, Input, Output
import pandas as pd
import plotly.colors
from webviz_config.webviz_plugin_subclasses import ViewABC

from ...._plugin_ids import PluginIds
from ...._shared_view_elements._graph import Graph
from ._settings import ViewSettings


class PopulationIndicators(ViewABC):
    class Ids:
        POPULATION = "population-absolute"
        POPULATION_GROWTH = "population-growth"
        RURAL_URBAN_POPULATION = "rural-urban-population-relative"
        RURAL_URBAN_POPULATION_GROWTH = "rural-urban-population-growth"
        SETTINGS = "settings"

    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Population indicators")

        self.df_population_growth = population_df[
            population_df["Indicator Code"] == "SP.POP.GROW"
        ]

        self.df_population_absolute = population_df[
            population_df["Indicator Code"].isin(
                ["SP.POP.TOTL", "SP.POP.TOTL.FE.IN", "SP.POP.TOTL.MA.IN"]
            )
        ]

        self.df_population_relative = population_df[
            population_df["Indicator Code"].isin(
                ["SP.POP.TOTL.FE.ZS", "SP.POP.TOTL.MA.ZS"]
            )
        ]

        self.df_rural_urban_population_absolute = population_df[
            population_df["Indicator Code"].isin(["SP.RUR.TOTL", "SP.URB.TOTL"])
        ]

        self.df_rural_urban_population_relative = population_df[
            population_df["Indicator Code"].isin(
                ["SP.RUR.TOTL.ZS", "SP.URB.TOTL.IN.ZS"]
            )
        ]

        self.df_rural_urban_population_growth = population_df[
            population_df["Indicator Code"].isin(["SP.RUR.TOTL.ZG", "SP.URB.GROW"])
        ]

        self.add_settings_group(ViewSettings(), PopulationIndicators.Ids.SETTINGS)

        column = self.add_column()

        first_row = column.make_row()
        first_row.add_view_element(Graph(), PopulationIndicators.Ids.POPULATION)
        first_row.add_view_element(Graph(), PopulationIndicators.Ids.POPULATION_GROWTH)

        second_row = column.make_row()
        second_row.add_view_element(
            Graph(), PopulationIndicators.Ids.RURAL_URBAN_POPULATION
        )
        second_row.add_view_element(
            Graph(), PopulationIndicators.Ids.RURAL_URBAN_POPULATION_GROWTH
        )

    def set_callbacks(self) -> None:
        @callback(
            Output(
                self.view_element(PopulationIndicators.Ids.POPULATION)
                .component_unique_id(Graph.Ids.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(PopulationIndicators.Ids.POPULATION_GROWTH)
                .component_unique_id(Graph.Ids.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(PopulationIndicators.Ids.RURAL_URBAN_POPULATION)
                .component_unique_id(Graph.Ids.GRAPH)
                .to_string(),
                "figure",
            ),
            Output(
                self.view_element(
                    PopulationIndicators.Ids.RURAL_URBAN_POPULATION_GROWTH
                )
                .component_unique_id(Graph.Ids.GRAPH)
                .to_string(),
                "figure",
            ),
            Input(
                self.get_store_unique_id(PluginIds.Stores.SELECTED_COUNTRIES), "data"
            ),
            Input(self.get_store_unique_id(PluginIds.Stores.SELECTED_YEARS), "data"),
            Input(
                self.settings_group(PopulationIndicators.Ids.SETTINGS)
                .component_unique_id(ViewSettings.Ids.VALUES)
                .to_string(),
                "value",
            ),
        )
        def _update_plots(
            countries: List[str], years: List[int], abs_rel_values: str
        ) -> Tuple[dict, dict, dict, dict]:
            colors = plotly.colors.DEFAULT_PLOTLY_COLORS

            df_population = (
                self.df_population_absolute
                if abs_rel_values == "absolute"
                else self.df_population_relative
            )
            title = (
                "Population"
                if abs_rel_values == "absolute"
                else "Population (% of total population)"
            )
            population = {
                "data": (
                    [
                        {
                            "x": list(
                                df_population.loc[df_population["Country Name"] == x]
                                .loc[df_population["Indicator Code"] == "SP.POP.TOTL"]
                                .dropna(axis="columns", how="all")
                                .columns[4:]
                            ),
                            "y": list(
                                df_population.loc[df_population["Country Name"] == x]
                                .loc[df_population["Indicator Code"] == "SP.POP.TOTL"]
                                .iloc[:, 4:]
                                .dropna(axis="columns", how="all")
                                .values.tolist()[0]
                            ),
                            "type": "line",
                            "name": f"{x}, total",
                            "line": {"color": colors[i % len(colors)]},
                        }
                        for i, x in enumerate(countries)
                    ]
                    if abs_rel_values == "absolute"
                    else []
                )
                + [
                    {
                        "x": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[
                                df_population["Indicator Code"]
                                == (
                                    "SP.POP.TOTL.FE.IN"
                                    if abs_rel_values == "absolute"
                                    else "SP.POP.TOTL.FE.ZS"
                                )
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[
                                df_population["Indicator Code"]
                                == (
                                    "SP.POP.TOTL.FE.IN"
                                    if abs_rel_values == "absolute"
                                    else "SP.POP.TOTL.FE.ZS"
                                )
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
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[
                                df_population["Indicator Code"]
                                == (
                                    "SP.POP.TOTL.MA.IN"
                                    if abs_rel_values == "absolute"
                                    else "SP.POP.TOTL.MA.ZS"
                                )
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_population.loc[df_population["Country Name"] == x]
                            .loc[
                                df_population["Indicator Code"]
                                == (
                                    "SP.POP.TOTL.MA.IN"
                                    if abs_rel_values == "absolute"
                                    else "SP.POP.TOTL.MA.ZS"
                                )
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
                ],
                "layout": {
                    "title": title,
                    "xaxis": {"range": years},
                },
            }

            population_growth = {
                "data": [
                    {
                        "x": list(
                            self.df_population_growth.loc[
                                self.df_population_growth["Country Name"] == x
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            self.df_population_growth.loc[
                                self.df_population_growth["Country Name"] == x
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
                    "title": "Population growth (annual %)",
                    "xaxis": {"range": years},
                },
            }

            df_rural_urban_population = (
                self.df_rural_urban_population_absolute
                if abs_rel_values == "absolute"
                else self.df_rural_urban_population_relative
            )
            title = f"Rural vs urban population{'' if abs_rel_values == 'absolute' else ' (% of total population)'}"
            rural_urban_population = {
                "data": [
                    {
                        "x": list(
                            df_rural_urban_population.loc[
                                df_rural_urban_population["Country Name"] == x
                            ]
                            .loc[
                                df_rural_urban_population["Indicator Code"]
                                == (
                                    "SP.RUR.TOTL"
                                    if abs_rel_values == "absolute"
                                    else "SP.RUR.TOTL.ZS"
                                )
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_rural_urban_population.loc[
                                df_rural_urban_population["Country Name"] == x
                            ]
                            .loc[
                                df_rural_urban_population["Indicator Code"]
                                == (
                                    "SP.RUR.TOTL"
                                    if abs_rel_values == "absolute"
                                    else "SP.RUR.TOTL.ZS"
                                )
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, rural",
                        "line": {"color": colors[i % len(colors)], "dash": "dash"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            df_rural_urban_population.loc[
                                df_rural_urban_population["Country Name"] == x
                            ]
                            .loc[
                                df_rural_urban_population["Indicator Code"]
                                == (
                                    "SP.URB.TOTL"
                                    if abs_rel_values == "absolute"
                                    else "SP.URB.TOTL.IN.ZS"
                                )
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            df_rural_urban_population.loc[
                                df_rural_urban_population["Country Name"] == x
                            ]
                            .loc[
                                df_rural_urban_population["Indicator Code"]
                                == (
                                    "SP.URB.TOTL"
                                    if abs_rel_values == "absolute"
                                    else "SP.URB.TOTL.IN.ZS"
                                )
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, urban",
                        "line": {"color": colors[i % len(colors)], "dash": "dot"},
                    }
                    for i, x in enumerate(countries)
                ],
                "layout": {
                    "title": title,
                    "xaxis": {"range": years},
                },
            }

            rural_urban_population_growth = {
                "data": [
                    {
                        "x": list(
                            self.df_rural_urban_population_growth.loc[
                                self.df_rural_urban_population_growth["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_rural_urban_population_growth["Indicator Code"]
                                == "SP.RUR.TOTL.ZG"
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            self.df_rural_urban_population_growth.loc[
                                self.df_rural_urban_population_growth["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_rural_urban_population_growth["Indicator Code"]
                                == "SP.RUR.TOTL.ZG"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, rural",
                        "line": {"color": colors[i % len(colors)], "dash": "dash"},
                    }
                    for i, x in enumerate(countries)
                ]
                + [
                    {
                        "x": list(
                            self.df_rural_urban_population_growth.loc[
                                self.df_rural_urban_population_growth["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_rural_urban_population_growth["Indicator Code"]
                                == "SP.URB.GROW"
                            ]
                            .dropna(axis="columns", how="all")
                            .columns[4:]
                        ),
                        "y": list(
                            self.df_rural_urban_population_growth.loc[
                                self.df_rural_urban_population_growth["Country Name"]
                                == x
                            ]
                            .loc[
                                self.df_rural_urban_population_growth["Indicator Code"]
                                == "SP.URB.GROW"
                            ]
                            .iloc[:, 4:]
                            .dropna(axis="columns", how="all")
                            .values.tolist()[0]
                        ),
                        "type": "line",
                        "name": f"{x}, urban",
                        "line": {"color": colors[i % len(colors)], "dash": "dot"},
                    }
                    for i, x in enumerate(countries)
                ],
                "layout": {
                    "title": "Rural vs urban population growth (annual %)",
                    "xaxis": {"range": years},
                },
            }

            return (
                population,
                population_growth,
                rural_urban_population,
                rural_urban_population_growth,
            )
