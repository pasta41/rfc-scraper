import sys
from subprocess import check_call
import pandas as pd
import re
from collections import defaultdict
import csv

# TODO more sophisticated parsing
if len(sys.argv) != 2:
	print("Error: Expected 1 word to map; got {}.".format(len(sys.argv) - 1))
	exit(1)

metadata_file = "../data/metadata.csv"
rfcs_dir = "../data/rfcs/"
word = sys.argv[1]

print("Performing RFC mapping for: {}".format(word))

# call grep bash script to match word, case insensitive, against rfcs
# with surrounding text
response = check_call(["./match.sh", word])
if response != 0:
	print("Error: Crashed running match.sh")
	exit(1)

# call grep bash script to match word, case insensitive, against rfcs
response = check_call(["./match_rfc.sh", word])
if response != 0:
	print("Error: Crashed running match_rfc.sh")
	exit(1)

# TODO better encapsulation...pass output path to match.sh
match_output_file = "../data/match/{}.txt".format(word)
match_output_html = "../data/match/{}.html".format(word)
print("Saved matched rfc paths list: {}".format(match_output_file))
print("Saved matches with surrounding text: {}".format(match_output_html))

print("Number of rfcs matched: ")

response = check_call(["./count_matches.sh", match_output_file])
if response != 0:
	print("Error: Crashed running count_matches.sh")
	exit(1)

print()

# do mapping

# open metadata csv as dataframe
metadata_df = pd.read_csv(metadata_file)
metadata_df.fillna('', inplace=True)
#print(metadata_df)

# read the matched rfcs path list
# match the 1-4 digit rfc id in the file name
regex = "\d{1,4}"
rfc_id_list = []
with open(match_output_file) as f:
    for index, line in enumerate(f):
    	rfc_match = re.findall(regex, line.strip())[0]
    	rfc_id_list.append(rfc_match)

# grab subset of metadata_df matching those rfc ids
matched_df = metadata_df[metadata_df['RFC_ID'].isin(rfc_id_list)]

matched_df.to_csv("../data/match/{}.csv".format(word), index = False)


# print list of unique authors matched

authors = defaultdict(int)

matched_df_authors = matched_df['Authors'].to_list()
for matched_author_list in matched_df_authors:
	a_s = matched_author_list.split(",")
	for a in a_s:
		authors[a] += 1

authors_output_file = "../data/match/{}_authors.csv".format(word)
print("Saved matched rfc author counts: {}".format(authors_output_file))
print("Unique authors: {}".format(len(authors.keys())))

with open(authors_output_file, 'w') as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(['Author', "RFC_Match_Count"])

    for key, value in authors.items():
       writer.writerow([key, value])
