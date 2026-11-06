from bs4 import BeautifulSoup as soup
from selenium import webdriver
import requests
import os, sys, linecache
import glob, re
import time

def get_driver():
	profile = webdriver.FirefoxProfile('path/to/firefox/profile') # open the firefox profile for adblock
	driver = webdriver.Firefox(profile) # open firefox with the profile retrieved
	print(1) #debug
	driver.set_window_size(1296,546) # resize the window automatically
	print(2) #debug
	return driver
	
def acquireAllPages(driver, a_list, baseUrl, count=-1):
	# for l in a_list:
		# print(l)
		
	print("*-/-*"*7)
	if count < 0:
		# print("wrong")
		driver.get(baseUrl)
	else:
		# print("right")
		driver.get(a_list[count])
	time.sleep(.1)
	anchs = driver.find_elements_by_xpath('//*[@href]')
	
	for anch in anchs:
		lank = anch.get_attribute("href")
		if baseUrl in lank and "#" not in lank and ".html" in lank and lank not in a_list:
			a_list.append(anch.get_attribute("href"))
	

	count+=1
	if count == len(a_list): # base case: recursion reached when end of list is reached
		print(len(a_list))
		return a_list
		
	acquireAllPages(driver, a_list, baseUrl, count)
	
def absolutePaths(path):
	for root, dirs, files in os.walk(os.path.abspath(path)):
		for file in files:
			yield(os.path.join(root, file))
		break

def getFilename(file):
	
	return file.split("\\")[-1]

class PathList:
	def __init__(self, files=[], dir=""):
		self.files=files
		self.setInputDirectory(dir)
		
	def filter(self, term):
			self.files = [f for f in self.files if term in f]
	
	def setInputDirectory(self, path, update=True):
		self.dir = path
		if update:
			self.files = list(absolutePaths(path))
	
	def setOutputDirectory(self, path):
		self.outdir = path
		
	def addFile(self, filepath):
		if type(filepath) == type(str()) and filepath not in self.files:
			self.files.append(filepath)
		elif filepath in self.files:
			print("file already exists")
		else:
			raise ValueError("Parameter must be string filepath")
			
	def addFiles(self, filepaths):
		exists=[]#debug
		if type(filepaths) == type(list()):
			#self.files.extend(filepaths)
			for f in filepaths:
				if f not in self.files:
					self.files.append(f)
				else:
					exists.append(f)
		else:
			raise ValueError("Parameter must be a list string filepaths.")
			
		if len(exists) > 0:
			print("some items excluded due to duplicates")
		elif len(exists) == len(filepaths):
			print("all files already exist; no changes made")
		
	def clearFiles(self):
		self.files = []
		
