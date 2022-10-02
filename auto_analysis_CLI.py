'''
CLI interface for auto_analysis.py script

A friendly user interface through terminal to run the script
'''
########################################################################################################################################
# File Attributes
__all__ = []
__author__ = 'AbdulRahman Mohsen'
__version__ = '0.1.0'

########################################################################################################################################



#######################################################################################################
#### CONSTANTS

PATH_TO_SCRIPT = 'internals/main/'
#######################################################################################################



#######################################################################################################
#### imports

# importing standard library modules
import pickle
from dataclasses import dataclass
from typing import List, Tuple, Dict
import os
from pathlib import Path
from time import sleep
import shutil
import importlib

# importing git, it's essential to import main library if it's not there
try:
	import git
	from git import Repo
except ModuleNotFoundError:
	os.system('pip3 install GitPython')
	import git
	from git import Repo

# Main script import form GitHub
main_script_imported_through_function = False
first_time = False
def import_main_script():
	'''
	1- Decides if we need to clone or pull
	2- git clone into 'internals/git_cloned' (or pulls it)
	3- replaces the file in the same directory with the new one
	4- imports it
	'''

	# Check if repo is there, then clone OR pull
	if os.path.exists(PATH_TO_SCRIPT):
		
		# pull newest version from github
		g = git.cmd.Git(PATH_TO_SCRIPT)
		g.pull()

		# reloading the main script
		importlib.reload(auto_analysis)
		
	else:
		# clone repo for the first time
		Repo.clone_from('https://github.com/ambadran/Valeo-Auto-Analyzer.git', PATH_TO_SCRIPT)

		global first_time
		first_time = True


	# Display latest change Done
	last = next(Repo(PATH_TO_SCRIPT).iter_commits())
	message = last.message[:last.message.find('Change-Id')].strip()
	print(f"Latest Commit message: {message}\nLatest Commit Date and Time: {last.committed_datetime}")

	# setting the flag
	global main_script_imported_through_function
	main_script_imported_through_function = True

# importing the main script itself
try:  
	import internals.main.src.main_pkg.auto_analysis as auto_analysis
except ModuleNotFoundError:
	try:
		print("auto_analysis.py not found, Trying to Import it from github")
		import_main_script()
		print("Successfully Imported the Latest Version of the script!\n\n")

		if first_time:
			# importing the new script :)
			import internals.main.src.main_pkg.auto_analysis as auto_analysis

		sleep(1)
	except ModuleNotFoundError:
		print('Failed to import it from github!')
		raise ModuleNotFoundError("\nThe main script 'auto_analysis.py' is not found by CLI!\nCheck availability in the same folder and spelling.")

# importing 3rd party library modules
try:
	import pyfiglet
except ModuleNotFoundError:
	print("\n\n Module 'pyfiglet' not installed, Commencing the installation!\n\n")
	os.system('pip3 install pyfiglet')
	print("\n Done Installing 'pyfiglet' module!\n")
	import pyfiglet

#######################################################################################################



#######################################################################################################
##### Definitions #####

# Storage for long texts
@dataclass
class text:
	welcome_banner = pyfiglet.figlet_format(f"Valeo Auto Analyzer\nV {auto_analysis.__version__}")

	intro = f"""IMPORTANT ASPECTS TO LOOK OUT FOR:
	1- Make sure that you activated the correct branch the script is meant to analyze for
	2- Make sure that path to REPORT is passed where the last folder has "Release" and "Rolling Build" folders
	3- Make sure that the ID of the found component matches the ID of the component wanted
	4- Make sure the correct path(s) to code is passed
	5- Make sure to filter comments analysis table as there will always be undecided comments outputed from the script
	that does need human intervention to decide their severity

IMPORTANT ASPECTS THAT WILL GAURANTEE SCRIPT MALFUNCTION
	1- Moving the file from its original place to anywhere else
	2- Changing the paths of any of the passed paths without updating in the CLI
	"""
	first_time_intro = f"""#################################### Introduction ##############################################
This is the first time the script runs therefore PLEASE make sure the following is achieved:
	1- Read the next carefully, they are descriptive and very important to follow precise for the script to run properly
	2- Make sure you've put 'auto_analysis.py' and 'CLI.py' in an empty folder before running otherwise delete the generated folder

Script Brief:{auto_analysis.__doc__}

IMPORTANT ASPECTS TO LOOK OUT FOR:
	1- Make sure that you activated the correct branch the script is meant to analyze for
	2- Make sure that path to REPORT is passed where the last folder has "Release" and "Rolling Build" folders
	3- Make sure that the ID of the found component matches the ID of the component wanted
	4- Make sure the correct path(s) to code is passed
	5- Make sure to filter comments analysis table as there will always be undecided comments outputed from the script
	that does need human intervention to decide their severity

IMPORTANT ASPECTS THAT WILL GAURANTEE SCRIPT MALFUNCTION
	1- Moving the file from its original place to anywhere else
	2- Changing the paths of any of the passed paths without updating in the CLI
################################################################################################
"""

