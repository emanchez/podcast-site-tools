
from bs4 import BeautifulSoup as soup
import requests
import glob
import re
			
if __name__ == "__main__":
		
	dir = "post final/backup"

	all_files = glob.glob("../" + dir + "/*.html")
	for file in all_files:
		with open(file, "rb") as fr:
			with open("test_files/" + file.split("\\")[1], "w", encoding="utf-8") as fw:
				#print(file)
				bs = soup(fr.read()) #initialize BeautifulSoup 4 with html code
				
				
				new_i = bs.new_tag("img", id="ppimg", src="pix/pp.png", width="75%")
				new_a = bs.new_tag("a", href="https://payments.example/donate?button=BUTTON_ID")
				new_a.insert(3, new_i)
				
				try:
					bs.body.find("a",attrs={"href":"http://www.stitcher.com/podcast/example-podcast"}).parent.find_all("br")[6].insert_after(new_a)
					bs.body.find_all("a", attrs={"href":"index"})[0]["href"] = "index.html"
				except AttributeError:
					print("cannot apply script to " + file)
					continue
				
				new_a = bs.new_tag("a", href='https://payments.example/donate?button=BUTTON_ID')

				# # create new anchor with link
				# new_a["id"] = 'donate-btn' # add id to anchor
				# new_a.string = "DONATE" # add inner HTML to anchor
				
				# new_li = bs.new_tag("li", role='presentation') # create new list item
				# new_li["id"] = "anim-btn" # add id to list item
				
				# new_li.insert(3,new_a) # add anchor to the list item tag
				
				bs.body.find("li", attrs={"id":"anim-btn"}).find("a")["href"] = 'https://payments.example/donate?button=BUTTON_ID' # add list item to the proper unordered list tag within navigation div
				
				bs = bs.prettify() # format html code for writing
				fw.write(str(bs)) # output html code from BeautifulSoup to file
				#quit()