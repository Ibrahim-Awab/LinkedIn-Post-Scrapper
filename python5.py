from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome driver with headless options
options = webdriver.ChromeOptions()
options.add_argument("headless")

exe_path = ChromeDriverManager().install()
service = Service(exe_path)
# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Firefox()


# Log in to LinkedIn
driver.get("https://www.linkedin.com/login")
sleep(6)

linkedin_username = ""
linkedin_password = ""

driver.find_element(By.XPATH, "//input[@id='username']").send_keys(linkedin_username)
driver.find_element(By.XPATH, "//input[@id='password']").send_keys(linkedin_password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
sleep(20)

# Navigate to My Network page to get connections
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
sleep(5)

# Scrape the first five connections
connection_links = []

# Extract the first five connections' URLs
connections = driver.find_elements(By.XPATH, "//a[contains(@class, 'mn-connection-card__link')]")[:5]
for connection in connections:
    connection_links.append(connection.get_attribute('href'))

for profile_url in connection_links:
    driver.get(profile_url + 'recent-activity/all/')
    sleep(5)

    try:
        post_elements = driver.find_elements(By.XPATH, ".//div[contains(@class, 'update-components-actor__meta relative')]")
        if post_elements:
            post_owner = post_elements[0].text
            print('Post Owner:', post_owner)

            # post_date = driver.find_element(By.XPATH, ".//a[contains(@class, 'app-aware-link update-components-actor__sub-description-link')]").text
            # print('Post Date:', post_date)

            post_text_elements = driver.find_elements(By.XPATH, ".//div[contains(@class, 'feed-shared-update-v2__description-wrapper mr2')]")
            repost_text_elements = driver.find_elements(By.XPATH, ".//div[contains(@id, 'fie-impression-container')]")

            if post_text_elements:
                post_text = post_text_elements[0].text
                print('Post Text:', post_text)
            elif repost_text_elements:
                repost_text = repost_text_elements[0].text
                print('Repost Data:', repost_text)
            else:
                print("No text found for the post")

            like_button = driver.find_element(By.XPATH, ".//button[contains(@class, 'react-button__trigger')]")
            like_status = like_button.get_attribute('aria-pressed')
            if like_status == 'true':
                print('Like Post: True')
            else:
                print('Like Post: False')
            print('*************************************')
        else:
            print(f"No posts found for {profile_url}")

    except Exception as e:
        print(f"Error scraping post for {profile_url}: {e}")
    sleep(4)

# driver.close()



                
                