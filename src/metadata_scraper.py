import requests
import csv

base_URL = 'https://www.rfc-editor.org/rfc-index.html'


data_dir = "../data/"

page = requests.get(base_URL, allow_redirects=True)
if page.status_code == 200:
	# store
	open("rfc_metadata.txt", 'wb').write(page.content)
else:
	print("Error: Status Code: {}".format(page.status_code))

# each RFC is in a tr element; but grabbing td
# helps cut off link
rfcs = str(page.content).split("<tr valign=\"top\">")

with open("../data/metadata.csv", "w", encoding='utf-8') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(['RFC_ID', 'Title', 'Authors', 'Date', 'Status', 'Stream', "Area", "Working_Group"])

	for rfc in rfcs:
		# otherwise, not issued
		if "<b>" in rfc and "JavaScript" not in rfc:
			prefix, remainder = rfc.split("</b>", 1)
			prefix = prefix.split("<b>")
			title = prefix[1].strip()
			rfc_number = int(prefix[0].split("</noscript>")[0].split("<noscript>")[1])
			authors, remainder = remainder.split("[", 1)
			# i hate python
			authors = authors.split("\\n")[0].strip()
			date, remainder = remainder.split("]", 1)
			date = date.strip()

			# Not grabbing obselescene info; just status, stream, area,
			# working group
			_, remainder = remainder.split("Status:")
			status, remainder = remainder.split(")", 1)
			status = status.strip()

			_, remainder = remainder.split("Stream: ")
			stream = remainder.split(",", 1)[0]
			if ")" in stream:
				stream = stream.split(")")[0].strip()

			area = ""
			if "Area" in remainder:
				_, remainder = remainder.split("Area:")
				area = remainder.split(",", 1)[0].strip()
				if ")" in area:
					area = area.split(")")[0].strip()
			
			wg = "" # always last in the tuple
			if "WG" in remainder:
				_, remainder = remainder.split("WG:")
				wg = remainder.split(")", 1)[0].strip()

			writer.writerow([rfc_number, title, authors, date, status, stream, area, wg])