class Scraper:
	def __init__(self, fl=None, useDriver=False, baseUrl=""):
		if useDriver: # only need driver for javascript generated websites
			if baseUrl == "":
				raise ValueError("3rd parameter must contain a url to the base webpage")
			self.driver = get_driver()
			self.fileList = acquireAllPages(self.driver, [], baseUrl)
			
		elif fl is not None:
			self.fileList = fl
		
		else:
			raise ValueError("Parameters for scraper constructor are invalid")
			
	def setFileList(self, fl):
		self.fileList = fl

	
	def groupSearchElement(self, elem, attributes={}, area="body"):
		outList = []
		for file in self.fileList.files:
			with open(file, "rb") as fr:
				bs = soup(fr.read())
				if area == "body":
					e_ = bs.body.find(elem, attrs=attributes)
				elif area == "head":
					e_ = bs.head.find(elem, attrs=attributes)
				else:
					raise ValueError("area parameter must only contain 'body' or 'head'")
				
				if e_ is not None:
					outList.append(file)
		return outList
		
	def refineSearchElement(self, elem, attributes={}, area="body", fileContains=None):
		# search through some files in fileList using advanced search
		# return files where element is present as a list
		if type(attributes)!=type(dict()):
			raise ValueError("attributes parameter must be a dictionary")
			
		outList = []
		newList = []
		if fileContains:
			newList = [i for i in self.fileList.files if fileContains in i]
		for file in newList:
			with open(file, "rb") as fr:
				bs = soup(fr.read())
				if area == "body":
					e_ = bs.body.find(elem, attrs=attributes)
				elif area == "head":
					e_ = bs.head.find(elem, attrs=attributes)
				else:
					raise ValueError("area parameter must only contain 'body' or 'head'")
				
				if e_ is not None:
					outList.append(file)
		return outList
		
	def updateElementValue(self, files, elem, attributes, newValue, area="body"):
		# take a file string and elem tagObject and update ONE file with parameters specified
		for file in files:
			with open(file, "rb") as fr:
				with open(self.fileList.outdir+ "/" + getFilename(file), "w", encoding="utf-8") as fw:
					bs = soup(fr.read())
					if area == "body":
						e_ = bs.body.find(elem, attrs=attributes)
					elif area == "head":
						e_ = bs.head.find(elem, attrs=attributes)
					else:
						raise ValueError("area parameter must only contain 'body' or 'head'")
					e_.string = newValue

					bs = bs.prettify() # format html code for output
					fw.write(str(bs)) # output html code from BeautifulSoup to file
				
	
	def updateElementAttribute(self, files, elem, attributes, attribute, attributeVal, area="body"):
		# take a fileList object and update each file with parameters specified
		for file in files:
			with open(file, "rb") as fr:
				with open(self.fileList.outdir + "/" + getFilename(file), "w", encoding="utf-8") as fw:
					bs = soup(fr.read())
					if area == "body":
						e_ = bs.body.find(elem, attrs=attributes)
					elif area == "head":
						e_ = bs.head.find(elem, attrs=attributes)
					else:
						raise ValueError("area parameter must only contain 'body' or 'head'")
					e_[attribute] = attributeVal

					bs = bs.prettify() # format html code for output
					fw.write(str(bs)) # output html code from BeautifulSoup to file
		
	def updateElementAttributes(self, files, elem, attributes, updateAttributes, area="body"):
		# take a fileList object and update each file with parameters specified
		if type(attributes)!=type(dict()):
			raise ValueError("attributes parameter must be a dictionary")
		
		
		for file in files:
			with open(file, "rb") as fr:
				with open(self.fileList.outdir + "/" + getFilename(file), "w", encoding="utf-8") as fw:
					bs = soup(fr.read())
					if area == "body":
						e_ = bs.body.find(elem, attrs=attributes)
					elif area == "head":
						e_ = bs.head.find(elem, attrs=attributes)
					else:
						raise ValueError("area parameter must only contain 'body' or 'head'")
					
					for key in updateAttributes.keys():
						e_[key] = updateAttributes[key]

					bs = bs.prettify() # format html code for output
					fw.write(str(bs)) # output html code from BeautifulSoup to file

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('{}, LINE {}:\n\n\t{}\n\n{}'.format(filename, lineno, line.strip(), exc_obj))
	
	
if __name__ == "__main__":
	
	# s = PathList()
	# s.addFile("a")
	
	# d = get_driver()
	# bse = "https://podcast.example/"
	# pages=[bse]
	# acquireAllPages(d, pages, bse)
	
	# print(len(pages))
	# for i in pages:
		# print(i)
		
	inp = "./site_copy"
	outp = "./output"
		
	
	pl = PathList(dir=inp)
	pl.setOutputDirectory(outp)
	print(len(pl.files))
	term = ".html"
	pl.filter(term)
	print(len(pl.files))
	# for a in pl.files:
	# 	print(a)
	# quit()
	sss = Scraper(fl=pl)

	elemnt = "a"
	searchDict = {"href":"https://payments.example/donate?button=BUTTON_ID"}

	print("test group search (indiscriminate): ", end="")
	gsList = sss.groupSearchElement(elemnt, searchDict)
	print(len(gsList))
	print("test refined search (with search terms):", end="")
	rsList = sss.refineSearchElement(elemnt, searchDict, fileContains="ep_")
	print(len(rsList))

	# print("test update element value (simple):", end="")
	# sss.updateElementValue(rsList, elemnt, searchDict, "DON TE")
	# print("test update element value (extra):", end="")
	# sss.updateElementValue(rsList, elemnt, {"id": "donate-btn"}, "DON TE")

	# print("test update element attribute (single):", end="")
	# sss.updateElementAttribute(rsList, elemnt, searchDict, "class", "donate-btn donate-btn2")

	print("test update element attributes (multiple):", end="")
	sss.updateElementAttributes(rsList, elemnt, searchDict, {"href": "https://www.google.com", "class":"no-class-here haha", "src":"none"} )


	