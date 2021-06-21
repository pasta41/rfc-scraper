import requests

base_URL = 'https://www.rfc-editor.org/rfc/rfc'


# Change max RFC number by checking the website; it is unstable
# javascript and not worth scraping
rfc_max = 9085

data_dir = "../data/rfc/"

for i in range(9085, rfc_max + 1):
	rfc = "{}.txt".format(i)
	page = requests.get(base_URL + rfc, allow_redirects=True)
	if page.status_code == 200:
		open("{}rfc{}".format(data_dir, rfc), 'wb').write(page.content)
	elif page.status_code == 404:
		print("Error: RFC {} not found".format(i))
	else:
		print("Error: RFC {}; Status Code: {}".format(i, page.status_code))
