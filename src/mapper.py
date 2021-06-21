import sys
from subprocess import check_call
import pandas as pd
import re

# TODO more sophisticated parsing
if len(sys.argv) != 2:
	print("Error: Expected 1 word to map; got {}.".format(len(sys.argv) - 1))
	exit(1)

metadata_file = "../data/metadata.csv"
rfcs_dir = "../data/rfcs/"
word = sys.argv[1]

print("Performing RFC mapping for: {}".format(word))

# call grep bash script to match word, case insensitive, against rfcs
response = check_call(["./match.sh", word])
if response != 0:
	print("Error: Crashed running match.sh")
	exit(1)

# TODO better encapsulation...pass output path to match.sh
match_output_file = "../data/match/{}.txt".format(word)
print("Saved matched rfc paths list: {}".format(match_output_file))

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
    	