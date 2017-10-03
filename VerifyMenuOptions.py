# coding=utf-8
from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
import time
import unittest
# -*- coding: utf-8 -*-

class Verify_Idaho_Menu_Options(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
       # self.driver.get('http://idwebtg.carsstage.org/#roadReports?timeFrame=TODAY&layers=roadReports%2CwinterDriving%2CweatherWarnings%2CotherStates')
        self.driver.get('http://hb.511.idaho.gov/#roadReports?timeFrame=TODAY&layers=roadReports%2CwinterDriving%2CweatherWarnings%2CotherStates')
        print ('\n') + "Test Verifying Idaho TG Web Left Side Menu Options"


    def test_idaho_menu(self):

        driver = self.driver

        # Login To The System
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'sign-in-link')))
        driver.find_element_by_id('sign-in-link').click()
        driver.find_element_by_id('userAccountEmail').send_keys('ryan.kavanaugh@crc-corp.com')
        driver.find_element_by_id('userAccountPassword').send_keys('qa1234')
        driver.find_element_by_id('userAccountPassword').submit()

        # Check that the menu items are all present
        left_Panel_Wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))
        # Personalize your 511
        assert (driver.find_element_by_xpath('//*[@title="Ryan’s Favorites"]').is_displayed()) == True, "Favorites not present"
        # All Reports
        assert driver.find_element_by_xpath('//*[@title="See all traffic reports and winter driving conditions"]').is_displayed(), "All Reports not present"
        # Google Traffic
        assert driver.find_element_by_xpath('//*[@title="See up-to-date traffic conditions"]').is_displayed(), "Google Traffic not present"
        # Cameras
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of cameras and view camera images"]').is_displayed(), "Cameras not present"
        # Weather Stations
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of weather stations and review weather data"]').is_displayed(), "Weather Stations not present"
        # Electronic Signs
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of signs"]').is_displayed(), "Electronic Signs not present"
        # Transit Routes
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of bus routes and positions"]').is_displayed(), "Transit Routes not present"
        # Mountain Passes
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of mountain passes"]').is_displayed(), "Mountain Passes not present"
        # Twitter
        assert driver.find_element_by_xpath('//*[@title="Follow area Twitter feeds to get traffic alerts"]').is_displayed(), "Twitter not present"


        # Check that the menu options that open a new panel are functioning properly
        # Favorites
        driver.find_element_by_xpath('//*[@title="Ryan’s Favorites"]').click()
        assert driver.find_element_by_id('favorites-content-area').is_displayed()
        time.sleep(1)
        home_Button_Wait = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'homeBtn')))
        home_Button_Wait.click()

        # Wait for main menu to load
        left_Panel_Wait2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))

        # Transit Routes
        driver.find_element_by_xpath('//*[@title="See maps and lists of bus routes and positions"]').click()
        assert driver.find_element_by_id('address0').is_displayed()
        time.sleep(1)
        home_Button_Wait.click()

        # Wait for main menu to load
        left_Panel_Wait3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))
        #time.sleep(3)
        # Twitter
        driver.find_element_by_xpath('//*[@title="Follow area Twitter feeds to get traffic alerts"]').click()
        time.sleep(1)
        left_Panel_WaitTwitter = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'feedGroupsContainer')))
        assert ('Traffic Alerts via Twitter') in driver.page_source, "The twitter panel is not displayed"


    def tearDown(self):
         print '\n' + "Test Completed"
         self.driver.quit()


if __name__ == '__main__':
    unittest.main()