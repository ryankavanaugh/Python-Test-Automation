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

class Verify_Login_And_Saving_Routes(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        print '\n' + "Test for ID: Verifying login and saving routes features" + '\n'


    def test_login_route_creation_and_deletion(self):

        driver = self.driver
        driver.maximize_window()

    #   HEAD TO CO WEBSITE
        driver.get("http://hb.511.idaho.gov/#roadReports?timeFrame=TODAY&layers=roadReports%2CwinterDriving%2CweatherWarnings%2CotherStates")

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
        driver.find_element_by_id('searchBtn').click()

    #  ENTER LOCATIONS A & B
        time.sleep(2)
        driver.find_element_by_id('address0').send_keys('Idaho Falls, ID')
        time.sleep(2)
        driver.find_element_by_id('address0').send_keys(Keys.RETURN)
        driver.find_element_by_id('address1').send_keys('Sun Valley, ID')
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
        pageLoadWait = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "favorites-content-area")))
        assert (driver.find_element_by_id("favorites-content-area").is_displayed()), 'Event Edits Creation Button Is Not Displayed' # Did we make it to the 'Favorites' page


#        driver.save_screenshot('FavoritesPageScreenShot.png')

        routeHamburgerMenuWait = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="Customize and control Your 511"]')))

        driver.find_element_by_xpath('//*[@title="Customize and control Your 511"]').click()
        driver.find_element_by_xpath("//*[contains(text(), 'Delete this route')]").click()
        alert = driver.switch_to.alert.accept()

        keepRunningLoop = True

        while (keepRunningLoop):
            try:
                menuWait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="Customize and control Your 511"]')))
                driver.find_element_by_xpath('//*[@title="Customize and control Your 511"]').click()

                deleteWait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Delete this route')]")))
                driver.find_element_by_xpath("//*[contains(text(), 'Delete this route')]").click()
                alert = driver.switch_to.alert.accept()
            except:
                break


        try:
            driver.find_element_by_xpath('//*[@title="Customize and control Your 511"]').is_displayed()
            assert False
        except:
             assert True


    def tearDown(self):
        print '\n' + "Test Completed"
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()