import csv

# Creates a composite dictionary of <state,area> to silver plan rates
# @return the composite dictionary
def createRateDictionary():
    outputDictionary = {}
    with open('testData/plans.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Read each row but only save the silver plan entries
        for row in reader:
            if (row['metal_level'].lower() == 'silver'):
                key = tuple([row['state'].lower(), row['rate_area'].lower()])

                # if the item exists append to list otherwise create a new one
                if key in outputDictionary:
                    rates = outputDictionary[key]
                    rates.append(row['rate'])
                    rates.sort()
                    outputDictionary[key] = rates
                else:
                    outputDictionary[key] = [row['rate']]
    return outputDictionary

# Create a dictionary of <zip codes> to the 2nd lowest rate
# @param rateDictionary composite dictionary of <state,area> to silver plan rates
# @return the composite dictionary
def createZipRateDictionary(rateDictionary):
    sanitizedZipCodes = sanitizeZipCodes()
    outputDictionary = {}
    with open('testData/zips.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Read each row
        for row in reader:
            key = tuple([row['state'].lower(), row['rate_area'].lower()])
            # if the item exists assoicate the zip to the 2nd lowest rate
            if key in rateDictionary:
                rates = rateDictionary[key]

                # Check if the zipcode the zip code is ambiguous
                zipkey = row['zipcode'].lower()
                if zipkey in sanitizedZipCodes:
                    if sanitizedZipCodes[zipkey] != '?':

                        # Check if there is more than one rate get index 1 in presorted list
                        if len(rates) > 1:
                            outputDictionary[row['zipcode'].lower()] = rates[1]
                       # else There is only one entry do nothing
                    # else Zip code is ambiguous
                # else Zip code does not exsist in the list (This should never happen since they are from the same file but its good to check)

            # else Do nothing no rate data available

    return outputDictionary

# sanitizes the zips.csv to determines what is ambiguous and creates a dictionary of zip codes to rate_area.
# @param zipDictionary dictionary of <zip> to rate_area
# @return the dictionary
def sanitizeZipCodes():
    zipDictionary = {}
    with open('testData/zips.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Read each row
        for row in reader:
            key = row['zipcode'].lower()

            # Check if this zip code exists in the list already
            if key in zipDictionary:
                # If its a duplicate allow it to stay otherwise the zip code is ambiguous
                # Denoted with '?' for later use
                if zipDictionary[key] != row['rate_area'].lower():
                    zipDictionary[key] = '?'
            else:
                # Add it if not exists
                zipDictionary[key] = row['rate_area'].lower()
    return zipDictionary

# updates the SLCSP CSV File and writes to console
# @param zipRateDictionary dictionary of <zip> to 2nd lowest price
def updateSlcspFile(zipRateDictionary):
    outputDictionary = {}
    with open('testData/slcsp.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Read each row
        for row in reader:
            key = row['zipcode'].lower()

            # if the rate zip assoication exists update the output
            if key in zipRateDictionary:
                outputDictionary[row['zipcode']] = zipRateDictionary[key]
            else:
                outputDictionary[row['zipcode']] = ''

    # Write out an updated CSV file and StdOut
    with open('slcsp_updated.csv', 'w', newline='') as file:
        fieldnames = ['zipcode', 'rate']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        print(fieldnames)

        for entry in outputDictionary:

            # Attempt to format the float
            if outputDictionary[entry] != '':
                row = {'zipcode': entry, 'rate': format(
                    float(outputDictionary[entry]), '.2f')}
                stdOutStr = entry + ', ' + \
                    format(float(outputDictionary[entry]), '.2f')
            else:
                row = {'zipcode': entry, 'rate': outputDictionary[entry]}
                stdOutStr = entry + ', ' + outputDictionary[entry]
            print(stdOutStr)    # write StdOut
            writer.writerow(row)  # Write file


# Get the composite Dictionary <state, area> = area_rate
rateDictionary = createRateDictionary()

# Get the Dictionary <Zip> = 2nd lowest rate and remove all zip code ambiguity
zipRateDictionary = createZipRateDictionary(rateDictionary)

# Create an updated the CSV
updateSlcspFile(zipRateDictionary)

print("NOTE: Please see 'slcsp_updated.csv' in the same folder as this program for the output in csv format")
