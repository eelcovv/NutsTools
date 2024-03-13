# This file contains the global variables used in the code for NutsTools. It stores the default values.
# The values are stored in the settings file stored in the default location (LocalAppData\NutsTools in Windows or
# .local/share/NutsTools in Linux). The second run, the global variables are read from this settings file. You can
# modify the settings file to your needs.

NUTS_CODE_DEFAULT_DIRECTORY = "nutstools"
NUTS_CODE_DEFAULT_SETTINGS_FILE_NAME = "nutstools_settings.yml"

NUTS_DATA = {
    "2021": {
        "url": "https://gisco-services.ec.europa.eu/tercet/NUTS-2021/",
        "files": {
            "AT": "pc2020_AT_NUTS-2021_v1.0.zip",
            "BE": "pc2020_BE_NUTS-2021_v1.0.zip",
            "BG": "pc2020_BG_NUTS-2021_v1.0.zip",
            "CH": "pc2020_CH_NUTS-2021_v1.0.zip",
            "CY": "pc2020_CY_NUTS-2021_v1.0.zip",
            "CZ": "pc2020_CZ_NUTS-2021_v2.0.zip",
            "DE": "pc2020_DE_NUTS-2021_v4.0.zip",
            "DK": "pc2020_DK_NUTS-2021_v1.0.zip",
            "EE": "pc2020_EE_NUTS-2021_v1.0.zip",
            "EL": "pc2020_EL_NUTS-2021_v1.0.zip",
            "ES": "pc2020_ES_NUTS-2021_v1.0.zip",
            "FI": "pc2020_FI_NUTS-2021_v1.0.zip",
            "FR": "pc2020_FR_NUTS-2021_v2.0.zip",
            "HR": "pc2020_HR_NUTS-2021_v2.0.zip",
            "HU": "pc2020_HU_NUTS-2021_v1.0.zip",
            "IE": "pc2020_IE_NUTS-2021_v1.0.zip",
            "IS": "pc2020_IS_NUTS-2021_v1.0.zip",
            "IT": "pc2020_IT_NUTS-2021_v1.0.zip",
            "LI": "pc2020_LI_NUTS-2021_v1.0.zip",
            "LT": "pc2020_LT_NUTS-2021_v1.0.zip",
            "LU": "pc2020_LU_NUTS-2021_v1.0.zip",
            "LV": "pc2020_LV_NUTS-2021_v1.0.zip",
            "MK": "pc2020_MK_NUTS-2021_v1.0.zip",
            "NL": "pc2020_NL_NUTS-2021_v2.0.zip",
            "NO": "pc2020_NO_NUTS-2021_v2.0.zip",
            "PT": "pc2020_PT_NUTS-2021_v1.0.zip",
            "PL": "pc2020_PL_NUTS-2021_v1.0.zip",
            "RO": "pc2020_RO_NUTS-2021_v2.0.zip",
            "RS": "pc2020_RS_NUTS-2021_v1.0.zip",
            "SE": "pc2020_SE_NUTS-2021_v2.0.zip",
            "SI": "pc2020_SI_NUTS-2021_v1.0.zip",
            "SK": "pc2020_SK_NUTS-2021_v2.0.zip",
            "TR": "pc2020_TR_NUTS-2021_v1.0.zip",
            "UK": "pc2020_UK_NUTS-2021_v3.0.zip",
        },
    }
}


DEFAULT_YEAR = "2021"
DEFAULT_COUNTRY = "NL"
NUTS_YEARS = set(NUTS_DATA.keys())
COUNTRY_CODES = set(NUTS_DATA[DEFAULT_YEAR]["files"].keys())
