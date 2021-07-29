import pandas as pd
import csv

# TODO refactor this into a function and use in mapper

filename = "../data/rfcs_filtered.txt"
rfc_id_list = open(filename).read().splitlines()

# open metadata csv as dataframe
metadata_file = "../data/metadata.csv"
metadata_df = pd.read_csv(metadata_file)
metadata_df.fillna('', inplace=True)

matched_df = metadata_df[metadata_df['RFC_ID'].isin(rfc_id_list)]

# save subsetted metadata df; TODO refactor
matched_df.to_csv("../data/rfcs_filtered_metadata.csv", index=False, encoding='utf-8')

matched_df_wgs = matched_df[['RFC_ID', 'Working_Group']]
wgs = set(filter(None, matched_df_wgs["Working_Group"].to_list()))

wgs_output_file = "../data/match/wgs_survivab_account_filtered.csv"

with open(wgs_output_file, 'w') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(['Working_Group', "RFC_Match_Count", "Matched_RFC_IDs"])

	for wg in wgs:
		matches_for_wg = matched_df_wgs[matched_df_wgs["Working_Group"] == wg]
		rfcs_for_wg = matches_for_wg["RFC_ID"].to_list()
		writer.writerow([wg, len(rfcs_for_wg), ','.join([str(i) for i in rfcs_for_wg])])

print("Saved matched rfcs by working group and counts: {}".format(wgs_output_file))
print("Unique working groups: {}".format(len(wgs)))
