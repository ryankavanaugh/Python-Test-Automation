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
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest
#from pyvirtualdisplay import Display
# -*- coding: utf-8 -*-


class Verify_Login_And_Saving_Routes(unittest.TestCase):
    def setUp(self):
        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()
        self.driver = webdriver.Chrome()
        print '\n' + "Test for Idaho: Verifying login feature" + '\n'
        self.driver.get("http://hb.511.idaho.gov/")


    def test_login_route_creation_and_deletion(self):

        driver = self.driver
        driver.maximize_window()

        loginElement = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'sign-in-link')))
        driver.find_element_by_id('sign-in-link').click()
        loginElement2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'userAccountEmail')))
        driver.find_element_by_id('userAccountEmail').send_keys('ryan.kavanaugh@crc-corp.com')
        driver.find_element_by_id('userAccountPassword').send_keys('qa1234')
        driver.find_element_by_id('userAccountPassword').submit()

        left_Panel_Wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))
        assert driver.find_element_by_xpath("//*[contains(text(), 'Ryan’s 511')]")


    def tearDown(self):
        print '\n' + "Test Completed"
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()