from typing import Type, Union

from dash.development.base_component import Component
from webviz_config.webviz_plugin_subclasses import (
    ViewElementABC,
)
import webviz_core_components as wcc


class Graph(ViewElementABC):
    class Ids:
        GRAPH = "graph"

    def __init__(self, height: str = "43vh") -> None:
        super().__init__()

        self.height = height

    def inner_layout(self) -> Union[str, Type[Component]]:
        return wcc.Graph(
            id=self.register_component_unique_id(Graph.Ids.GRAPH),
            config={"displayModeBar": False},
            style={"height": self.height, "min-height": "300px"},
        )
