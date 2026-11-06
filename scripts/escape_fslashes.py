with open("episodes.json", "r", encoding="utf-8") as fr:
	temp = []
	for line in fr.readlines():
		if "epsource" in line:
			line = line.replace("/", "\/")
		temp.append(line)
		
	with open("episodesnew.json", "w", encoding="utf-8") as fw:
		for line in temp:
			fw.write(line)