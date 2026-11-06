import xml.etree.cElementTree as ET

lines = []

with open("ordered_episodes.txt", "r", encoding="utf-8") as f:
	for line in f:
		lines.append(line.split("\t"))
		

root = ET.Element("root")

count = 0
for line in lines:
	#print(len(line))
	sub = ET.SubElement(root, "episode", number=str(count))
	ET.SubElement(sub, "name").text = line[0]
	ET.SubElement(sub, "title").text = line[1]
	ET.SubElement(sub, "description").text = line[2]
	ET.SubElement(sub, "imagepath").text = line[0].split(" ")[0] + ".jpg"
	count += 1
	
tree = ET.ElementTree(root)
tree.write("episodes.xml")