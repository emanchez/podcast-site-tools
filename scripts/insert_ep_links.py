import json
import glob

base = "../site_copy/"
webbase ="http://localhost:1234/ud/"
files = glob.glob(base + "ep_*.html")

def check_episode(num):
	for filename in files:
		comp = filename.split("_")[1]
		if num == comp:
			return filename
			
	return None



with open("episodesin.json", "r", encoding="utf-8") as fr:
	with open("episodes.json", "w") as fw:
		data = json.load(fr)
		for d in data:
			epfile = check_episode(d["@number"])
			#print(epfile)
			if (epfile != None):
				#print(webbase + "site_copy/" + epfile.split("\\")[-1])
				d['eplink'] = webbase + "site_copy/" + epfile.split("\\")[-1]
			else:
				#print(None)
				d['eplink'] = ""
		
		json.dump(data, fw)