class Memory:
	'''
	This class is responsible to deal with anything related to saving or reading program internal memory
	The memory is a pickle file which saves the memory object called everytime the .py file runs
	'''
	def __init__(self):

		#  checking to see if it's the first time
		try:
			f = open('internals/pickle.pkl', 'r')
			f.close()
		
		except FileNotFoundError:  # dealing with first time runs
			
			
			print("first time run")
			print('creating folders')
			self.exec_first_time_stuff()

			self.is_first_time = True
			self.num_runs = 1
			self._paths = {}
			self.paths = {}

			return None  # stop init function here

		########### Initiating a memory object not run for first time ##############
		# loading memory
		self.load_memory()

		self.num_runs = self.num_runs+1

	def load_memory(self):
		with open('internals/pickle.pkl', 'rb') as pkl:
			loaded = pickle.load(pkl)
			self.__dict__.update(loaded)

	def exec_first_time_stuff(self):
		'''
		1- Create input folder
		2- Create pickle folder and file
		3- create output folder
		4- create logging folder and file
		'''
		Path(f"input_files/polarian_csv_outputs/").mkdir(parents=True, exist_ok=True)

		Path(f"input_files/reports/").mkdir(parents=True, exist_ok=True)

		Path(f"input_files/reports/").mkdir(parents=True, exist_ok=True)

		Path(f"internals/").mkdir(parents=True, exist_ok=True)
		os.system('attrib +h internals')
		
		Path(f"output/").mkdir(parents=True, exist_ok=True)
		
		Path(f"logging/").mkdir(parents=True, exist_ok=True)

	def get_found_memory_text(self, name: str, detected_memory: str, memory_type_text: str) -> str:
		'''
		return the text that should be printed to the user when memory found
		'''
		memory_type_text_capital = memory_type_text.replace("_", " ").capitalize()
		memory_type_text = memory_type_text.replace("_", " ")

		return f"""{memory_type_text_capital} to {name.replace("_", " ")} detected in memory:\n{detected_memory}

			If you want to change the {memory_type_text.replace("_", " ")} permenantly press 'c'.
			If you want to change the {memory_type_text.replace("_", " ")} temporary press 't'.
			Otherwise, press enter: """

	def get_not_found_memory_text(self, name: str, memory_type_text: str) -> str:
		'''
		return the text that should be printed to the user when memory NOT found
		'''
		memory_type_text = memory_type_text.replace("_", " ").capitalize()
		return f"{memory_type_text} to {name} folder not found in memory."

	def __str__(self):
		'''
		return object.__dict__ as string
		'''
		return str(self.__dict__)

	############################################################################################
	### Memory attributes
	@property
	def is_first_time(self):
		is_first_time = self._is_first_time
		return is_first_time

	@is_first_time.setter
	def is_first_time(self, value):
		self._is_first_time = value
		with open('internals/pickle.pkl', 'wb') as pkl:
			pickle.dump(self.__dict__, pkl)

	@property
	def num_runs(self):
		num_runs = self._num_runs
		return num_runs

	@num_runs.setter
	def num_runs(self, value):
		self._num_runs = value
		with open('internals/pickle.pkl', 'wb') as pkl:
			pickle.dump(self.__dict__, pkl)

	@property
	def paths(self) -> dict:
		paths = self._paths
		return paths

	@paths.setter
	def paths(self, path: dict) -> None:
		self._paths.update(path)
		with open('internals/pickle.pkl', 'wb') as pkl:
			pickle.dump(self.__dict__, pkl)
	############################################################################################

