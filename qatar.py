import xml.etree.ElementTree as ET
import re
import csv


def extract_amount(text):
    pattern = r"EGP\s+(\d+\.\d{2})"
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    else: return False

def extract_limit(text):
    regex = r"limit is EGP ([0-9.]+)"
    match = re.search(regex, text)
    if match:
        return float(match.group(1))
    return None

def extract_date_and_time(text):
    pattern = r"(\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[AP]M)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    
    else: return False

def extract_credit_card_ending(text):
    pattern = r"\* (\d{4}) has been used"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else : return False

def extract_location(text):
    pattern = r"at (.+?)\."
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else: return False

def contains_star(input_string):
    return '*' in input_string

def extract_sublists(my_list, delimiter):
    # Find the indices of the delimiter elements
    delimiter_indices = [i for i, val in enumerate(my_list) if val == delimiter]

    # Create sublists between delimiter elements
    sublists = [my_list[delimiter_indices[i]+1:delimiter_indices[i+1]] for i in range(len(delimiter_indices)-1)]

    return sublists

xml_file_path = "/home/kali/Desktop/all_python_files/qatar/download.xml"

def add_the_hash_map_values(hashMap, listToAddOn:list):
    for key, value in hashMap.items():
        amount = value['amount']
        limit = value['limit']
        place = value['place']
        credit_card_number = value['credit card number']

        listToAddOn[key].append(amount)
        listToAddOn[key].append(limit)
        listToAddOn[key].append(place)
        listToAddOn[key].append(credit_card_number)

def extract_messages_from_xml(xml_path):
    # Path to your XML file

    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    body_element = root.find('{http://schemas.microsoft.com/office/word/2003/wordml}body')
    sect = body_element.find('{http://schemas.microsoft.com/office/word/2003/auxHint}sect')
    tbls = sect.findall('{http://schemas.microsoft.com/office/word/2003/wordml}tbl')

    messages_data = []

    for MasterGrandFather in tbls:
        MGF_to_append = MasterGrandFather.findall("{http://schemas.microsoft.com/office/word/2003/wordml}tr")

        for GrandFather in MGF_to_append:
            GF_to_append = GrandFather.findall("{http://schemas.microsoft.com/office/word/2003/wordml}tc")

            for Paerent in GF_to_append:
                Paerents_to_append = Paerent.findall("{http://schemas.microsoft.com/office/word/2003/wordml}p")

                for Child in Paerents_to_append:
                    Childs_to_append = Child.findall("{http://schemas.microsoft.com/office/word/2003/wordml}r")

                    for Kid in Childs_to_append:
                        Kids_to_append = Kid.findall("{http://schemas.microsoft.com/office/word/2003/wordml}t")
                        for i in Kids_to_append: messages_data.append(i.text)

    return messages_data

messages_data = extract_messages_from_xml(xml_file_path)

def replace_commas_in_the_list(the_list):
    the_new_list = []
    for i in the_list:
        old = str(i)
        new = old.replace(",", "")
        the_new_list.append(new)

    return the_new_list

def make_a_hash_map_for_the_data(list_of_messages):
    
    hash_map = {}
    for j in list_of_messages:
        for i in j:
            if contains_star(i):
                hash_map[list_of_messages.index(j)] = {"amount": None, "credit card number": None, "place": None, "limit":None}

                amount = extract_amount(i)
                if amount:
                    hash_map[list_of_messages.index(j)]['amount'] = amount
        
                
                place = extract_location(i)
                if place:
                    hash_map[list_of_messages.index(j)]['place'] = place

                Credit_card_number = extract_credit_card_ending(i)
                if Credit_card_number:
                    hash_map[list_of_messages.index(j)]['credit card number'] = Credit_card_number

                limit = extract_limit(i)
                if limit:
                    hash_map[list_of_messages.index(j)]['limit'] = limit

            else: pass
    return hash_map

def fix_the_data():

    mylist = [item for item in messages_data if item != "From HSBC: Your Credit Card ending with"]
    mylist_without_commas = replace_commas_in_the_list(mylist)
    logs = extract_sublists(mylist_without_commas, "Received")

    hash_map = make_a_hash_map_for_the_data(logs)

    add_the_hash_map_values(hash_map, logs)
    return logs
    

with open('transactions.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(fix_the_data())
