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
# -*- coding: utf-8 -*-

class Verify_Idaho_Links(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://hb.511.idaho.gov/#roadReports?timeFrame=TODAY&layers=roadReports%2CwinterDriving%2CweatherWarnings%2CotherStates')
        # print ('\n') + "Test verifying Idaho's TG Web's Topbar Menu links" + ('\n')


    def test_a_idaho_menu_buttons_without_dropdown_links(self, windows_handles=None):

        print '\n' + "Verifying: 511 -> Top bar links w/o dropdown options (streamlined version, mobile version, & truckers' info)"

        driver = self.driver
        driver.maximize_window()

        # Login To The System

        # while this element is not present
        loginElement = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'sign-in-link')))
        driver.find_element_by_id('sign-in-link').click()
        driver.find_element_by_id('userAccountEmail').send_keys('ryan.kavanaugh@crc-corp.com')
        driver.find_element_by_id('userAccountPassword').send_keys('qa1234')
        driver.find_element_by_id('userAccountPassword').submit()

        # Check that the menu items are all present
        left_Panel_Wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))
        driver.find_element_by_xpath("//*[contains(text(), 'Streamlined Version')]").click()
        driver.find_element_by_xpath("//*[contains(text(), 'Mobile Version')]").click()

        # Streamlined Version
        driver.switch_to.window(driver.window_handles[-1])
        title = driver.title
        assert title == 'Idaho Transportation Department - Low Bandwidth Web - Road Reports'
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

        # Mobile Version
        driver.switch_to.window(driver.window_handles[-2])
        assert driver.find_element_by_xpath("//*[contains(text(), 'Smartphone App available now')]").is_displayed()
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

        # Truckers Info
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_xpath("//*[contains(text(), \"Truckers' Info\")]").click()
        truckerTitle = driver.title
        assert truckerTitle == 'Idaho Transportation Department Trucker Information'

    #   ===========================================================================================
    #                          Test the '511' Topbar Menu Dropdown links
    #   ===========================================================================================

    def test_b_511_link_511_about(self, windows_handles=None):

        print '\n' + "Verifying: 511 -> About"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), '511 Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        aboutLink = driver.find_element_by_xpath("//*[contains(text(), 'ABOUT')]")
        actions.move_to_element(aboutLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        assert driver.find_element_by_xpath(
            "//*[contains(text(), 'About 511/FAQ')]").is_displayed(), "The 511 About page link is not operating properly"


    def test_c_511_link_511_phone_help(self, windows_handles=None):

        print '\n' + "Verifying: 511 -> Phone Help"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), '511 Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        phoneHelp = driver.find_element_by_xpath("//*[contains(text(), 'HELP')]")
        actions.move_to_element(phoneHelp).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        assert driver.find_element_by_xpath(
            "//*[contains(text(), '511 PHONE HELP')]").is_displayed(), "The 511 Phone Help link is not operating properly"


    def test_d_511_link_your_511(self, windows_handles=None):

        print '\n' + "Verifying: 511 -> Your 511"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), '511 Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        your511 = driver.find_element_by_xpath("//*[@id='ddsubmenu1']/li[3]/a/i")

        actions.move_to_element(your511).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        title = driver.title

        assert title == 'Your 511 Help', "The Your 511 Phone Help link is not operating properly"


    def test_e_511_tourist_info_airports(self, windows_handles=None):

        print '\n' + "Verifying: Tourist Info -> Airports"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Tourist Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        airportsLink = driver.find_element_by_xpath("//*[contains(text(), 'Airports')]")
        actions.move_to_element(airportsLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        airportsTitle = driver.title

        assert airportsTitle == 'Aeronautics | Idaho Transportation Department', 'The Airports page link did not open properly'


    def test_f_511_tourist_info_rest_areas(self, window_handles=None):

        ###   7   7   7   7   7   7   7   7   7   7   7   7   7   7   7   7
        ###                   RELATIVE      X-PATH
        ###   7   7   7   7   7   7   7   7   7   7   7   7   7   7   7   7

        print '\n' +  "Verifying: Tourist Info -> Rest Areas"

        driver = self.driver
        driver.maximize_window

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Tourist Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        restAreasLink = driver.find_element_by_xpath("//*[@id='ddsubmenu2']/li[2]/a")
        actions.move_to_element(restAreasLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        restAreasTitle = driver.title

        assert restAreasTitle == 'Road Maintenance | Idaho Transportation Department', 'The Rest Areas page link did not work correctly'


    def test_g_511_tourist_info_scenic_byways(self, windows_handles=None):

        print '\n' +  "Verifying: Tourist Info -> Scenic Byways"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Tourist Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        airportsLink = driver.find_element_by_xpath("//*[contains(text(), 'Scenic Byways')]")
        actions.move_to_element(airportsLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        scenicBywaysTitle = driver.title

        assert scenicBywaysTitle == 'Idaho Scenic Byways/Backcountry Drives | Visit Idaho', 'The Scenic Byways page link did not operate properly'


    def test_h_511_tourist_info_tourism(self, windows_handles=None):

        print '\n' +  "Verifying: Tourist Info -> Tourism"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Tourist Info')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        tourismLink = driver.find_element_by_xpath("//*[contains(text(), 'Tourism')]")
        actions.move_to_element(tourismLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        tourismPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Official Vacation & Travel Guide')]")))

        tourismTitle = driver.title

        assert tourismTitle == 'Visit Idaho | Official Vacation & Travel Guide', "The 'Tourism' page link did not operate properly"


    def test_i_511_links_contact_id(self, windows_handles=None):

        print '\n' + "Verifying: Links -> Contact ID"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Contact ITD')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        contactIDPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID , 'Comment_ResponseRequested_flag')))

        contactIDTitle = driver.title

        assert contactIDTitle == 'Idaho Transportation Department Comments', 'The Contact ID page link did not operate properly'


    def test_j_511_links_adjacent_areas(self, windows_handles=None):

        print '\n' + "Verifying: Links -> Adjacent Areas"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Adjacent Areas')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        adjacentAreasPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Idaho Transportation Department')]")))

        adjacentAreasTitle = driver.title

        assert adjacentAreasTitle == 'Idaho Transportation Department - Low Bandwidth Web - Updates', 'The Adjacent page link did not load properly'


    def test_k_511_links_amber_alerts(self, windows_handles=None):

        print '\n' + "Verifying: Links -> AMBER Alerts"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'AMBER Alerts')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        amberAlertsPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'MAKE THE WORLD SAFER FOR KIDS.')]")))

        assert driver.find_element_by_xpath("//*[contains(text(), 'MAKE THE WORLD SAFER FOR KIDS.')]").is_displayed(), 'The Amber Alerts page link did not load properly'


    def test_l_511_links_ada_county(self, windows_handles=None):

        print '\n' + "Verifying: Links -> Ada County Area Traffic"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Ada County Area Traffic')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        adaCountyPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Ada County Highway District Traffic Information')]")))

        adaCountyTitle = driver.title

        assert adaCountyTitle == 'Ada County Highway District Traffic Information', 'The Adjacent page link did not load properly'


    def test_m_511_links_national_fire(self, windows_handles=None):

        print '\n' + "Verifying: Links -> National Interagency Fire Ctr"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'National Interagency Fire Ctr')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        nationalFirePageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'National Interagency Fire Center')]")))

        nationalFireTitle = driver.title

        assert nationalFireTitle == 'National Interagency Fire Center', 'The National Interagency Fire Ctr page link did not load properly'


    def test_n_511_links_national_weather_service(self, windows_handles=None):

        print '\n' + "Verifying: Links -> National Weather Service"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'National Weather Service')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        nationalWeatherPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Western Region Headquarters')]")))

        nationalWeatherServiceTitle = driver.title

        assert nationalWeatherServiceTitle == 'Western Region Headquarters', 'The National Weather Service page link did not load properly'


    def test_o_511_links_roadway_weather_forecasts(self, windows_handles=None):

        print '\n' + "Verifying: Links -> National Roadway Weather Forecasts"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Roadway Weather Forecasts')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        roadwayWeatherPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'National Weather Service - NWS Pocatello')]")))

        roadwayWeatherTitle = driver.title

        assert roadwayWeatherTitle == 'National Weather Service - NWS Pocatello', 'The National Roadway Weather Forecasts page link did not load properly'


    def test_p_511_links_I15_construction(self, windows_handles=None):

        print '\n' + "Verifying: Links -> I15 Construction"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'I-15 Construction')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        i15PageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'I-15 Construction |  Idaho Transportation Department')]")))

        i5Title = driver.title

        assert i5Title == 'I-15 Construction | Idaho Transportation Department', 'The I15 Construction page link did not load properly'


    def test_q_511_links_wildfire_info(self, windows_handles=None):

        print '\n' + "Verifying: Links -> Wildfire Info (GEOMAC)"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Wildfire Info (GEOMAC)')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        wildfirePageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'GeoMAC Wildfire')]")))

        wildfireInfoTitle = driver.title

        assert wildfireInfoTitle == 'GeoMAC Wildfire Application', 'The Wildfire Info (GEOMAC) page link did not load properly'


    def test_r_511_links_bike_map(self, windows_handles=None):

        print '\n' + "Verifying: Links -> Bike Map"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Bike Map')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)

        bikeMapURL = driver.current_url

        assert bikeMapURL.__contains__(".pdf"), 'The Bike Map page link did not load properly'


    def test_s_511_links_Iway(self, windows_handles=None):

        print '\n' + "Verifying: Links -> I-Way"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'I-Way')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        iWayPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.ID, 'social_media')))

        assert driver.find_element_by_id('social_media').is_displayed(), 'The I-Way page link did not load properly'


    def test_t_511_links_transporting_a_boat(self, windows_handles=None):

        print '\n' + "Verifying: Links -> Transporting a Boat"

        driver = self.driver
        driver.maximize_window()

        actions = ActionChains(driver)

        menu = driver.find_element_by_xpath("//*[contains(text(), 'Links')]")
        actions.move_to_element(menu).perform()

        time.sleep(3)

        contactIDLink = driver.find_element_by_xpath("//*[contains(text(), 'Transporting a Boat')]")
        actions.move_to_element(contactIDLink).click().perform()

        driver.switch_to.window(driver.window_handles[-1])

        transABoatPageVerification = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Pacific States Marine Fisheries Commission')]")))

        transBoatTitle = driver.title

        assert transBoatTitle == 'Pacific States Marine Fisheries Commission', 'The Transporting a Boat page link did not load properly'


    def tearDown(self):
         print self.driver.title
         print "Test Completed"
         self.driver.quit()


if __name__ == '__main__':
    print ('\n') + "Test verifying Idaho's TG Web Topbar Menu links"
    unittest.main()