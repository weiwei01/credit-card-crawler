from pprint import pprint
import selenium
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pydbfunction
globalCompany = "esun"
globalCategory = "others"
def writePatentHtmlToFile(fileName, html):
	file = open(fileName+".txt", 'w')
	file.write(html)
	file.close

def readDataFromDb(selectSql):
	resultList = []
	db = pydbfunction.MyDBTest()
	results = db.selectData(selectSql)
	for result in results:
		dict = {}
		dict["company"] = result[0]
		dict["category"] = result[1]
		dict["url"] = result[2]
		dict["html"] = result[3]
		resultList.append(dict)
	return resultList

def storeMainPointToDatabase(discount):
	db = pydbfunction.MyDBTest()
	dataList = []
	dataList.append(globalCompany)
	dataList.append(globalCategory)
	dataList.append(discount["title"])
	dataList.append(discount["short"])
	dataList.append(discount["url"])
	dataList.append(discount["img_url"])
	insertSql = "INSERT INTO discount_table(company, category, title, short, url, img_url) VALUES (%s, %s, %s, %s, %s, %s)"
	db.insertData(insertSql, dataList)

def parseTitle(child):
	title = ""
	try:
		title = child.find("h2").text.strip()
	except:
		title = ""
	return title
def parseShort(child):
	title = ""
	try:
		title = child.find("p",{"class":"short"}).text.strip()
	except:
		title = ""
	return title
def parseUrl(child):
	title = ""
	try:
		title = child["href"]
	except:
		title = ""
	return title
def parseImgUrl(child):
	title = ""
	try:
		title = child.find("img")["src"].strip()
	except:
		title = ""
	return title
def parseHtml(html):
	soup = BeautifulSoup(html)
	discountBlocks = soup.find("div", {"class":"page"})
	#pprint(discountBlocks)
	discountChildren = discountBlocks.findAll("a", recursive=False)
	for child in discountChildren:
		title = parseTitle(child)
		short = parseShort(child)
		url = parseUrl(child)
		img_url = parseImgUrl(child)
		#pprint(title)
		#pprint(short)
		#pprint(url)
		#pprint(img_url)
		dict = {}
		dict["title"] = title
		dict["short"] = short
		dict["url"] = url
		dict["img_url"] = img_url
		pprint(dict)
		storeMainPointToDatabase(dict)
def main():
	selectSql = "select * from promotion_table where category = '{category}' ".format(category=globalCategory) #where id = 'US9533547' # limit 500 offset 1
	resultList = readDataFromDb(selectSql)
	for result in resultList:
		try:
			company = (result["company"])
			category = (result["category"])
			url = (result["url"])
			html = (result["html"])
			#pprint(result)
			title = parseHtml(html)

		except Exception as e:
			print(e)

	
from argparse import ArgumentParser

if __name__ == '__main__': 

	main()
