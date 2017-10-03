from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
import time
import unittest

class Verify_Zoom_Feature(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        print '\n' + "Test for CO: Verifying login feature and saving a route features" + '\n'


    def test_login_credentials(self):

        driver = self.driver

    #   HEAD TO CO WEBSITE
        driver.get("http://cowebtg.carsstage.org/")

    #   SELECT THE FAVORITE PAGE
        time.sleep(4)
        signInButton = driver.find_element_by_id('favoriteBtn')
        signInButton.click()

    #   LOGIN INFO/LOGIN BUTTON
        time.sleep(2)
        driver.find_element_by_id('userAccountEmail').send_keys('ryan.kavanaugh@crc-corp.com') # Login
        driver.find_element_by_id('userAccountPassword').send_keys('qa1234')
        driver.find_element_by_id('userAccountPassword').submit()

    #   HEAD TO THE SEARCH PAGE
        time.sleep(2)
        driver.find_element_by_id('searchBtn').click()  # Search Panel

    #  ENTER LOCATIONS A & B
        time.sleep(2)
        driver.find_element_by_id('address0').send_keys('alpine')
        time.sleep(2)
        driver.find_element_by_id('address0').send_keys(Keys.RETURN)
        driver.find_element_by_id('address1').send_keys('Denver, CO')
        time.sleep(2)
        driver.find_element_by_id('address1').send_keys(Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_id('pickARouteSearchBtn').click()

    #  SAVE THE LINK
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="leftPanelContent"]/div/div[3]/a').click() # Clicking the save this link

    #  CLICK SUBMIT
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="save-route-form"]/button').submit() # Clicking the submit button

    #   ASSERT THE SAVE FUNCTION WORKED AND WE ARE NOW ON THE 'FAVORITES' PAGE
        time.sleep(10)
        assert (driver.find_element_by_id("favorites-content-area").is_displayed()), 'Event Edits Creation Button Is Not Displayed' # Did we make it to the 'Favorites' page

        driver.save_screenshot('screen2.png')


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()