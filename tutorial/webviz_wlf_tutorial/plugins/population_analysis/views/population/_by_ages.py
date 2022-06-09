from typing import List

from dash import callback, Input, Output
from dash.development.base_component import Component
import math
import pandas as pd
import plotly.colors
from webviz_config.webviz_plugin_subclasses import SettingsGroupABC, ViewABC
import webviz_core_components as wcc

from ..._element_ids import ElementIds


class ViewSettings(SettingsGroupABC):
    class Ids:
        VIEW_BY = "view-by"
        VALUES = "values"

    def __init__(self) -> None:
        super().__init__("View settings")

    def layout(self) -> List[Component]:
        return [
            wcc.RadioItems(
                id=self.register_component_unique_id(ViewSettings.Ids.VIEW_BY),
                label="View by",
                options=[
                    {"label": "Age group", "value": "age-group"},
                    {"label": "Country", "value": "country"},
                ],
                value="age-group",
            ),
            wcc.RadioItems(
                id=self.register_component_unique_id(ViewSettings.Ids.VALUES),
                label="Relative or absolute values",
                options=[
                    {"label": "Absolute", "value": "absolute"},
                    {"label": "Relative", "value": "relative"},
                ],
                value="absolute",
            ),
        ]


class PopulationByAges(ViewABC):
    def __init__(self, population_df: pd.DataFrame) -> None:
        super().__init__("Population by ages")

        self.add_settings_group(ViewSettings(), ElementIds.Population.ByAges.SETTINGS)

        self.absolute_indicators_female = [
            f"SP.POP.{str(i).zfill(2)}{str(i+4).zfill(2)}.FE" for i in range(0, 76, 5)
        ] + ["SP.POP.80UP.FE"]
        self.absolute_indicators_male = [
            f"SP.POP.{str(i).zfill(2)}{str(i+4).zfill(2)}.MA" for i in range(0, 76, 5)
        ] + ["SP.POP.80UP.MA"]
        self.relative_indicators_female = [
            f"SP.POP.{str(i).zfill(2)}{str(i+4).zfill(2)}.FE.5Y"
            for i in range(0, 76, 5)
        ] + ["SP.POP.80UP.FE.5Y"]
        self.relative_indicators_male = [
            f"SP.POP.{str(i).zfill(2)}{str(i+4).zfill(2)}.MA.5Y"
            for i in range(0, 76, 5)
        ] + ["SP.POP.80UP.MA.5Y"]

        self.df_pop_ages_female = population_df[
            population_df["Indicator Code"].isin(self.absolute_indicators_female)
        ]
        self.df_pop_ages_male = population_df[
            population_df["Indicator Code"].isin(self.absolute_indicators_male)
        ]
        self.df_pop_ages_female_relative = population_df[
            population_df["Indicator Code"].isin(self.relative_indicators_female)
        ]
        self.df_pop_ages_male_relative = population_df[
            population_df["Indicator Code"].isin(self.relative_indicators_male)
        ]

        self.main_column = self.add_column(ElementIds.Population.ByAges.MAIN_COLUMN)

    def set_callbacks(self) -> None:
        @callback(
            Output(
                self.layout_element(ElementIds.Population.ByAges.MAIN_COLUMN)
                .get_unique_id()
                .to_string(),
                "children",
            ),
            Input(
                self.get_store_unique_id(ElementIds.Stores.SELECTED_COUNTRIES), "data"
            ),
            Input(self.get_store_unique_id(ElementIds.Stores.SELECTED_YEARS), "data"),
            Input(
                self.settings_group(ElementIds.Population.ByAges.SETTINGS)
                .component_unique_id(ViewSettings.Ids.VIEW_BY)
                .to_string(),
                "value",
            ),
            Input(
                self.settings_group(ElementIds.Population.ByAges.SETTINGS)
                .component_unique_id(ViewSettings.Ids.VALUES)
                .to_string(),
                "value",
            ),
        )
        def _adjust_plots(
            countries: List[str], years: List[int], view_by: str, abs_rel_values: str
        ) -> List[Component]:
            view_elements = []
            colors = plotly.colors.DEFAULT_PLOTLY_COLORS

            max_num_columns = 4

            current_row_elements = []
            current_column = 0

            year_column_indices = [4 + years[0] - 1960, 4 + years[1] - 1960]

            if view_by == "age-group":
                for index, age_group in enumerate(
                    zip(self.absolute_indicators_female, self.absolute_indicators_male)
                ):

                    figure = {
                        "data": [
                            {
                                "x": list(
                                    self.df_pop_ages_female.dropna(
                                        axis="columns", how="all"
                                    ).columns[
                                        year_column_indices[0] : year_column_indices[1]
                                    ]
                                ),
                                "y": list(
                                    self.df_pop_ages_female.loc[
                                        self.df_pop_ages_female["Country Name"] == x
                                    ]
                                    .loc[
                                        self.df_pop_ages_female["Indicator Code"]
                                        == age_group[0]
                                    ]
                                    .iloc[
                                        :,
                                        year_column_indices[0] : year_column_indices[1],
                                    ]
                                    .dropna(axis="columns", how="all")
                                    .values.tolist()[0]
                                ),
                                "type": "line",
                                "name": f"{x}, female",
                                "line": {
                                    "color": colors[i % len(colors)],
                                    "dash": "dot",
                                },
                            }
                            for i, x in enumerate(countries)
                        ]
                        + [
                            {
                                "x": list(
                                    self.df_pop_ages_male.dropna(
                                        axis="columns", how="all"
                                    ).columns[
                                        year_column_indices[0] : year_column_indices[1]
                                    ]
                                ),
                                "y": list(
                                    self.df_pop_ages_male.loc[
                                        self.df_pop_ages_male["Country Name"] == x
                                    ]
                                    .loc[
                                        self.df_pop_ages_male["Indicator Code"]
                                        == age_group[1]
                                    ]
                                    .iloc[
                                        :,
                                        year_column_indices[0] : year_column_indices[1],
                                    ]
                                    .dropna(axis="columns", how="all")
                                    .values.tolist()[0]
                                ),
                                "type": "line",
                                "name": f"{x}, male",
                                "line": {
                                    "color": colors[i % len(colors)],
                                    "dash": "dot",
                                },
                            }
                            for i, x in enumerate(countries)
                        ],
                        "layout": {
                            "title": str(
                                self.df_pop_ages_female.loc[
                                    self.df_pop_ages_female["Indicator Code"]
                                    == age_group[0]
                                ]["Indicator Name"].tolist()[0]
                            ).replace(", female", "")
                        },
                    }
                    current_row_elements.append(
                        wcc.WebvizViewElement(
                            children=[
                                wcc.Graph(figure=figure, style={"height": "30vh"})
                            ],
                            id=self.unique_id(age_group[0]),
                        )
                    )

                    current_column += 1

                    if (
                        current_column >= max_num_columns
                        or index == len(self.df_pop_ages_female) - 1
                    ):
                        view_elements.append(
                            wcc.WebvizPluginLayoutRow(current_row_elements)
                        )
                        current_row_elements = []
                        current_column = 0

            else:
                graph_height = max(45.0, 90.0 / len(countries))
                max_num_columns = int(
                    math.ceil(float(len(countries)) * graph_height / 90.0)
                )
                for index, country in enumerate(countries):
                    x_values = []
                    for x in self.df_pop_ages_female.dropna(
                        axis="columns", how="all"
                    ).columns[year_column_indices[0] : year_column_indices[1]]:
                        x_values.append(f"{x}, female")
                        x_values.append(f"{x}, male")

                    df_female = (
                        self.df_pop_ages_female
                        if abs_rel_values == "absolute"
                        else self.df_pop_ages_female_relative
                    )
                    df_male = (
                        self.df_pop_ages_male
                        if abs_rel_values == "absolute"
                        else self.df_pop_ages_male_relative
                    )

                    figure = {
                        "data": [
                            {
                                "x": x_values,
                                "y": [
                                    item
                                    for t in zip(
                                        list(
                                            df_female.loc[
                                                df_female["Country Name"] == country
                                            ]
                                            .loc[df_female["Indicator Code"] == x[0]]
                                            .iloc[
                                                :,
                                                year_column_indices[
                                                    0
                                                ] : year_column_indices[1],
                                            ]
                                            .dropna(axis="columns", how="all")
                                            .values.tolist()[0]
                                        ),
                                        list(
                                            df_male.loc[
                                                df_male["Country Name"] == country
                                            ]
                                            .loc[df_male["Indicator Code"] == x[1]]
                                            .iloc[
                                                :,
                                                year_column_indices[
                                                    0
                                                ] : year_column_indices[1],
                                            ]
                                            .dropna(axis="columns", how="all")
                                            .values.tolist()[0]
                                        ),
                                    )
                                    for item in t
                                ],
                                "type": "bar",
                                "name": str(
                                    df_female.loc[df_female["Indicator Code"] == x[0]][
                                        "Indicator Name"
                                    ].tolist()[0]
                                ).replace(", female", ""),
                            }
                            for i, x in enumerate(
                                zip(
                                    self.absolute_indicators_female
                                    if abs_rel_values == "absolute"
                                    else self.relative_indicators_female,
                                    self.absolute_indicators_male
                                    if abs_rel_values == "absolute"
                                    else self.relative_indicators_male,
                                )
                            )
                        ],
                        "layout": {
                            "title": country,
                            "barmode": "stack",
                            "showlegend": False if max_num_columns >= 2 else True,
                        },
                    }
                    current_row_elements.append(
                        wcc.WebvizViewElement(
                            children=[
                                wcc.Graph(
                                    figure=figure, style={"height": f"{graph_height}vh"}
                                )
                            ],
                            id=self.unique_id(country),
                        )
                    )

                    current_column += 1

                    if current_column >= max_num_columns or index == len(countries) - 1:
                        view_elements.append(
                            wcc.WebvizPluginLayoutRow(current_row_elements)
                        )
                        current_row_elements = []
                        current_column = 0

            return view_elements
