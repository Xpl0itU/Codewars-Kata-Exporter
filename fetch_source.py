from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from helper.api import CodeWarsApi

with open('./setup.json') as fin:
    setup = json.load(fin)

driver = webdriver.Chrome()
driver.get("https://www.codewars.com/users/sign_in")

driver.find_element_by_xpath("//button[1]").click()
input("press enter when logged in")
driver.find_element_by_xpath("//div[@class='profile-pic mr-0']/img[1]").click()

user_name = driver.current_url.split("/")[-1]
api = CodeWarsApi(setup['codewars']['api_key'])

completed_katas = 0
total_pages = 1
current_page = 0
while current_page < total_pages:
  data = api.get_user_total_completed(user_name, current_page)
  total_pages = data['totalPages']
  current_page += 1
  for i in data['data']:
      completed_katas+=len(i['completedLanguages'])

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Solutions")))
driver.find_element_by_link_text('Solutions').click()

calculated_max_refreshes = completed_katas // 15 + 3
if calculated_max_refreshes < setup['reloads_in_browser']:
    nReloads = calculated_max_refreshes
else:
    nReloads = setup['reloads_in_browser']

elem = driver.find_element_by_tag_name("body")
for _ in range(nReloads):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

with open('./source.html', 'w', encoding="utf-8") as fin:
    fin.write(driver.page_source)

driver.close()