class UserInput:
	'''
	Manages all inputs needed to run the script
	'''
	def __init__(self):
		'''
		runs all input gathering methods and assigns attributes
		Object meant to be passed to execute_script() function
		'''

		# Polarian CSV files
		self.read_process_polarian_csv_files()

		self.paths = {}

		# Code files path
		self.paths_to_code = self.get_memory('code', 'path', memory_is_list=True)

		# report files path
		self.path_to_reports = self.get_memory('reports', 'path', memory_is_list=False)

		# tcc path
		self.path_to_tcc = self.get_memory('tcc', 'path', memory_is_list=False)

		# My Polarian web page link
		self.my_polarian_web_page = self.get_memory('my_polarian_web_page', 'web_page_link', memory_is_list=False)

		# Variant of component
		self.variant = self.get_variant()

		# branch of component
		self.branch = self.get_branch()

		# components to be worked on
		self.components = self.get_and_validate_components(self.branch)

		# make google sheet or not
		self.make_google_sheets = self.get_make_google_sheets_stat()

	def read_process_polarian_csv_files(self) -> None:
		'''
		Reads and Assigns all_object class variable in all Polarian workitems
			- reads all csv files
			- create workitem objects for everything
			- assign all workitem objects in the respective class variable cls.all_objects
		'''
		# Polarian csv files
		if not memory.is_first_time:
			print("Reading all CSVs...")
			all_ = auto_analysis.read_assign_all_CSVs()
			print("\nDone Reading and parsing all CSVs\n\n")

		else:
			k = input("Please input the 4 csv files into the folders then press Enter..")
			print("Reading all csvs")
			all_ = auto_analysis.read_assign_all_CSVs()

	def get_memory_value_from_user(self, memory_is_list) -> List[str]:
		'''
		Called when reassigning of path from user is required
		returns list of paths to code inputed by user
		'''
		print()
		
		if not memory_is_list:
			path = input("Please enter path: ").strip('. ')
			while path == '':
				path = input("Nothing was inputed, Please enter path: ").strip('. ')
			output = path

		else:
			output = []
			path = input("Please enter path (or enter q to stop): ").strip('. ')
			while path != 'q':
				if path != '':
					output.append(path)
				path = input("Please enter path (or enter q to stop): ").strip('. ')


		print(f"Path(s) inputed: {output}\n")

		return output

	def get_memory(self, name: str, memory_type_text: str, memory_is_list: bool) -> List[str]:
		'''
		Implements Logic of whether to use path saved in memory or get it again from user, etc..

		:param func_to_run: function to run after reading memory, could be any function
		'''
		paths = {}
		try:
			if memory_is_list:
				detected_memory = "\n".join(memory.paths[name])
			else:
				detected_memory = memory.paths[name]

			q = input(memory.get_found_memory_text(name, detected_memory, memory_type_text))
			if q == 'c':
				self.paths[name] = self.get_memory_value_from_user(memory_is_list)
				memory.paths = self.paths
			elif q == 't':
				self.paths[name] = self.get_memory_value_from_user(memory_is_list)
			else:
				self.paths[name] = memory.paths[name]

			print()

		except KeyError:  # first time
			print(memory.get_not_found_memory_text(name, memory_type_text))
			paths[name] = self.get_memory_value_from_user(memory_is_list)
			self.paths[name] = paths[name]
			memory.paths = paths

			# finished first time stuff
			memory.is_first_time = False

		return self.paths[name]

	def get_variant(self) -> str:
		'''
		Searching for all possible variants in the components list then letter the user choose one of them
		'''
		components = list(auto_analysis.Component.all_objects.values())

		all_variants = []
		for comp in components:
			all_variants.extend(comp.variant)

		possible_variants = []
		for var in all_variants:
			if var not in possible_variants:
				possible_variants.append(var)


		### Filters
		# filtering variant that only occured once
		possible_variants = [var for var in possible_variants if all_variants.count(var) > 1]

		# filtering '' variants
		possible_variants = [obj for obj in possible_variants if obj != '']

		# filtering enteries that are same but have different capital letters
		possible_variants = list(set([var.lower().strip() for var in possible_variants]))

		### Getting the variant from the user
		print(f"All the possible variant for components in the Components csv file are:\n{possible_variants}")
		variant = input("Please enter the name of one of them: ").lower().strip()
		while variant not in possible_variants:
			variant = input(f"Invalid input!\nValid variants: {possible_variants}\nPlease choose one of them: ").lower().strip()

		return variant

	def get_branch(self) -> str:
		'''
		#TODO: searches for all possible branches
		#TODO: let user choose from one of them
		#TODO: Activates the branch choosen by user, somehow ;)
		:return: choosen branch
		'''
		branch = input(f'Please input branch: ').strip().capitalize()

		return branch

	def get_component_name(self) -> str:
		'''
		return input from user of component name
		makes sure component name is valid:
							- not ''
		'''
		component_name = input("\nPlease enter Component name: ").strip()

		#### validating correct name
		# not empty
		while component_name == '':
			print("You Didn't enter any component Name, Please Try again!")
			component_name = input("\nPlease enter Component name: ").strip()

		# has a wrong character
		unwanted_characters = [' ', '%', '(']
		for char in unwanted_characters:
			while char in component_name:
				print("Detected a wrong character in the component name")
				component_name = input("\nPlease enter Component name: ").strip()

		#### Filters
		# .c filter
		if '.c' in component_name:
			component_name = component_name[:component_name.index('.c')]

		return component_name

	def get_CAT_num(self) -> int:
		'''
		return input from user of CAT_num
		makes sure CAT_num is valid:
							- can be casted into an int type
							- range is from 1 to 3 inclusive
		'''
		CAT_num = input("Please input CAT number: ").strip()

		#### validating correct CAT number
		# check if it's an int
		while not CAT_num.isdigit():
			print("Wrong Input! CAT_num must be an integer")
			CAT_num = input("Please input CAT number: ").strip()
		
		CAT_num = int(CAT_num)  # now we are sure CAT_num string contains integer, so we can cast successfully

		# checking if CAT_num is within range
		MAX_CAT_num = 3
		MIN_CAT_num = 1
		while CAT_num < MIN_CAT_num or CAT_num > MAX_CAT_num:
			print(f"Wrong Input! CAT number must be within {MIN_CAT_num-1} < CAT number < {MAX_CAT_num-1}")
			CAT_num = int(input("Please input CAT number: ").strip())

		return CAT_num

	def validate_component(self, component_name: str, CAT_num: int) -> auto_analysis.Component:
		'''
		calls Component.get_component
		deals with components not found by giving the user another chance to
				1- rewrite the name of the component
				2- or change it's CAT number to 3 so that this step could be bypassed
		'''
		print(f"Finding Component: {component_name} in Polarian\n")

		def recurse(component_name):
			try:
				wanted_component = auto_analysis.Component.get_component(component_name, CAT_num, self.branch)
			except LookupError:
				print("Didn't find this component in Polarian\n")
				print("You have 2 Options:")
				print("1- Enter '3' to change CAT number and bypass finding in polarian step.")
				print("2- Just Press Enter to re-enter the component name again (if you think it could be a spelling mistake).")
				
				choice = input("Enter you choice: ").strip()
				if choice == '3':
					wanted_component = auto_analysis.Component.get_component(component_name, 3, self.branch)
				else:
					component_name = self.get_component_name()
					wanted_component = recurse(component_name)

			return wanted_component

		wanted_component = recurse(component_name)

		if wanted_component.found_in_polarian:
			print(f"Found Component: {wanted_component.true_title} in Polarian!\n")

		return wanted_component

	def get_and_validate_components(self, branch) -> List[auto_analysis.Component]:
		'''
		Process
			- gets input form user of component name and CAT number
			- checks for it in Component.all_objects
			- assigns CAT_num attribute to Component
			- repeat if user wants
			- return list of components
		:return: list of Component Objects with CAT_num attribute
		'''

		######### First Entry
		# Input first component
		component_name = self.get_component_name()
		CAT_num = self.get_CAT_num()
		# validate first component
		wanted_components = [self.validate_component(component_name, CAT_num)]

		######## Algorithm to get and validate other components, Other Entries
		q = input("Do you want to Enter another component with same variant and branch? (y/n): ").lower()
		while q != 'n':

			if q == 'y':  # User wants to input another component
				
				# Input another component
				component_name = self.get_component_name()
				CAT_num = self.get_CAT_num()
				# validate another component
				wanted_components.append(self.validate_component(component_name, CAT_num))
				
			else:  # Wrong input from user, q should be 'y' or 'n' only
				print("Wrong input")
			
			q = input("Do you want to Enter another component with same variant and branch? (y/n): ").lower()

		return wanted_components

	def get_make_google_sheets_stat(self) -> bool:
		'''
		Asks if user wants to make google sheet or not

		If yes then it will make sure the necessary inputs for making google sheet is okay,
			1- validating and assign polarian web page link class variable to WorkItem class
			2- copies json file form src/ to script homedir
		'''
		print()
		make_google_sheets = input("Do you want to create Google Sheets for all entered Components? (y/n): ").strip().lower()

		#### validating answer
		while make_google_sheets != 'y' and make_google_sheets != 'n':
			print('Invalid Answer!')
			make_google_sheets = input("Do you want to create Google Sheet? (y/n): ").strip()

		result_mapping = {'y': True, 'n': False}

		result = result_mapping[make_google_sheets]

		if result:
			#### preparing for google sheet

			# assigning polarian web page base link
			auto_analysis.WorkItem.assign_validate_polarian_link(self.my_polarian_web_page)

			### copy and paste checklist.json to script internal files
			# copying	
			with open('internals/main/src/main_pkg/json_files/checklist_sheet.json', 'r') as file:
				loaded = file.read()

			# pasting
			Path(auto_analysis.GoogleSheet.path_to_json_files).mkdir(parents=True, exist_ok=True)
			with open(auto_analysis.GoogleSheet.path_to_json_files+ 'checklist_sheet.json', 'w') as file:
				file.write(loaded)

			path_to_token_json = auto_analysis.GoogleSheet.path_to_json_files + 'token.json'
			if not os.path.exists(path_to_token_json):
				k = input("'token.json' not found in json files, Please input it....")

		return result

	def __str__(self):
		'''
		return string __dict__
		'''
		return str(self.__dict__)

