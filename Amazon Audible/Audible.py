#imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time



#website
website = "https://www.audible.ca/search?node=21073389011&ref_pageloadid=not_applicable&ref=a_search_l1_catRefs_18&pf_rd_p=e73bc6dd-0441-4a91-9b45-0da1b5c2a70a&pf_rd_r=YRFMXVH735B40P6SB5YW&pageLoadId=pzUHXZpj8OOQhU9c&ref_plink=not_applicable&creativeId=9648f6bf-4f29-4fb4-9489-33163c0bb63e"

driver = webdriver.Safari()
driver.get(website)
driver.maximize_window()

#pagination
pagination = driver.find_element(By.CSS_SELECTOR, "ul.pagingElements")  
page_elements = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(page_elements[-2].text) 


# Pagination 2
current_page = 1   # this is the page the bot starts scraping

books = []  

# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    time.sleep(2)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.bc-list')))
    container = driver.find_element(By.CSS_SELECTOR, 'ul.bc-list')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.bc-list')))

    items = driver.find_elements(By.CSS_SELECTOR, 'ul.bc-list')




    for item in items:
        title_elements = item.find_elements(By.CSS_SELECTOR, 'h3.bc-heading a.bc-link')
        author_elements = item.find_elements(By.CSS_SELECTOR, 'li.authorLabel a.bc-link')
        length_elements = item.find_elements(By.CSS_SELECTOR, 'li.runtimeLabel span.bc-text')

        if title_elements:
            title_text = title_elements[0].text.strip() if title_elements else 'Unknown'

            author_text = author_elements[0].text.strip() if author_elements else 'Unknown'

            length_text = length_elements[0].text.replace('Length: ', '').strip() if length_elements else 'Unknown'

            books.append({'Title': title_text, 'Author': author_text, 'Length': length_text})
    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, './/span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass


driver.quit()

books_df = pd.DataFrame(books)
books_df.to_csv('/Users/paramjaswal/Desktop/Scraping/Amazon Audible/books.csv', index=False)


