from pprint import pprint
import selenium
from bs4 import BeautifulSoup
import time
from pyquery import PyQuery as pq
from lxml import etree
from treelib import Node, Tree
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pydbfunction
def writePatentHtmlToFile(fileName, html):
	file = open(fileName+".txt", 'w')
	file.write(html)
	file.close
	
def crawlPageHtml(url):
	#使用chrome的webdriver
	#browser = webdriver.Chrome()
	#開啟google首頁
	#browser.get(url)
	#time.sleep(5)
	#html = browser.page_source
	#pprint(html)
	#如果需要執行完自動關閉，就要加上下面這一行
	#browser.close()

	driver = webdriver.Remote(
		command_executor='http://127.0.0.1:4444/wd/hub',
		 desired_capabilities=DesiredCapabilities.CHROME
	)
	driver.get(url)
	time.sleep(5)
	html = driver.page_source
	driver.quit() # 關閉 chromedriver
	
	#write
	#writePatentHtmlToFile(patentId, html)
	
	
	
	
	#read
	#fileName = "US9533547.txt"
	#file = open(fileName, 'r', encoding='UTF-8')
	#html = file.read()
	#print(content)
	#file.close()
	

	
	
	
	
	#patentContent = pq("class","flex flex-width style-scope patent-result")
	#patentContent = doc.attr("class", "flex flex-width style-scope patent-result")
	#claim = doc.attr("class", "claim style-scope patent-text")	
	return html
def parseToTree(html):

	soup = BeautifulSoup(html)
	parsed_soup = soup.findAll("div", {"class":"flex flex-width style-scope patent-result"})[1]
	patentClaims = parsed_soup.findAll("div", {"class":"claim style-scope patent-text"})
	#patentContent = parsed_soup.findAll("div", {"class":"flex flex-width style-scope patent-result"})
	#patentClaims = patentContent.find("div", {"class":"claim style-scope patent-text"})
	#
	patentDict = {}
	#tree.create_node('ROOT','root')  # root node
	for claim in patentClaims:
		#print(claim.text)
		dependentTo = claim.find("claim-ref")#.get("idref")
		

		if dependentTo:
			dependentTo = dependentTo.get("idref")
			#print("dependent: " + dependentTo.text)
			#print("Parent: " + str(dependentTo))
			#pass
		claimId = (claim.get('id'))
		#print(patentId)
		#patentClaim = (claim)
		#print(patentClaim)
		
		
		
		if claimId is None:
			continue
		#print("claimId: " + claimId)
		#print("claim: " + str(claim))

		if dependentTo:
			patentDict[claimId] = dependentTo
		else:
			patentDict[claimId] = "root"

		
		#if dependentTo in patentDict:
		#	patentDict[dependentTo].append(patentId)
		#else:
		#	patentDict[patentId] = []
		#print("###########")
		#pprint(patentDict)
		
	
	return patentDict

	
def makeTree(patentDict):
	added = set()
	tree = Tree()

	tree.create_node('ROOT','root')
	for key, value in patentDict.items():
		if value == "root":
			tree.create_node(key, key, 'root')
		else:
			tree.create_node(key, key, value)
	return tree
def parseClaims(html):
	soup = BeautifulSoup(html)
	parsed_soup = soup.findAll("div", {"class":"flex flex-width style-scope patent-result"})[1]
	return parsed_soup

def parseSummary(html):
	soup = BeautifulSoup(html)
	#for content in parsed_soup:


	#parsed_soup = soup.findAll("heading", {"class":"heading"})
	parsed_soup = soup.findAll("heading")
	summaryId = ""
	summmaryNextHeadingId = ""
	for i in range(len(parsed_soup)):
		id = (parsed_soup[i].get("id"))
		text = (parsed_soup[i].text)

		if text == "SUMMARY":
			summaryId = id
			summmaryNextHeadingId = parsed_soup[i+1].get("id")
	pprint(parsed_soup)
	print(summaryId)
	print(summmaryNextHeadingId)
	
	summaryPosition = 0
	summaryNextPosition = 0
	summary = ""
	
	parsed_soup = soup.findAll("div", {"class":"flex flex-width style-scope patent-result"})[0]
	for i in range(len(list(parsed_soup.descendants))):
		content = list(parsed_soup.descendants)[i]
		id = ""
		try:
			id = content.get("id")
		except:
			pass
		if id == summaryId:
			summaryPosition = i
			continue

		if id == summmaryNextHeadingId:
			summaryNextPosition = i
			break
#		if summaryPosition  == 0 or summaryNextPosition == 0:
#			continue
		if summaryPosition != 0 and i > summaryPosition:
			if content.string:
				summaryContent = content.string
				#summaryContent = summaryContent.replace("\n", "")
				#summaryContent = summaryContent.replace("\'", "")
				summary += summaryContent + " "
			
	#print(summary)
	#print(summaryPosition, summaryNextPosition)


	return parsed_soup
def storeToDatabase(patentId, url, html):
	db = pydbfunction.MyDBTest()
	dataList = []
	dataList.append(patentId)
	dataList.append(url)
	dataList.append(html)
	insertSql = "INSERT INTO patent_html(id, url, html) VALUES (%s, %s, %s)"
	db.insertData(insertSql, dataList)
def main(patentId):
	url = 	"https://patents.google.com/patent/"+ patentId
	html = crawlPageHtml(url)
	#patentDict = parseToTree(html)
	#pprint(patentDict)
	#tree = makeTree(patentDict)
	#print("ID: " + patentId)
	#tree.show()	
	#summary = parseSummary(html)
	#claims = parseClaims(html)
	#pprint(claims.text)
	storeToDatabase(patentId, url, html)
	#print((patentClaims))
from argparse import ArgumentParser

if __name__ == '__main__': 
	#parser = ArgumentParser()
	#parser.add_argument("-q", "--optional-arg", 
	#	help="optional argument", dest="opt", default="US9731707")	
	#args = parser.parse_args()
	#print("Patent ID:", args.opt)
	
	#main(args.opt) 
	main("esun", "")

