from typing import List

from dash.development.base_component import Component
from webviz_config.webviz_plugin_subclasses import SettingsGroupABC

import webviz_core_components as wcc


class ViewSettings(SettingsGroupABC):
    class Ids:
        VALUES = "values"

    def __init__(self) -> None:
        super().__init__("View settings")

    def layout(self) -> List[Component]:
        return [
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
