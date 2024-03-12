from nutstools.postalnuts import NutsPostalCode, NutsData

# This initialises the default file location (in local cache) + downloads the file from the eurostat website
nuts_data = NutsData()

# This reads the postcode from the nuts code file and turns it into a data frame
nuts = NutsPostalCode(nuts_data.nuts_codes_file)

# now you can convert single postal code to NUTS
post_code = "2612AB"
nuts_code = nuts.one_postal2nuts(postal_code=post_code)
print(f"Postal code {post_code} has nuts code {nuts_code}")

# or you can convert a series of postcode
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
print("\nNUTS code at level 3:")
print(all_codes)

# doing the same for nuts level 1 gives
all_codes = nuts.postal2nuts(postal_codes=postal_codes, level=1)
print("\nNUTS code at level 1:")
print(all_codes)
