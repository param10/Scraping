from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import sys
from HomeScrape import get_tweets

website = "https://twitter.com/i/flow/login"
driver = webdriver.Safari()
driver.get(website)
driver.maximize_window()

time.sleep(5)

# Wait for the username input field and enter the username
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='text']"))
).send_keys("ENTER YOUR EMAIL")


elements = driver.find_elements(By.CSS_SELECTOR, "div.css-1rynq56")

for element in elements:
    if "Next" in element.text:  
        element.click()  
        break
#this part only if the page arrives for my case it did
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='text']"))
).send_keys("ENTER YOUR NUMBER OR USERNAME") 

elements = driver.find_elements(By.CSS_SELECTOR, "div.css-1rynq56")

for element in elements:
    if "Next" in element.text:  
        element.click()  
        break
# until here or comment this out

WebDriverWait(driver, 3).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password'][name='password']"))
).send_keys("ADD YOUR PASSWORD HERE")

elements = driver.find_elements(By.CSS_SELECTOR, "span.css-1qaijid.r-bcqeeo.r-qvutc0.r-poiln3")

for element in elements:
    if "Log in" in element.text:  
        element.click()  
        break


max_tweets = 100
tweets_collected = 0
tweets_data = []

while tweets_collected < max_tweets:
    articles = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, "//article"))
    )
    new_tweets = get_tweets(articles)
    
    for tweet in new_tweets:
        if tweet not in tweets_data:
            tweets_data.append(tweet)
            tweets_collected += 1
            if tweets_collected >= max_tweets:
                break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


df_tweets = pd.DataFrame(tweets_data)
df_tweets.to_csv('/Users/paramjaswal/Desktop/Scraping/Twitter Bot/tweets.csv', index=False)
print(df_tweets)