def interactive_intro():
	'''
	An interactive  introductory function that should help users understand the script more
	'''
	# The beautiful banner :)
	print(text.welcome_banner)

	# Ask user if he wants to update
	if not main_script_imported_through_function:  # making sure the script wasn't already pulled or cloned
		q = input("Do you want to update main package (y/n): ")
		while q != 'n':
			if q == 'y':
				import_main_script()
				print("Main Script updated!\n\n")
				break
			else:
				print("Invalid Answer!")
				q = input("Do you want to update main package (y/n): ")

	else:
		sleep(2)

	if not memory.is_first_time:
		print(text.intro)
	else:
		print(text.first_time_intro)
		memory.exec_first_time_stuff()

	q = input("Enter 'i' for more Information abou this script, else press enter: ")

	if q == 'i':
		print('\n\n')
		print(text.first_time_intro)

	k = input("Press to start analysing!")
	print('\n')

def execute_script(user_input: UserInput) -> List[auto_analysis.BlockTemplate]:
	'''
	Function to Execute the script, aka- call create_blocks() for every inputed component
	
	:user_input: UserInput object that contains all the necessary inputs to run the script successfully
	:return: list of blocks for every inputed component
	'''
	list_of_blocks = []
	for wanted_component in user_input.components:
		
		### Analysing the component
		print(f"Starting analysis for {wanted_component.title} of variant {wanted_component.variant} of ID {wanted_component.ID}\nand Document name '{wanted_component.document}'\n\n")
		blocks = auto_analysis.create_blocks(wanted_component, user_input.variant, user_input.branch, user_input.paths_to_code, user_input.path_to_reports, user_input.path_to_tcc, user_input.my_polarian_web_page)
		print('\nAnalysis is Completed Successfully!!!\n')

		list_of_blocks.append(blocks)

	return list_of_blocks

