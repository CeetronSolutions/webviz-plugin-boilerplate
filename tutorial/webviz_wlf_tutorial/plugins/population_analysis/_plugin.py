from typing import List, Type, Union
from pathlib import Path

import pandas as pd
from webviz_config import WebvizPluginABC
from dash.development.base_component import Component

from ._plugin_ids import PluginIds
from ._error import error
from ._shared_settings import Filter
from ._views._birth_death_fertility._birth_indicators import BirthIndicators
from ._views._birth_death_fertility._mortality_rates_and_death import (
    MortalityRatesAndNumberOfDeaths,
)
from ._views._population._by_ages import PopulationByAges
from ._views._population._indicators import PopulationIndicators

from ._shared_view_elements._graph import Graph
from ._views._population._by_ages._view import (
    ViewSettings as PopulationByAgesViewSettings,
)
from ._views._population._indicators._settings import (
    ViewSettings as PopulationIndicatorsViewSettings,
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
    This is just an overview over this tutorial plugin's file structure. This is not necessary to implement for custom
    plugins.
    * shared_settings/ - A directory containing all shared settings files
      - _filter.py - A SettingsGroupABC subclass containing settings for globally filtering countries and years
    * view_elements/ - A directory containing all generic view elements, i.e. view elements that are used by different
       views in different view groups
      - _graph.py - A view element for displaying a wcc.Graph (used by all views in this plugin for plotting data)
    * views/
      - birth_death_fertility/ - A directory containing all views in the view group 'Birth, death and fertility'
        - _birth_indicators.py - A view on different indicators related to birth, e.g. birth and fertility rates and
          life expectancy
        - _mortality_rates_and_death.py - A view on different indicators related to death and mortality,
          e.g. death rate and mortality rate for different age groups
      - population/ - A directory containing all views in the view group 'Population'
        - _by_ages.py - A view on the population of the selected countries divided by different age groups
        - _indicators.py - A view on the population development, e.g. population growth and rural vs. urban population
    * _error.py - Contaings a layout function for error messages
    * _plugin_ids - Contains both IDs for all views and stores and the names of the view groups
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
            PluginIds.SharedSettings.FILTER,
        )

        self.add_view(
            BirthIndicators(self.population_df),
            PluginIds.BirthDeathFertility.BIRTH_INDICATORS,
            PluginIds.BirthDeathFertility.GROUP_NAME,
        )
        self.add_view(
            MortalityRatesAndNumberOfDeaths(self.population_df),
            PluginIds.BirthDeathFertility.MORTALITY_RATES_AND_NUMBER_OF_DEATHS,
            PluginIds.BirthDeathFertility.GROUP_NAME,
        )

        self.add_view(
            PopulationByAges(self.population_df),
            PluginIds.Population.BY_AGES,
            PluginIds.Population.GROUP_NAME,
        )
        self.add_view(
            PopulationIndicators(self.population_df),
            PluginIds.Population.INDICATORS,
            PluginIds.Population.GROUP_NAME,
        )

    @property
    def tour_steps(self) -> List[dict]:
        return [
            {
                "id": self.shared_settings_group(
                    PluginIds.SharedSettings.FILTER
                ).component_unique_id(Filter.Ids.COUNTRY_SELECT),
                "content": """Select for which countries you want to have data shown. This is a global setting and is 
                applied to all views of this plugin. Note that the more countries are selected the more the plugin's
                loading time increases and the harder the plots get to understand. Consider selecting at max 5 countries.
                """,
            },
            {
                "id": self.shared_settings_group(
                    PluginIds.SharedSettings.FILTER
                ).component_unique_id(Filter.Ids.YEAR_SLIDER),
                "content": """Restrict the years you want data to be shown for. This is a global setting and is 
                applied to all views of this plugin.""",
            },
            {
                "id": self.view(PluginIds.BirthDeathFertility.BIRTH_INDICATORS)
                .view_element(BirthIndicators.Ids.BIRTH_RATES)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Crude birth rate indicates the number of live births occurring during the year, 
                per 1,000 population estimated at midyear. Subtracting the crude death rate from the crude birth rate 
                provides the rate of natural increase, which is equal to the rate of population change in the absence 
                of migration.""",
            },
            {
                "id": self.view(PluginIds.BirthDeathFertility.BIRTH_INDICATORS)
                .view_element(BirthIndicators.Ids.FERTILITY_RATES)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Total fertility rate represents the number of children that would be born to a woman 
                if she were to live to the end of her childbearing years and bear children in accordance with 
                age-specific fertility rates of the specified year.
                """,
            },
            {
                "id": self.view(PluginIds.BirthDeathFertility.BIRTH_INDICATORS)
                .view_element(BirthIndicators.Ids.LIFE_EXPECTANCY)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Life expectancy at birth indicates the number of years a newborn infant would live if 
                prevailing patterns of mortality at the time of its birth were to stay the same throughout its life.
                """,
            },
            {
                "id": self.view(PluginIds.BirthDeathFertility.BIRTH_INDICATORS)
                .view_element(BirthIndicators.Ids.SEX_RATIO)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Sex ratio at birth refers to male births per female births. The data are 5 year averages.
                """,
            },
            {
                "id": self.view(
                    PluginIds.BirthDeathFertility.MORTALITY_RATES_AND_NUMBER_OF_DEATHS
                )
                .view_element(MortalityRatesAndNumberOfDeaths.Ids.DEATH_RATE)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Crude death rate indicates the number of deaths occurring during the year, per 1,000 
                population estimated at midyear. Subtracting the crude death rate from the crude birth rate provides 
                the rate of natural increase, which is equal to the rate of population change in the absence of 
                migration.""",
            },
            {
                "id": self.view(
                    PluginIds.BirthDeathFertility.MORTALITY_RATES_AND_NUMBER_OF_DEATHS
                )
                .view_element(MortalityRatesAndNumberOfDeaths.Ids.MORTALITY_RATE_ADULTS)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Adult mortality rate, is the probability of dying between the ages of 15 and 60 - that is, 
                the probability of a 15-year-old female/male dying before reaching age 60, if subject to age-specific 
                mortality rates of the specified year between those ages.
                """,
            },
            {
                "id": self.view(
                    PluginIds.BirthDeathFertility.MORTALITY_RATES_AND_NUMBER_OF_DEATHS
                )
                .view_element(
                    MortalityRatesAndNumberOfDeaths.Ids.MORTALITY_RATE_INFANTS
                )
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Infant mortality rate is the number of infants dying before reaching one year of age, 
                per 1,000 live births in a given year.
                """,
            },
            {
                "id": self.view(
                    PluginIds.BirthDeathFertility.MORTALITY_RATES_AND_NUMBER_OF_DEATHS
                )
                .view_element(
                    MortalityRatesAndNumberOfDeaths.Ids.MORTALITY_RATE_NEONATAL
                )
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Neonatal mortality rate is the number of neonates dying before reaching 28 days of age, 
                per 1,000 live births in a given year.
                """,
            },
            {
                "id": self.view(
                    PluginIds.BirthDeathFertility.MORTALITY_RATES_AND_NUMBER_OF_DEATHS
                )
                .view_element(
                    MortalityRatesAndNumberOfDeaths.Ids.MORTALITY_RATE_UNDER_FIVE
                )
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Under-five mortality rate is the probability per 1,000 that a newborn baby will die 
                before reaching age five, if subject to age-specific mortality rates of the specified year.
                """,
            },
            {
                "id": self.view(PluginIds.Population.BY_AGES)
                .layout_element(PopulationByAges.Ids.MAIN_COLUMN)
                .get_unique_id(),
                "content": """Population between the respective ages as a percentage of the total population. 
                Population is based on the de facto definition of population.
                """,
            },
            {
                "id": self.view(PluginIds.Population.BY_AGES)
                .settings_group(PopulationByAges.Ids.SETTINGS)
                .component_unique_id(PopulationByAgesViewSettings.Ids.VIEW_BY),
                "content": """Here you can select if the data shall be viewed by age groups or selected countries.
                """,
            },
            {
                "id": self.view(PluginIds.Population.BY_AGES)
                .settings_group(PopulationByAges.Ids.SETTINGS)
                .component_unique_id(PopulationByAgesViewSettings.Ids.VALUES),
                "content": """Select if you want to work with absolute or relative data.
                """,
            },
            {
                "id": self.view(PluginIds.Population.BY_AGES)
                .settings_group(PopulationByAges.Ids.SETTINGS)
                .component_unique_id(PopulationByAgesViewSettings.Ids.GENDER),
                "content": """Use this option to have a closer look at a particular gender.
                """,
            },
            {
                "id": self.view(PluginIds.Population.INDICATORS)
                .view_element(PopulationIndicators.Ids.POPULATION)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Total population is based on the de facto definition of population, 
                which counts all residents regardless of legal status or citizenship. 
                The values shown are midyear estimates.
                """,
            },
            {
                "id": self.view(PluginIds.Population.INDICATORS)
                .view_element(PopulationIndicators.Ids.POPULATION_GROWTH)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Annual population growth rate for year t is the exponential rate of growth of midyear 
                population from year t-1 to t, expressed as a percentage . Population is based on the de facto 
                definition of population, which counts all residents regardless of legal status or citizenship.
                """,
            },
            {
                "id": self.view(PluginIds.Population.INDICATORS)
                .view_element(PopulationIndicators.Ids.RURAL_URBAN_POPULATION)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Rural/urban population refers to people living in rural/urban areas as defined by 
                national statistical offices. It is calculated as the difference between total population and 
                urban/rural population. Aggregation of urban and rural population may not add up to total population 
                because of different country coverages.
                """,
            },
            {
                "id": self.view(PluginIds.Population.INDICATORS)
                .view_element(PopulationIndicators.Ids.RURAL_URBAN_POPULATION_GROWTH)
                .component_unique_id(Graph.Ids.GRAPH),
                "content": """Rural/urban population refers to people living in rural/urban areas as defined by 
                national statistical offices. It is calculated as the difference between total population and 
                urban/rural population.""",
            },
            {
                "id": self.view(PluginIds.Population.INDICATORS)
                .settings_group(PopulationIndicators.Ids.SETTINGS)
                .component_unique_id(PopulationIndicatorsViewSettings.Ids.VALUES),
                "content": """Select if you want to work with absolute or relative data.
                """,
            },
        ]

    @property
    def layout(self) -> Union[str, Type[Component]]:
        """
        This method is only going to be called when no views have been added to the plugin,
        i.e. when the data could not be read and the '__init__' method terminated with setting
        the 'error_message' member.
        """
        return error(self.error_message)
