from playwright.sync_api import sync_playwright
import json
import time
import os.path
from helper.api import CodeWarsApi

with open("./setup.json", encoding="utf-8") as fin:
    setup = json.load(fin)

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    if os.path.exists("./cookies.json"):
        with open("./cookies.json", "r", encoding="utf-8") as fin:
            context.add_cookies(json.load(fin))
        page.goto("https://www.codewars.com/dashboard")
    else:
        page.goto("https://www.codewars.com/users/sign_in")
        input("press enter when logged in")
    page.locator("//div[@class='profile-pic mr-0']/img[1]").wait_for()
    page.query_selector("//div[@class='profile-pic mr-0']/img[1]").click()
    user_name = page.url.split("/")[-1]
    api = CodeWarsApi(setup["codewars"]["api_key"])
    completed_katas = 0
    total_pages = 1
    current_page = 0
    while current_page < total_pages:
        data = api.get_user_total_completed(user_name, current_page)
        total_pages = data["totalPages"]
        current_page += 1
        for i in data["data"]:
            completed_katas += len(i["completedLanguages"])
    page.wait_for_selector("//a[text()='Solutions']").click()

    calculated_max_refreshes = completed_katas // 15 + 3
    if calculated_max_refreshes < setup["reloads_in_browser"]:
        nReloads = calculated_max_refreshes
    else:
        nReloads = setup["reloads_in_browser"]

    for _ in range(nReloads):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    with open("./source.html", "w", encoding="utf-8") as fin:
        fin.write(page.content())
    with open("./cookies.json", "w", encoding="utf-8") as fin:
        fin.write(json.dumps(context.cookies()))

    browser.close()
