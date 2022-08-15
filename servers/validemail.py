
# Python program to validate an Email 

# import re module 

# re module provides support 
# for regular expressions 
import re 

# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
	
# Define a function for 
# for validating an Email 
def check(email): 

	# pass the regualar expression 
	# and the string in search() method 
	if(re.search(regex,email)): 
		return "Valid Email"
		
	else: 
		return "Invalid Email"
	

