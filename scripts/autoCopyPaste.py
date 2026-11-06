
from bs4 import BeautifulSoup as soup
import requests
import glob
			
if __name__ == "__main__":
		
	dir = "site_copy"

	all_files = glob.glob("../" + dir + "/ep_*.html")
	for file in all_files:
		with open(file, "rb") as fr:
			with open("eps_donate_trial2/" + file.split("\\")[1], "w", encoding="utf-8") as fw:
				bs = soup(fr.read()) #initialize BeautifulSoup 4 with html code
				
				
				# ANIMATED DONATE BUTTON INJECTION
				new_a = bs.new_tag("a", href="https://payments.example/donate") # create new anchor with link
				new_a["id"] = 'donate-btn' # add id to anchor
				new_a.string = "DONATE" # add inner HTML to anchor
				
				new_li = bs.new_tag("li", role='presentation') # create new list item
				new_li["id"] = "anim-btn" # add id to list item
				
				new_li.insert(3,new_a) # add anchor to the list item tag
				
				ul_ = bs.body.findAll("div", attrs={"class":"navHeaderCollapse"})[0].find("ul")# add list item to the proper unordered list tag within navigation div
				
				liList = ul_.findAll("li") # get list of all li tags in nav ul
				
				liList[len(liList) - 1].insert_after(new_li) # insert new li tag at the end of the ul
				
				# ANIMATED DONATE LINK INJECTION
				
				faultyAnchors = bs.body.find_all("a", attrs={"href":"index"}) # fix all anchors with incorrect link
				for anch in faultyAnchors:
					anch["href"] = "index.html"
				
				bs = bs.prettify() # format html code for writing
				fw.write(str(bs)) # output html code from BeautifulSoup to file
				quit()