import xml.etree.ElementTree as ET
import re
import csv


def extract_amount(text):
    pattern = r"EGP\s+(\d+\.\d{2})"
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    pass


def extract_date_and_time(text):
    pattern = r"(\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[AP]M)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    pass

def extract_credit_card_ending(text):
    pattern = r"\* (\d{4}) has been used"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    pass
def extract_location(text):
    pattern = r"at (.+?)\."
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    pass

def extract_sublists(my_list, delimiter):
    # Find the indices of the delimiter elements
    delimiter_indices = [i for i, val in enumerate(my_list) if val == delimiter]

    # Create sublists between delimiter elements
    sublists = [my_list[delimiter_indices[i]+1:delimiter_indices[i+1]] for i in range(len(delimiter_indices)-1)]

    return sublists

# Path to your XML file
xml_file_path = "/home/kali/Desktop/all_python_files/qatar/download.xml"

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()
body_element = root.find('{http://schemas.microsoft.com/office/word/2003/wordml}body')
sect = body_element.find('{http://schemas.microsoft.com/office/word/2003/auxHint}sect')

tbls = sect.findall('{http://schemas.microsoft.com/office/word/2003/wordml}tbl')
print(tbls)

print("#")

trs = []
tcs = []
ps = []
rs = []
ts = []

for tbl in tbls:
    trs_to_append = tbl.findall("{http://schemas.microsoft.com/office/word/2003/wordml}tr")

    for tc in trs_to_append:
        tcs_to_append = tc.findall("{http://schemas.microsoft.com/office/word/2003/wordml}tc")

        for p in tcs_to_append:
            ps_to_append = p.findall("{http://schemas.microsoft.com/office/word/2003/wordml}p")

            for r in ps_to_append:
                rs_to_append = r.findall("{http://schemas.microsoft.com/office/word/2003/wordml}r")

                for t in rs_to_append:
                    ts_to_append = t.findall("{http://schemas.microsoft.com/office/word/2003/wordml}t")
                    for i in ts_to_append: ts.append(i.text)

for i in range(17):
    ts.remove("From HSBC: Your Credit Card ending with")
# for text in ts:
#     print(extract_amount(text))
#     print(extract_date_and_time(text))
#     print(extract_credit_card_ending(text))
#     print(extract_location(text))
                    
logs = extract_sublists(ts, "Received")

counter = 0
for transaction in logs:
    for i in transaction:

        if extract_amount(str(i)):
            logs[counter].append(extract_amount(str(i)))

        else: pass

        if extract_location(str(i)):
            logs[counter].append(extract_location(str(i)))

        else: logs[counter].append(None)
    counter += 1
    


with open('transactions.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(logs)
