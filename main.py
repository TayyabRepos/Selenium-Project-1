from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import sys
import datetime as datetime

application_path=os.path.dirname(sys.executable)

now = datetime.datetime.now()

date=now.strftime("%Y-%m-%d")

 
url = 'https://www.thesun.co.uk/sport/football/'

#Headless-Option

options = Options()
options.add_argument("--headless=new")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)


 
driver.get(url)

titles=[]
subtitles=[]
links=[]
 
containers = driver.find_elements(by='xpath', value='//div[@class="teaser__copy-container"]')
for container in containers:
	title = container.find_element(by='xpath', value='.//h3')
	subtitle = container.find_element(by='xpath', value='.//p')
	link = container.find_element(by='xpath', value='.//a')
	titles.append(title.text)
	subtitles.append(subtitle.text)
	links.append(link.get_attribute('href'))

my_dict = {'title':titles, 'subtitle':subtitles, 'link':links}


data = pd.DataFrame(my_dict)

filename = f'thesun {date}.csv'

final_path=os.path.join(application_path, filename)

data.to_csv(final_path, index=False)

driver.quit()