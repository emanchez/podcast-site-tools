from bs4 import BeautifulSoup as soup
import requests
import glob
			
if __name__ == "__main__":
		
	dir = "site_copy"
	all_files = glob.glob("../" + dir + "/ep_*.html")
	
	for file in all_files:
		with open(file, "rb") as fr:
		
			bs = soup(fr.read()) #initialize BeautifulSoup 4 with html code
			try:
				#use mlg python strats to search for tags using inline functions
				anch = bs.body.find(lambda tag:tag.name=="a" and tag.text==" More Episodes of Example Podcast",{"href":"episodes.html"})
				
				#show what each search result yields
				if anch:
					print(anch)
					
				
				
				
			except Exception as e:
				print("we have a little situaaaation")
				print(e)