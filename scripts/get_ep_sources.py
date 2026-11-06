import glob
from bs4 import BeautifulSoup as bs

dir = "site_copy"

all_files = glob.glob(dir + "/ep_*.html")

eps = []

with open("ep_to_src.txt", "w", encoding="utf-8") as fw:
	for filepath in all_files:
		txt = ""
		with open(filepath, "r", encoding="utf-8") as fr:
			txt = fr.read()
			
		ep_no = filepath.split("_")[1]
		eps.append(ep_no)
		soup = bs(txt)
		element = soup.body.find("iframe")
		fw.write(ep_no +"\t"+ element["src"] + "\n")



for i in range(0, 74):
	if str(i) not in eps:
		print(str(i) + " not found")
	