def export_csv(list_of_blocks, user_input):
	'''
	exporting analysis blocks results as CSV files
	'''

	### Export outputs as CSVs
	for blocks in list_of_blocks:
		auto_analysis.export_csv(blocks)


	if not user_input.make_google_sheets:

		print("\n\nDone Analysing: \n")

		for ind, comp in enumerate(user_input.components):
			print(f"{ind+1}- {comp.true_title}")

def export_GoogleSheet(list_of_blocks, user_input):
	'''
	export analysis blocks result as Google Sheet
	'''
	if user_input.make_google_sheets:
		links = []

		# Export output in a Google Sheet
		for blocks in list_of_blocks:
			google_sheet = auto_analysis.GoogleSheet(blocks)
			google_sheet.save_link_in_txt_file()
			links.append(google_sheet.link)		

		print("\n\nDone Analysing: \n")

		for ind, comp in enumerate(user_input.components):
			print(f"{ind+1}- {comp.true_title} - {links[ind]}")

#######################################################################################################



#######################################################################################################
if __name__ == '__main__':

	# Recalling memory!
	global memory
	memory = Memory()

	# Introduction
	interactive_intro()

	# set current working directory
	auto_analysis.set_wanted_directory(os.getcwd())

	# Get user inputs!
	user_input = UserInput()

	# Execute the Script!
	list_of_blocks = execute_script(user_input)

	# exporting CSV files
	export_csv(list_of_blocks, user_input)

	# exporting google sheets
	export_GoogleSheet(list_of_blocks, user_input)

	# Done!
	input("\nPress to End.")
#######################################################################################################
