import json
import os

base = "site_copy/"
picdir = "pix/"

with open(base + "episodes.json", "r", encoding="utf-8") as fr:
	x = fr.read().replace("\n", "");
	
	jsondata = json.loads(x)
	
	for j in jsondata:
		if not os.path.exists(base + picdir + j["imagepath"]):
			print(j["@number"])