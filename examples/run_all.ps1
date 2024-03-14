# first run for a country: update the settings
postalcode2nuts -i postal_codes_NL.txt --verbose --country NL --update
postalcode2nuts -i postal_codes_NL.txt --verbose --level 2
postalcode2nuts -i postal_codes_NL.txt --verbose --level 1
postalcode2nuts -i postal_codes_NL.txt --verbose --level 0

# first run for a country: update the settings
postalcode2nuts -i postal_codes_BE.txt --verbose --country BE --update
postalcode2nuts -i postal_codes_BE.txt --verbose --level 2
