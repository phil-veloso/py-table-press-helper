"""
Splits csv file into mutile files for importing to WP TablePress
"""

# Standard library imports
from pathlib import Path

import csv
from fuzzywuzzy import fuzz

from zipfile import ZipFile 
import os 
#----------------------------------------------------------------------

class TablePressHelper():
	
	DEBUG 			= True
	SUFFIX			= "-Email-2020-04-18"

	auto_ratio 		= 94
	check_ratio 	= 90

	def __init__(self):
		self.extract()
		
		user_input = input( "create zip, Y or N?" )
		reponse = user_input.lower()
		if reponse == "y":
			self.zip_files()

		
	def extract(self):
		# Loop log files
		for idx, file in enumerate( Path('input').glob('*.csv') ):
			
			# Get contents
			with open(file, mode='r') as csv_file:

				# settings
				csv_reader = csv.DictReader(csv_file)
				line_count = 0
				
				# loop rows
				for row in csv_reader:
					if self.DEBUG and line_count < 1:
						self.match_file( row )
						line_count += 1
					else:
						self.match_file( row )

	def match_file(self, row):
		
		list_name = list(row.values())[0].replace(",", "").replace(" &", "").replace(" ", "-")

		for idx, file in enumerate( Path('output').glob('*.csv') ):

			file_name = file.stem
			match_ratio = fuzz.ratio( file_name, list_name + self.SUFFIX )

			if  match_ratio >= self.auto_ratio:
				self.write_file( file, row )	
			elif match_ratio >= self.check_ratio:
				user_input = input( "{} confidence, that {} matches {}, Y or N?".format( match_ratio, file_name, list_name ))
				reponse = user_input.lower()
				if reponse == "y":
					self.write_file( file, row )

			
	def write_file(self, file, row):
					
		try:
			with open( file, 'w') as output:

				writer = csv.writer( output, delimiter="," )

				for (k,v) in enumerate(row): 
					
					if k == 0:
						# first element
						writer.writerow( [ "Region", "Count" ] )
					elif k == len(row) - 1:
						# last element
						writer.writerow( [ "Total", "=SUM(B2:B10)" ] )
					else:
						# middle elements
						key = list( row.values() )[k]
						writer.writerow( [ v, key ] )

		except IOError:
			print( "I/O error: {}".format( file.stem ) )
	

	def zip_files( self ):
		
		# define directory
		directory = './output'
		
		# initializing empty file paths list 
		file_paths = [] 
	
		# crawling through directory and subdirectories 
		for root, directories, files in os.walk(directory): 
			for filename in files: 
				# join the two strings in order to form the full filepath. 
				filepath = os.path.join(root, filename) 
				file_paths.append(filepath) 

		# printing the list of all files to be zipped 
		# print('Following files will be zipped:') 
		# for file_name in file_paths: 
		# 	print(file_name) 

		# writing files to a zipfile 
		with ZipFile('output.zip','w') as zip: 
			# writing each file one by one 
			for file in file_paths: 
				zip.write(file) 

		print('All files zipped successfully!')       


# End TablePressHelper Class
#----------------------------------------------------------------------		

if __name__ == '__main__':
	TablePressHelper()