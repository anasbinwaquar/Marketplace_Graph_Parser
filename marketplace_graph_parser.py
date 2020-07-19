from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import re

def Graph_Parser(url,driver):
	driver.get(url)   
	name=driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[2]/div[1]/span').text
	soup=BeautifulSoup(driver.page_source,'html.parser')
	all_scripts = soup.find_all('script')
	script=all_scripts[19]
	print(name)
	with open("data.json", "w", encoding="utf8") as outfile:
	        json.dump(str(script), outfile, indent=2)
	f=open('data.json')
	data=json.load(f)
	label_regex=re.compile(r"labels:.*|data:.*")
	data=label_regex.findall(data)
	dates_sold=list()
	median_price=list()
	quantity_sold=list()
	dates_sold=data[0][10:len(data[0])-4].split('","')
	median_price=data[1][8:len(data[1])-3].split('","')
	quantity_sold=data[2][8:len(data[2])-3].split('","')
	f=open('./Graph_Data\\'+ name+'.csv','w',encoding='utf8')
	f.truncate()
	f.write('Dates_Sold,Median_Price,Quantity_Sold'+'\n')
	for i in range(len(dates_sold)):
		f.write(dates_sold[i].replace(',','')+','+ median_price[i]+','+  quantity_sold[i]+'\n' )
	f.close()


urls=list()
with open('links.csv', 'r',encoding='utf8',errors='ignore') as file:
    for line in file.readlines():
    	urls.append(line)
chrome_dir = 'C:\\Users\\Anas\\Desktop\\Web crawl Using Python\\Web Driver\\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-data-dir=C:\\Users\\Anas\\Desktop\\Web crawl Using Python\\chrome-data")
driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe',options=chrome_options)
for url in urls:
	Graph_Parser(url,driver)

driver.quit()