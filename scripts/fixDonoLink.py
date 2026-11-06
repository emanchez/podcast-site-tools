# donate-link
# donate-btn



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
		
	input_dir = "01_14_2020" # directory for website files
	output_dir = "donate_trial3"
	all_files = glob.glob("../" + input_dir + "/*.html") # grab all html files ONLY
	correct_link = "https://payments.example/donate?button=BUTTON_ID" # link to fix faulty anchor tags
	
	# begin loop
	for file in all_files:
		with open(file, "rb") as fr:
			#all_files contain filenames with an added "01_14_2020\" at the front of all of them. So we need to filter it using file.split("\\")[1] so we only have the name of the files and not relative filepaths
			with open(output_dir + "/" + file.split("\\")[1], "w", encoding="utf-8") as fw:
				bs = soup(fr.read()) #initialize BeautifulSoup 4 with html code
				
				try: # fix button
					
					bs.find("a",{"id":"donate-btn"})["href"] = correct_link
				
				except: # anchor not found, show fatal error and exit program
				
					print("we got a little situaaaaation: ")
					PrintException()
					quit()
					
				try: # fix link
					
					bs.find("a", {"id":"donate-link"})["href"] = correct_link
				
				except: # okay to have errors because there are some files hat don't contain this particular anchor id, we just pass to the next iteration of the for-loop after showing the error
					print("invalid link maybe?: {}".format(file))
					PrintException()
					print()
					print()
					continue
				
				faultyAnchors = bs.body.find_all("a", attrs={"href":"index"}) # fix all anchors with incorrect link
				for anch in faultyAnchors:
					anch["href"] = "index.html"
					 
				bs = bs.prettify() # format html code for writing
				fw.write(str(bs)) # output html code from BeautifulSoup to file
				
					