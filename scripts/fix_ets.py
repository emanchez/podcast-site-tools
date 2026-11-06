with open("ets_new.txt", "r", encoding="utf-8") as fr:
	with open("ets_newv2.txt","w",encoding="utf-8") as fw:
		for line in fr.readlines():
			temp = line.split("\t")
			temp[1] = temp[1].replace("https://html5-player.libsyn.com", "")
			fw.write(temp[0] +"\t"+ temp[1])