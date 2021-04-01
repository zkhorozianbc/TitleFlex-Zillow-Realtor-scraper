from TitleFlex import TitleFlex
from FirefoxDriver import FirefoxDriver
import sys
import json
import argparse

def write_property_data_to_file(property_data,filename="property_data.json"):

	#creates json file from property_data dict and 
	#saves in current directory
	with open(filename, 'w') as f:
		json.dump(property_data, f, indent=4, sort_keys=True)

def main(args):

	#parse address from command line, throw error if none provided
	address = " ".join(args.address)

	## Firefox Webdriver with custom settings 
	driver = FirefoxDriver().get_driver()

	##create titleflex object
	titleflex = TitleFlex(driver)

	##Get property data from titleflex, zillow, realtor
	property_data = titleflex.get_property_data(address)

	#write property_data dict to property_data.json
	write_property_data_to_file(property_data)

	#close driver
	driver.close()
	

#Get address from sys args 
if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument(
	    "--address",
		"-a",
	    type=str,
	    help="Address to search",
	    nargs="+",
	    required=True
	)
	parser.add_argument(
	    "--verbose",
		"-v",
	    help="Print verbose logs",
	    action='store_true'
	)
	
	args = parser.parse_args()

	main(args)
