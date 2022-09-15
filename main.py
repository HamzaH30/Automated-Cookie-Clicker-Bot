import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


def get_upgrade_id_cost():
    """Create a dictionary of all the upgrades' ID and their cost"""

    upgrades_tags = driver.find_elements(By.CSS_SELECTOR, "#store div")
    # Remove the last index, because it is not visible to the user
    upgrades_tags.pop()
    upgrade_IDs_cost = {}
    for upgrade in upgrades_tags:
        # Not exactly sure why I am getting errors. hence why I put this try except bloc
        try:
            upgrade_cost = int(upgrade.text.split("-")[1].split("\n")[0].strip().replace(",", ""))
        except:
            print("Error - continue")
        upgrade_IDs_cost[upgrade.get_attribute("id")] = upgrade_cost
    return upgrade_IDs_cost


# Setting up Selenium
chrome_driver_path = os.environ["CHROME_DRIVER_PATH"]
driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path))
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get the cookie
cookie = driver.find_element(By.ID, "cookie")

get_upgrade_id_cost()

five_second_timer = time.time() + 5
ending_time = time.time() + 60*1
# Setup while loop to run indefinitely
while time.time() < ending_time:
    # Click cookie
    cookie.click()

    if time.time() > five_second_timer:
        # Get the amount of money
        money = int(driver.find_element(By.ID, "money").text.replace(",", ""))

        upgrades = get_upgrade_id_cost()

        # Find which upgrade is affordable
        affordable_upgrades = []
        for upgrade_ID, upgrade_cost in upgrades.items():
            if money >= upgrade_cost:
                affordable_upgrades.append(upgrade_ID)

        # Find out the most expensive upgrade
        max_upgrade = affordable_upgrades[-1]

        # Buy/Click the most expensive upgrade
        driver.find_element(By.ID, max_upgrade).click()

        # print(f"You have {money} cookies. You can buy {affordable_upgrades}\n")

        # Reset five-second timer
        five_second_timer = time.time() + 5

# printing the number of cookies per second (cps) achieved
cps = driver.find_element(By.ID, "cps").text.split(":")[1].strip()
print(f"You got {cps} cookies per second!")

# Quitting driver
driver.quit()