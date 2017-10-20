from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
import time
import unittest
import os

# /Users/ryankavanaugh/Desktop/AMZUTests

# This test verifies that the Future Info Toolbar buttons are fully functional

driverName = []
driverName.append(webdriver.Chrome())
driverName.append(webdriver.Firefox())
driverName.append(webdriver.Safari())
driverName.append(webdriver.PhantomJS())

# For remote control browser
caps = []
caps.append(webdriver.DesiredCapabilities.CHROME)
caps.append(webdriver.DesiredCapabilities.FIREFOX)
caps.append(webdriver.DesiredCapabilities.FIREFOX)

class Verify_Idaho_Links(unittest.TestCase):

    def setUp(self):
        pass


    def test_Future_Info_Button_Is_Active(self):
        # for cap in caps:
        #     self.driver = webdriver.Remote(command_executor = 'http://localhost:4444/wd/hub', desired_capabilities=cap)
        for browser in driverName:

            self.driver = browser
            driver = self.driver
            url = 'http://hb.511.idaho.gov/'
            driver.set_window_size(1800, 1100)
            driver.get(url)
            loginElement = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'timeFrameSelectorDiv')))

            driver.find_element_by_id('timeFrameSelectorDiv').click()

            assert driver.find_element_by_id('timeFrameSelectorDiv').is_enabled()

            assert driver.find_element_by_id('smallTextLnk').is_enabled()

            assert driver.find_element_by_id('normalTextLnk').is_enabled()

            assert driver.find_element_by_id('largeTextLnk').is_enabled()

            assert driver.find_element_by_id('textOnlySiteLinkSpan').is_enabled()

            driver.quit()


    def tearDown(self):
        print "Test Completed"


if __name__ == '__main__':
    unittest.main()

