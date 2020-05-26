""" Simple Selenium tests """
import os

# Selenium 3.14+ doesn't enable certificate checking
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# This is the only code you need to edit in your existing scripts.
# The command_executor tells the test to run on Sauce, while the desired_capabilities
# parameter tells us which browsers and OS to spin up.
desired_cap = {
    'platform': "Windows 10",
    'browserName': "chrome",
    'browserVersion': 'beta',
    'version': "beta",
    'extendedDebugging': True,
    "capturePerformance": True,
    'crmuxdriverVersion': 'beta',
    'name': 'custom-commands-e2e-test',
    'build': "build-1234567890"
}


username = os.environ["SAUCE_USERNAME"]
access_key = os.environ["SAUCE_ACCESS_KEY"]

hub_url = 'https://{}:{}@ondemand.saucelabs.com/wd/hub'

driver = webdriver.Remote(
   command_executor=hub_url.format(username, access_key),
   desired_capabilities=desired_cap)
)

# This is your test logic. You can add multiple tests here.
driver.get("http://www.google.com")

driver.execute_script('sauce:performance', {'name': 'custom-commands-e2e-test', 'metrics': ['load']})

if "Google" not in driver.title:
    raise Exception("Unable to load google page!")
elem = driver.find_element_by_name("q")
elem.send_keys("Sauce Labs")
elem.send_keys(Keys.TAB)
elem.submit()
assert "Sauce" in driver.title

# This is where you tell Sauce Labs to stop running tests on your behalf.
# It's important so that you aren't billed after your test finishes.
driver.quit()
