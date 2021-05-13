from selenium import webdriver
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv
from itertools import zip_longest
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


car_model={
'focus','fusion','taurus','mustang','escape','ecosport','edge','flex','explorer','expedition','transit','transit-connect','f-250-super-duty'
,'f-350-super-duty','f-150','ranger'
}

#'coupe','wagon','sedan','hatchback','suv','type-s','32-type-s','hybrid','type-r'}
car_year={'2015','2016','2017','2018','2019'}
driver = webdriver.Chrome()
models=[]
years=[]
i=0
rating=[]
for model in car_model:
       for year in car_year:
              url= "https://www.edmunds.com/ford/"+model+"/"+year+"/review/"
              i+=1
              print(i)
              print(url)
              result = requests.get(url, headers=headers)
              print(result.status_code)
              if result.status_code==200: 
                driver.maximize_window()
                driver.get(url)
                time.sleep(5)
                content = driver.page_source.encode('utf-8').strip()
                soup = BeautifulSoup(content,"html.parser")
                officials = soup.findAll("div",{"class":"editorial-review-section"})
                ratings=""
                for entry in officials:                     
                     quote=entry.text
                     ratings+=quote
                     print("scraped")
                    #print(quote)
                #print(ratings)
                models.append(model)
                years.append(year)
                rating.append(ratings)
print(models)
print(years)
print(rating)


d = [models, years,rating]
export_data = zip_longest(*d, fillvalue = '')
with open('expert.csv', 'w',  newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Model", "Year","Review"))
      wr.writerows(export_data)
myfile.close()              

driver.quit()
print("done")
