from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Configuration
REMOTE_DEBUGGING_URL = "127.0.0.1:9222"  # Remote debugging URL

def get_members(driver):
    wait = WebDriverWait(driver, 60)  # Increase the timeout to 60 seconds
    try:
        print("Waiting for the members button to be clickable...")
        members_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='avatar_stack']"))
        )
        print("Members button found, clicking...")
        members_button.click()
        time.sleep(3)

        members = []
        while True:
            print("Finding member elements...")
            member_elements = driver.find_elements(By.XPATH, "//div[@data-qa='member_row']")
            print(f"Found {len(member_elements)} members on the page.")
            for member in member_elements:
                member_name = member.find_element(By.XPATH, ".//span[@data-qa='member_display_name']").text
                members.append(member_name)

            try:
                load_more_button = driver.find_element(By.XPATH, "//button[@data-qa='more_members_button']")
                print("Load more button found, clicking...")
                load_more_button.click()
                time.sleep(3)
            except Exception:
                print("No more load more button found.")
                break
        
        return members
    except Exception as e:
        print("Exception occurred while getting members:", e)
        print(driver.page_source)  # Print page source for debugging
        driver.quit()
        raise

if __name__ == "__main__":
    # Configure Chrome browser options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("debuggerAddress", REMOTE_DEBUGGING_URL)

    # Create Chrome WebDriver instance with remote debugging
    driver = webdriver.Chrome(options=options)
    
    try:
        # Directly go to the specific Slack channel URL if needed, otherwise assume you are already on the page
        # driver.get(SLACK_CHANNEL_URL)
        # time.sleep(5)
        
        members = get_members(driver)
        
        with open('members.json', 'w') as f:
            json.dump(members, f)
        print(f"Saved {len(members)} members to members.json.")
    finally:
        driver.quit()
