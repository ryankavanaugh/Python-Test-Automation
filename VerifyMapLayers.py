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
from pprint import pprint
# -*- coding: utf-8 -*-


class Verify_Idaho_Layers(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://hb.511.idaho.gov/#roadReports?timeFrame=TODAY&layers=roadReports%2CwinterDriving%2CweatherWarnings%2CotherStates')


    def test_presence_of_correct_layers(self):

        driver = self.driver
        driver.maximize_window()

        dropDownMenuWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'layers-menu-dropdown-button')))
        driver.find_element_by_id('layers-menu-dropdown-button').click()

        #=================== Road Reports Verification
        # Idaho: CHECKED √
        menuItemsWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layerSelector"]/ul/li[1]/a/span/img[1]')))
        roadReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[1]')
        roadReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", roadReports)
        self.assertIn('images/checkbox-checked.png', roadReportsOuterHTMLData)

        #=================== Winter Driving Verification
        # Idaho: CHECKED √
        winterDrivingReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[2]')
        winterDrivingOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", winterDrivingReports)
        self.assertIn('images/checkbox-checked.png', winterDrivingOuterHTMLData)

        #=================== Weather Warnings Verificationp
        # Idaho: CHECKED √
        weatherWarningsReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[3]')
        weatherWarningsReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", weatherWarningsReports)
        self.assertIn('images/checkbox-checked.png', weatherWarningsReportsOuterHTMLData)

        #=================== Traffic Speeds Verification
        # Idaho: UNCHECKED
        trafficSpeedsReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[4]')
        trafficSpeedsReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", trafficSpeedsReports)
        self.assertIn('images/checkbox-unchecked.png', trafficSpeedsReportsOuterHTMLData)

        # =================== Electronic Signs Verification
        # Idaho: UNCHECKED
        eSignsReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[5]')
        eSignsReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", eSignsReports)
        self.assertIn('images/checkbox-unchecked.png', eSignsReportsOuterHTMLData)

        # =================== Mountain Passes Verification
        # Idaho: UNCHECKED
        mountainPassesReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[6]')
        mountainPassesReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", mountainPassesReports)
        self.assertIn('images/checkbox-unchecked.png', mountainPassesReportsOuterHTMLData)

        # =================== Camera Verification
        # Idaho: UNCHECKED
        cameraReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[7]')
        cameraReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", cameraReports)
        self.assertIn('images/checkbox-unchecked.png', cameraReportsOuterHTMLData)

        # =================== Weather Stations Verification
        # Idaho: UNCHECKED
        weatherStationsReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[8]')
        weatherStationsReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", weatherStationsReports)
        self.assertIn('images/checkbox-unchecked.png', weatherStationsReportsOuterHTMLData)

        # =================== Rest Areas Verification
        # Idaho: UNCHECKED
        restAreasReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[9]')
        restAreasReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", restAreasReports)
        self.assertIn('images/checkbox-unchecked.png', restAreasReportsOuterHTMLData)

        # =================== Other States' Info Verification
        # Idaho: CHECKED √
        otherStatesReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[10]')
        otherStatesReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", otherStatesReports)
        self.assertIn('images/checkbox-checked.png', otherStatesReportsOuterHTMLData)

        # =================== Transit Routes Verification
        # Idaho: UNCHECKED
        transitRoutesReports = driver.find_element_by_xpath('//*[@id="layerSelector"]/ul/li[11]')
        transitRoutesReportsOuterHTMLData = driver.execute_script("return arguments[0].outerHTML;", transitRoutesReports)
        self.assertIn('images/checkbox-unchecked.png', transitRoutesReportsOuterHTMLData)


    def tearDown(self):
         print "Test Completed"
         self.driver.quit()


if __name__ == '__main__':
    print ('\n') + "Verifying Idaho TG Web Map Layers" + '\n'
    unittest.main()