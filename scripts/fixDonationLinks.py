'''

Author: Emmanuel Sanchez

Script: Fix Donation Links
Function: Sift through a group of html files for 2 specific anchor tags and update their href values to the correct donation url (tests showed that 95% of them were broken links; it's easier to just write the correct url to all of them)
'''

from bs4 import BeautifulSoup as soup
import requests, glob
	
if __name__ == "__main__":
		
	input_dir = "site_01_14_2020" # directory for website files
	output_dir = "donate_trial3" # directory to export changes
	all_files = glob.glob("../" + input_dir + "/*.html") # grab all html files ONLY
	correct_link = "https://payments.example/donate?button=BUTTON_ID" # link to fix faulty anchor tags
	
	# begin loop
	for file in all_files:
	
		# read bytes of file
		with open(file, "rb") as fr:
		
			# the list "all_files" contains filenames with an added "01_14_2020\\" string at the front of all of them. We need to filter it using "file.split("\\")[1]" so we only have the name of the files and not relative filepaths
			with open(output_dir + "/" + file.split("\\")[1], "w", encoding="utf-8") as fw:
				bs = soup(fr.read()) #initialize BeautifulSoup 4 with html code
				
				try: # fix button url
					
					bs.find("a",{"id":"donate-btn"})["href"] = correct_link
				
				except Exception as e: # anchor not found, show fatal error and exit program
				
					print("error in file when searching for donate-btn id: {}".format(file))
					print(e)
					quit()
					
				try: # fix link url
					
					bs.find("a", {"id":"donate-link"})["href"] = correct_link
				
				except Exception as e: # okay to have errors because there are some files that don't contain this particular anchor, we just pass to the next iteration of the for-loop after showing the error
					print("error in file when searching for donate-link id: {}".format(file))
					print(e, end="\n\n")
					continue
				
					 
				bs = bs.prettify() # format html code for viewing, otherwise everything will be written to a single line
				fw.write(str(bs)) # output html code from BeautifulSoup class to file
				
					