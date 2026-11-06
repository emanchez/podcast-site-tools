import xml.etree.cElementTree as ET

ep_dict = {}
with open("ets_newv2.txt", "r", encoding="utf-8") as fr:
	for line in fr.readlines():
		line_list = line.split("\t")
		ep_dict[line_list[0]] = line_list[1]
		

tree = ET.parse("episodes.xml")
root = tree.getroot()
for elem in root.findall("episode"):
	ep_no = elem.attrib["number"]
	sub = ET.SubElement(elem, "epsource")
	sub.text = ep_dict[ep_no].replace("\n", "")

tree.write("output.xml")