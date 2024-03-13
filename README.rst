.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

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

-----
Usage
-----

Command line tool
-----------------

This tools can be used to convert postal codes to NUTS codes.
Run the following to get the nuts belong by the postal code 2612AB::

    >> postalcode2nuts.exe -p 2612AB

This yields the following output::

    CODES
    2612AB    NL333
    Name: NUTS3, dtype: object

So the nuts3 code belong to the postal code *2612AB* is *NL333*.

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
