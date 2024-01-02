from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time  


your_username = "YOUR USERNAME"


def get_tweets(articles):
    tweets_data = []

    for article in articles:
        try:
            username_element = article.find_element(By.XPATH, ".//span[contains(@class, 'css-1qaijid') and starts-with(text(), '@')]")
            username = username_element.text.strip()

            if username == your_username:
                continue
            try:
                text_element = article.find_element(By.XPATH, ".//div[@lang='en'][contains(@class, 'css-1rynq56')]")
                text = text_element.text.strip()
            except NoSuchElementException:
                text = "No text found"

            tweets_data.append({'username': username, 'text': text})
        except NoSuchElementException:
            print("Article without a username found, skipping...")

    return tweets_data
    

