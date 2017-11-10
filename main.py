import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

pageOffset = 0
options = webdriver.ChromeOptions()
options.add_argument("--disable-web-security")
options.add_argument("-headless")
driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe", 0, options)
driver.set_page_load_timeout(60)
articleCount = 0
print("Navigating to godanriver")
driver.get("http://www.godanriver.com/search/?s=start_time&sd=asc&l=100&c=opinion*&o=" + str(pageOffset))
while len(driver.find_elements_by_css_selector('.results-container .card-headline h3 a')) > 0:
    listOfLinks = list(map((lambda a: a.get_attribute("href")), driver.find_elements_by_css_selector('.results-container .card-headline h3 a')))
    for l in listOfLinks:
        articleCount += 1
        print(str(articleCount) + ": " + l)
        attempts = 0

        driver.get(l)
        driver.implicitly_wait(35)
        try:
            elem = driver.find_element_by_css_selector('.hidden-print .fb-comments-count span')
            if elem != None:
                numComments = int(elem.text)
                print("Article has this many facebook comments: " + str(numComments))
                if numComments > 0:
                    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[title='Facebook Social Plugin']"))
                    commentNodes = driver.find_elements_by_class_name("_5mdd")
                    print("printing comments in comment nodes" + str(commentNodes))
                    commentPayloads = list(map((lambda commNode: commNode.text) , commentNodes))
                    print()
                    for c in commentPayloads:
                        print(c)
                    driver.switch_to.parent_frame()
            else:
                print("Comment count not loaded, skipping")
                continue

        except NoSuchElementException:
            print("Comments disabled, skipping")
    pageOffset += 100
    driver.get(
        "http://www.godanriver.com/search/?s=start_time&sd=asc&l=100&c=opinion*&o=" + str(pageOffset))
driver.close()