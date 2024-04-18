# XML Message Parser  
This Python script is designed to parse XML files containing messages and extract specific information such as amounts, limits, credit card numbers, and locations. It then organizes this data into a CSV file for further analysis.  

# Dependencies  
xml.etree.ElementTree: Used for parsing XML files.  
re: Regular expression library for pattern matching.  
csv: Library for reading and writing CSV files.  
# Functions
`extract_amount(text)`: Extracts the amount from the text after the "EGP" word.   
`extract_limit(text)`: Extracts the limit amount from the text.  
`extract_credit_card_ending(text)`: Extracts the last four digits of the credit card number.  
`extract_location(text)`: Extracts the location from the text.  
`contains_star(input_string)`: Checks if a given string contains an asterisk.  
`extract_sublists(my_list, delimiter)`: Splits a list into sublists based on a delimiter.  
`add_the_hash_map_values(hashMap, listToAddOn)`: Adds values from a hash map to a list based on the keys.   
`extract_messages_from_xml(xml_path)`: Extracts messages from an XML file and returns them as a list.  
`remove_commas_in_the_list(the_list)`: Removes commas from a list of strings.  
`make_a_hash_map_for_the_data(list_of_messages)`: Creates a hash map for the extracted data.  
`fix_the_data()`: Combines all the data fixing functions to process the extracted messages.  
# Usage   
Replace xml_file_path with the path to your XML file.  
Run the script to generate a CSV file named transactions.csv containing the extracted data.__
