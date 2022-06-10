from typing import Optional, Type, Union
from pathlib import Path

import pandas as pd
from webviz_config import WebvizPluginABC
from dash.development.base_component import Component

from ._plugin_ids import PluginIds
from ._error import error
from .shared_settings import Filter
from .views import (
    BirthIndicators,
    MortalityRatesAndNumberOfDeaths,
    PopulationByAges,
    PopulationIndicators,
)


class PopulationAnalysis(WebvizPluginABC):
    """
    This Webviz plugin is serving as a demonstration of how to utilize the new Webviz Layout Framework.
    Step by step, it is created in the respective tutorial: MISSING LINK.

    `Plugin functionality`:
    This plugin imports population data from the World Bank's 2022 `Population Estimates And Projections`
    data collection (https://datacatalog.worldbank.org/search/dataset/0037655/Population-Estimates-and-Projections)
    as a CSV file.
    It provides two view groups with two views each on the data:
    -   Birth, death, fertility and life expectancy
        -   Birth indicators
            -   Birth and fertility rates
            -   Life expectancy at birth (male/female/total)
            -   Sex ratio at birth (male births per female
        -   Mortality and death rates
    -   Population
        -   Population by ages
            -   Population ages (0-80+, absolute and relative values)
        -   Population indicators
            -   Population growth (annual %)
            -   Population (male/female/total)
            -   Rural and urban population (absolute/relative/annual growth)

    `Plugin file structure:`
    * _element_ids - Containing element IDs for all elements
    """

    def __init__(self, path_to_population_data_csv_file: Path) -> None:
        super().__init__(stretch=True)

        self.error_message = ""
        try:
            self.population_df = pd.read_csv(path_to_population_data_csv_file)
        except PermissionError:
            self.error_message = (
                f"Access to file '{path_to_population_data_csv_file}' denied."
            )
            "Please check your path for 'path_to_population_data_csv_file' and make sure your application has permission to access it."
            return
        except FileNotFoundError:
            self.error_message = f"File '{path_to_population_data_csv_file}' not found."
            "Please check your path for 'path_to_population_data_csv_file'."
            return
        except pd.errors.ParserError:
            self.error_message = (
                f"File '{path_to_population_data_csv_file}' is not a valid CSV file."
            )
            return
        except pd.errors.EmptyDataError:
            self.error_message = (
                f"File '{path_to_population_data_csv_file}' is an empty file."
            )
            return
        except Exception:
            self.error_message = f"Unknown exception when trying to read '{path_to_population_data_csv_file}'."
            return

        self.add_store(
            PluginIds.Stores.SELECTED_COUNTRIES, WebvizPluginABC.StorageType.SESSION
        )

        self.add_store(
            PluginIds.Stores.SELECTED_YEARS, WebvizPluginABC.StorageType.SESSION
        )

        self.add_shared_settings_group(
            Filter(self.population_df),
            PluginIds.SharedSettings.Filter.ID,
        )

        self.add_view(
            BirthIndicators(self.population_df),
            PluginIds.BirthDeathFertility.BirthIndicators.ID,
            PluginIds.BirthDeathFertility.NAME,
        )
        self.add_view(
            MortalityRatesAndNumberOfDeaths(self.population_df),
            PluginIds.BirthDeathFertility.MortalityRatesAndNumberOfDeaths.ID,
            PluginIds.BirthDeathFertility.NAME,
        )

        self.add_view(
            PopulationByAges(self.population_df),
            PluginIds.Population.ByAges.ID,
            PluginIds.Population.NAME,
        )
        self.add_view(
            PopulationIndicators(self.population_df),
            PluginIds.Population.Indicators.ID,
            PluginIds.Population.NAME,
        )

    @property
    def layout(self) -> Union[str, Type[Component]]:
        return error(self.error_message)
