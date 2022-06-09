class ElementIds:
    class Stores:
        SELECTED_COUNTRIES = "selected-countries"
        SELECTED_YEARS = "selected-years"

    class SharedSettings:
        class Filter:
            ID = "filter"

    GRAPH = "graph"

    class BirthDeathFertility:
        NAME = "Birth, death and fertility"

        class BirthIndicators:
            ID = "birth-indicators"

            BIRTH_RATES = "birth-rates"
            FERTILITY_RATES = "fertility-rates"
            LIFE_EXPECTANCY = "life-expectancy"
            SEX_RATIO = "sex-ratio"
            SETTINGS = "settings"
            CHART_TYPE = "chart-type"

        class MortalityRatesAndNumberOfDeaths:
            ID = "mortality-death-rates"

            DEATH_RATE = "death-rate"
            MORTALITY_RATE_ADULTS = "mortality-rate-adults"
            MORTALITY_RATE_INFANTS = "mortality-rate-infants"
            MORTALITY_RATE_NEONATAL = "mortality-rate-neonatal"
            MORTALITY_RATE_UNDER_FIVE = "mortality-rate-under-five"

    class Population:
        NAME = "Population"

        class ByAges:
            ID = "by-ages"

            MAIN_COLUMN = "main-column"
            SETTINGS = "settings"

        class Indicators:
            ID = "indicators"
