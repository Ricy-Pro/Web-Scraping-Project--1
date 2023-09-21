import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

import time



driver = webdriver.Chrome()


url = "https://www.ycombinator.com/companies?batch=S23&batch=W23&industry=B2B"

driver.get(url)


scroll_pause_time = 2
scroll_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_scroll_height = driver.execute_script("return document.body.scrollHeight")
    if new_scroll_height == scroll_height:
        break
    scroll_height = new_scroll_height




soup = BeautifulSoup(driver.page_source, "html.parser")

right_div= soup.find("div",{"class":"q1vdpoLtJkwUT8jN22K2 dsStC1AzZueqISZqfHLZ"})
product_elements = right_div.find_all("a",{"class","WxyYeI15LZ5U_DOM0z8F"})
print(len(product_elements))


product_details = []

def get_info(url):
    response=requests.get(url)
    soup1= BeautifulSoup(response.text,"html.parser")
    company_name=soup1.h1.text.strip()
    website=soup1.find("div",{"class":"inline-block group-hover:underline"}).text.strip()
    LinkedIn=soup1.find("a",{"title":"LinkedIn profile"})['href'] if soup1.find("a",{"title":"LinkedIn profile"}) else "-"
    location=soup1.find_all("span")[12].text.strip() if soup1.find_all("span")[12] else "-"
    name=soup1.find_all("div",{"class":"font-bold"})[1].text.strip() 
    
    
   
    
    
    product_details.append({

        "Company Name": company_name,
        "Website": website,
        "Location": location,
        "LinkedIn": LinkedIn,
        "Name": name,
        
        
      
    })
cnt=0
for product in product_elements:
    url="https://www.ycombinator.com"+product['href']
    cnt=cnt+1
    print(str(cnt)+"/344")
    
    get_info(url)
    
   
    
   


csv_filename = "Companies.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Company Name","Website","Location","LinkedIn","Name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_details)

print(f"Scraped data saved to {csv_filename}")
driver.quit()

