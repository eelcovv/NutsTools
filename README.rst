=========
NutsTools
=========


    Convert postal codes to NUTS codes

EU NUTS (an abbreviation for Nomenclature of Territorial Units for Statistics) codes are standardized codes used by the
European Union to define administrative and statistical regions for the purpose of data collection and analysis.

The translation between Postal codes of home addresses and de NUTS code is given at the EU website. This tools
is an  Python interface to easily obtain the code lists and transform postal codes into NUTS codes.

------------
Installation
------------

Install the tool by::

    pip install nutstools

In case you are behind a proxy which requires authentication you may want to install the packages
*requests_kerberos_proxy*. You can install it yourself with::

    pip install requests-kerberos-proxy

or, alternatively, install the nutstools package as::

    pip install nutstools[proxy]

which will automatically include the required proxy packages

-----
Usage
-----

Command line tool
-----------------

This tools can be used to convert postal codes to NUTS codes.
Run the following to get the nuts belong by the postal code 2612AB::

    >> postalcode2nuts.exe -p 2612AB

This yields the following output::

    2612AB    NL333

So the nuts3 code belong to the postal code *2612AB* is *NL333*.

It is also possible to convert the postal codes stored in a file using the -i option.
In case your file with the name *postal_codes.txt* contains the following::

    '8277 AM'
    '2871 KA'
    '9408 BJ'
    '3076 KA'
    '3068 LM'
    '7543 GV'

Running the following::

    >> postalcode2nuts.exe -i postal_codes.txt -o -

gives  the following output::

    8277AM    NL211
    2871KA    NL33B
    9408BJ    NL131
    3076KA    NL33C
    3068LM    NL33C
    7543GV    NL213

In case the output argument *-o -* i is left out, the output filename will be based on
the input file with the suffix *nuts3*, where 3 stands for the nuts level of the output.

Help message
------------

The full help  message of the tools is::

    PS> postalcode2nuts.exe --help
    usage: postalcode2nuts [-h] [--version] [-p POSTALCODE] [-i INPUT_FILE_NAME] [--nuts_file_name NUTS_INPUT_FILE_NAME]
                           [-o OUTPUT_FILE_NAME] [-v] [-vv] [-l LEVEL] [--year {2021}]
                           [--country {DE,SK,FI,DK,IT,LU,LI,SE,LV,TR,UK,ES,EE,HR,MK,CY,IS,AT,RO,HU,BG,BE,PL,CH,RS,IE,CZ,NL,NO,PT,SI,LT,FR,EL}]
                           [--update_settings] [--directory DIRECTORY]

    Converts a postal code to its NUTS code

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -p POSTALCODE, --postal_code POSTALCODE
                            Postcode
      -i INPUT_FILE_NAME, --input_file_name INPUT_FILE_NAME
                            Input file with Postal codes
      --nuts_file_name NUTS_INPUT_FILE_NAME
                            Overrule input filename with the NUTS translation data
      -o OUTPUT_FILE_NAME, --output_file_name OUTPUT_FILE_NAME
                            Output file with Postal codes and NUTS
      -v, --verbose         set loglevel to INFO
      -vv, --debug          set loglevel to DEBUG
      -l LEVEL, --level LEVEL
                            The level at we want to get the NUTS-code
      --year {2021}         The year of the NUTS files
      --country {DE,SK,FI,DK,IT,LU,LI,SE,LV,TR,UK,ES,EE,HR,MK,CY,IS,AT,RO,HU,BG,BE,PL,CH,RS,IE,CZ,NL,NO,PT,SI,LT,FR,EL}
                            The country code for the NUTS file
      --update_settings     Update the settings file with the new values
      --directory DIRECTORY
                            The location of the the NUTS files. If not given, the default directory will be picked

Python API
----------

The NUTS conversion can also be used in your own Python code. As an example,
this initialises the default file location (in local cache)
and it downloads the file from the eurostat website::

    from nutstools.postalnuts import NutsPostalCode, NutsData

    nuts_data = NutsData()

At this point the NUTS data file has been downloaded from the Eurostat website
and stored in the default location. You can now create an object with the nuts data::

    nuts = NutsPostalCode(nuts_data.nuts_codes_file)

The Nuts translation are stored at the same location in the file the *nuts.nuts_data* attribute. At this point you
can get a nuts code for a specific postal with as::

    post_code = "2612AB"
    nuts_code = nuts.one_postal2nuts(postal_code=post_code)
    print(f"Postal code {post_code} has nuts code {nuts_code}")

Which yields the output::

    Postal code 2612AB has nuts code NL333

Conversion of a list of postal code is also possible as::

    postal_codes = [
        "8277 AM",
        "2871 KA",
        "9408 BJ",
        "3076 KA",
        "3068 LM",
        "7543 GV",
        "4181 DG",
    ]

    all_codes = nuts.postal2nuts(postal_codes=postal_codes)

giving as output::

    8277AM    NL211
    2871KA    NL33B
    9408BJ    NL131
    3076KA    NL33C
    3068LM    NL33C
    7543GV    NL213
    4181DG    NL224
    Name: NUTS3, dtype: object

The same can be done for NUTS level 1::

    all_codes = nuts.postal2nuts(postal_codes=postal_codes, level=1)

which gives the following output::

    8277AM    NL2
    2871KA    NL3
    9408BJ    NL1
    3076KA    NL3
    3068LM    NL3
    7543GV    NL2
    4181DG    NL2
    Name: NUTS1, dtype: object


Default Settings
----------------

By default, postalcode2nuts will download the nuts code from the website
https://gisco-services.ec.europa.eu/tercet/NUTS-2021/.

The data is stored in *C:\\Users\\MyUser\\AppData\\Local* (windows) or *.local/share* (Linux)
in the directory *nutstools*. This location can be altered via the command line argument
*--directory <location>*.

The default settings are stored in the file *nutstools_settings.yml*. The contents of this file
contains all the default choices, such as the default country for which the NUTS code conversion
is applied (default is for The Netherlands using the code 'NL').
The contents of the settings file look like::

    COUNTRY_CODES: !!set
        <list of country codes>
    DEFAULT_COUNTRY: NL
    DEFAULT_YEAR: '2021'
    NUTS_CODE_DEFAULT_DIRECTORY: C:/Users/MyUser/AppData/Local/nutstools
    NUTS_DATA:
      '2021':
        files:
          NL: pc2020_NL_NUTS-2021_v2.0.zip
        url: https://gisco-services.ec.europa.eu/tercet/NUTS-2021/
    NUTS_YEARS: !!
      '2021': null

After running the code for the first time, the NUTS data file can be found in the *Cache* directory
at the same location. The next time the tool is run, the Cached files are used instead of downloading the
file again.

In case you want to alter the default choices, you can just modify the settings file to your needs.

Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
