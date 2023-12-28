#imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#website
website = "https://www.audible.ca/search"

driver = webdriver.Safari()
driver.get(website)
driver.maximize_window()

wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.bc-list')))
container = driver.find_element(By.CSS_SELECTOR, 'ul.bc-list')
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.bc-list')))

items = driver.find_elements(By.CSS_SELECTOR, 'ul.bc-list')



books = []  

for item in items:
    title_elements = item.find_elements(By.CSS_SELECTOR, 'h3.bc-heading a.bc-link')
    author_elements = item.find_elements(By.CSS_SELECTOR, 'li.authorLabel a.bc-link')
    length_elements = item.find_elements(By.CSS_SELECTOR, 'li.runtimeLabel span.bc-text')

    if title_elements:
        title_text = title_elements[0].text.strip() if title_elements else 'Unknown'

        author_text = author_elements[0].text.strip() if author_elements else 'Unknown'

        length_text = length_elements[0].text.replace('Length: ', '').strip() if length_elements else 'Unknown'

        books.append({'Title': title_text, 'Author': author_text, 'Length': length_text})



driver.quit()

books_df = pd.DataFrame(books)
books_df.to_csv('/Users/paramjaswal/Desktop/Scraping/Amazon Audible/books.csv', index=False)


