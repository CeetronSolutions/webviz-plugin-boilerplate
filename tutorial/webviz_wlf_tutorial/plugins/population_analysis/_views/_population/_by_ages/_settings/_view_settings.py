from typing import List

from dash.development.base_component import Component
from webviz_config.webviz_plugin_subclasses import SettingsGroupABC
import webviz_core_components as wcc


class ViewSettings(SettingsGroupABC):
    class Ids:
        VIEW_BY = "view-by"
        VALUES = "values"
        GENDER = "gender"

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
            wcc.RadioItems(
                id=self.register_component_unique_id(ViewSettings.Ids.GENDER),
                label="Gender",
                options=[
                    {"label": "Both", "value": "both"},
                    {"label": "Female", "value": "female"},
                    {"label": "Male", "value": "male"},
                ],
                value="both",
            ),
        ]
