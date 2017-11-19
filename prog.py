import csv

#
# Loads data from a file and returns the file data as a list, with or without the header row.
#
def load_file(filename, has_header):
	data = []
	with open(filename, 'r') as f:
		zipReader = csv.reader(f, delimiter=',')
		for row in zipReader:
			data.append(row)

	if has_header == True:
		del data[0]

	return data

#
# When there are multiple rate areas, make sure they are all the same. Return true
# or false indicating equality.
#
def verify_rate_areas_equal(zip_code_rate_area_data):

	# Get a list of the rate areas and check if they are the same
	rate_areas = [i[1] for i in zip_code_rate_area_data]

	# If all the values aren't the same, return False
	return all(x == rate_areas[0] for x in rate_areas)	

#
# For a given zipcode, finds the second lowest rate. If a 
# definitive answer can't be found, return blank.
#
def find_silver_rate_plans(zip_code, zip_code_list):

	# Step 1:  Using a list comprehension, find the rate area for a zip code.
	#	   Returned at is State, Rate_Area
	rate_area = [(i[1], i[4]) for i in zip_code_list if i[0] == zip_code]
	
	# Step 2: If we have multiple rows, verify that the rate_areas are the same. If not,
	#         the rate area is ambigous and should be left blank.	
	search_rate_plans = True
	
	if len(rate_area) > 1:
		search_rate_plans = verify_rate_areas_equal(rate_area) 

	# Step 3: Find all the rates for the rate area(s) in step 1, if rate area was determined.
	if search_rate_plans == True:
		# i[4] is rate_area. i[1] is state in plans.csv
		rate_plans = [ i for i in plans_list if i[4] == rate_area[0][1] and i[1] == rate_area[0][0] and i[2] == 'Silver']
		return rate_plans

	return []

#
# Write the file
#
def write_file(modified_data, outfile):
	f = open(outfile, "w")
	f.write("zipcode,rate\n")

	for row in modified_data:
        	f.write("%s,%s\n" % (row[0], row[1]))

	f.close()

# ####################
# Main
# ####################

# First, lets Load the data files
zip_code_list = load_file('zips.csv', True)
plans_list = load_file('plans.csv', True)

# Load the input file into memory.
input_file = load_file('slcsp.csv', True)

# For each row, determine the second lowest priced plan.
for row in input_file:
	silver_rate_plans = find_silver_rate_plans(row[0], zip_code_list)

	prices = ''
	
	# If the rate plans were found.
	if silver_rate_plans: 
		# Get a list of all the prices
		prices = [i[3] for i in silver_rate_plans]
        
		# If there are multiple price plans, sort them and take second lowest one.	
		if len(prices) >= 1:
			prices.sort()
			price = prices[1]
		elif len(prices) == 1:
			# No need to sort here
                	price = prices[0]
		else:
			#  Default to empty, if something unexpected happened.
			price = ''
	else:
		# When there is no rate plan data (eg, it couldn't be determined)
		price = ''

	# Update list and write to file
	row[1] = price

# Write the modified file
write_file(input_file, "slcsp_modified.csv")

