from bs4 import BeautifulSoup as soup	
import requests
import glob, sys, linecache

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('{}, LINE {}:\n\n\t{}\n\n{}'.format(filename, lineno, line.strip(), exc_obj))

			
if __name__ == "__main__":
		
	dir = "site_copy"
	all_files = glob.glob("../" + dir + "/*.html")
	
	for file in all_files:
		with open(file, "rb") as fr:
			with open("eps_donate_trial2/" + file.split("\\")[1], "w", encoding="utf-8") as fw:
		
				bs = soup(fr.read()) #initialize BeautifulSoup 4 with html code
				
				try:
					
					# ANIMATED DONATE BUTTON INJECTION #
					
					new_a = bs.new_tag("a", href="https://payments.example/donate", target="_blank", id='donate-btn') # create new anchor with link
					
					new_a.string = "DONATE" # add inner HTML to anchor
					
					new_li = bs.new_tag("li", role='presentation') # create new list item
					new_li["id"] = "anim-btn" # add id to list item
					
					new_li.insert(3,new_a) # add anchor to the list item tag
					
					ul_ = bs.body.findAll("div", attrs={"class":"navHeaderCollapse"})[0].find("ul")# add list item to the proper unordered list tag within navigation div
					
					liList = ul_.findAll("li") # get list of all li tags in nav ul
					
					liList[len(liList) - 1].insert_after(new_li) # insert new li tag at the end of the ul
					
					# DONATE LINK INJECTION #
					
					# use mlg scripting strats to save about 2 lines of code
					# get all anchor tags with specified text
					anch = bs.body.find(lambda tag:tag.name=="a" and "More Episodes of Example" in tag.text and "Get" not in tag.text,{"href":"episodes.html"}) 
					
					# create new anchor
					new_anch = bs.new_tag("a", href="https://payments.example/donate",target="_blank", id="donate-link") 
					new_anch.string = " Donate to Example Podcast" # insert anchor text 
					
					beearr = bs.new_tag("br")
					beearr2 = bs.new_tag("br")
					anch.insert_after(beearr) # inject anchor to html
					beearr.insert_after(beearr2) # inject anchor to html
					beearr2.insert_after(new_anch) # inject anchor to html
					# FIX THE STUPID ASS INDEX LINK FOR THE 20TH TIME #
					faultyAnchors = bs.body.find_all("a", attrs={"href":"index"}) # fix all anchors with incorrect link
					for anch in faultyAnchors:
						anch["href"] = "index.html"
						
					# CONCLUDE SCRIPT #
					bs = bs.prettify() # format html code for output
					fw.write(str(bs)) # output html code from BeautifulSoup to file
					#quit() # save compute time for testing by only outputting to a single file
					
					
				except Exception as e: # we got some problems if we get to this point
					print("we have a little situaaaation:", end=" ")
					print(file)
					PrintException()
					bs = bs.prettify() # format html code for output
					fw.write(str(bs)) # output html code from BeautifulSoup to file