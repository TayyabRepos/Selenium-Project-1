import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

url = 'https://www.amazon.co.uk/gp/bestsellers/computers/429886031?ref_=Oct_d_obs_S&pd_rd_w=VEtF7&content-id=amzn1.sym.57a927eb-79cc-4b22-a466-2e2c1b28ddac&pf_rd_p=57a927eb-79cc-4b22-a466-2e2c1b28ddac&pf_rd_r=5Q0DK4A93SHC70HMJNK1&pd_rd_wg=XNq7F&pd_rd_r=f825845a-a2a2-4526-b6e0-85edd9112ce8'

options = Options()
# options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

driver.maximize_window()

driver.get(url)

time.sleep(2)
#scroll to bottom of page
# Get the total height of the webpage
total_height = int(driver.execute_script("return document.body.scrollHeight"))

# Scroll to 80% of the total height
scroll_height = int(total_height * 0.8)
driver.execute_script(f"window.scrollTo(0, {scroll_height});")
time.sleep(5)

next_button = driver.find_element(By.CSS_SELECTOR, "li[class='a-last']")
prices = []
titles = []
imgURLs = []
def page_data():
    elem_list = driver.find_elements(By.CSS_SELECTOR, '#gridItemRoot > div')
    print(len(elem_list))

    for item in elem_list:
        price = None
        title = item.find_element(By.XPATH, './/div[2]/div/a[2]/span/div')
        imgURL = item.find_element(By.XPATH, './/div[2]/div/a/div/img').get_attribute('src')
        link = item.find_element(By.XPATH, './/div[2]/div/a').get_attribute('href')
        imgURLs.append(imgURL)
        titles.append(title.text)
        print(f'Title: ' + title.text)

        try:
            # price = item.find_element(By.XPATH, ".//div[2]/div/div[2]/a/span/span/span")
            price = item.find_element(By.CSS_SELECTOR, "span[class='p13n-sc-price']")
        except:
            pass

        if not price:
            try:
                # price = item.find_element(By.XPATH, './/div[1]/div/a/span/span')
                price = item.find_element(By.CSS_SELECTOR, "span[class='_cDEzb_p13n-sc-price_3mJ9Z']")
            except:
                pass

        if price:
            prices.append(price.text)
        else:
            prices.append('N/A')

        if price:
            print('Price: ' + price.text)
        elif price is None:
            print('Price: N/A')
        print('Image URL: ' + imgURL)
        print('Link: ' + link)

    print(len(prices))
    print(len(titles))
    print(len(imgURLs))


while True:
    page_data()
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li[class='a-last'] a")
        next_button.click()
        time.sleep(2)
        # scroll to bottom of page
        # Get the total height of the webpage
        total_height = int(driver.execute_script("return document.body.scrollHeight"))

        # Scroll to 80% of the total height
        scroll_height = int(total_height * 0.8)
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(5)
    except:
        break

my_dict = {'Title': titles, 'Price': prices, 'Image URL': imgURLs}
df = pd.DataFrame(my_dict)
df.to_csv('amazon.csv', index=False)
driver.quit()


#https://tohfaakib.com/google-maps-data-scraping-python-selenium/