.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=========
NutsTools
=========


    Convert postal codes to NUTS codes

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

The NUTS conversion can also be down in your own Python code by initialising the class::

    import NutsPostalCode

    nuts = NutsPostalCode()
    nuts_code = nuts.one_postal2nuts(postal_code="")

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

Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
