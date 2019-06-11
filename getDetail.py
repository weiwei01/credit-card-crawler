from pprint import pprint
import selenium
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pydbfunction
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

globalCompany = "esun"
globalCategory = "others"


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
	

	
	return html
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
		dict["title"] = result[2]
		dict["url"] = result[3]
		dict["short"] = result[4]
		dict["img_url"] = result[5]
		resultList.append(dict)
	return resultList

def storeMainPointToDatabase(company, category, url, title, short, img_url, discount_info):
	db = pydbfunction.MyDBTest()
	dataList = []
	dataList.append(company)
	dataList.append(category)
	dataList.append(url)
	dataList.append(title)
	dataList.append(short)
	dataList.append(img_url)
	dataList.append(discount_info)
	insertSql = "INSERT INTO detail_table(company, category, url, title, short, img_url, discount_info) VALUES (%s, %s, %s, %s, %s, %s, %s)"
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
	discountBlocks = soup.find("div", {"class":"tab-list-content active"})
	discount_info = ""
	try:
		discount_info = discountBlocks.text
	except:
		pass
	return discount_info
def main():
	selectSql = "select company,category,title,url,short,img_url from discount_table "
	resultList = readDataFromDb(selectSql)
	esun_url = "https://www.esunbank.com.tw"
	for result in resultList:
		try:
			company = (result["company"])
			category = (result["category"])
			url = (result["url"])
			title = (result["title"])
			short = (result["short"])
			img_url = (result["img_url"])
			#pprint(result)
			print(esun_url+url)
			
			html =  crawlPageHtml(esun_url+url)
			discount_info = parseHtml(html)
			
			storeMainPointToDatabase(company, category, url, title, short, img_url, discount_info)

		except Exception as e:
			print(e)

	
from argparse import ArgumentParser

if __name__ == '__main__': 

	main()
