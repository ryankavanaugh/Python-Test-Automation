from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
import json
import requests

# /Users/ryankavanaugh/Desktop/QA1/TG\ Web\ Automated\ Tests\ 2017/MDSS\ Update/
# Make sure this test only goes to staging and does not hit prod
class Verify_MDSS_Data(unittest.TestCase):

    def test_mdss_data(self):

        # Get auth token from API
        url = 'http://mn.carsstage.org/segments_v1/api/authTokens'
        myResponse = requests.post(url, json={'userName': 'ryan', 'password': 'qa'})
        jData = json.loads(myResponse.content)
        AuthID = jData.get('id')

        # Post a new snow event to the API
        currentConditionsAPIURL = 'http://mn.carsstage.org/segments_v1/api/currentConditions'
        headers = {'x-crc-authToken':AuthID, 'Accept':'application/json'} #, 'text':'javascript'}
        currentConditionsResponse = requests.post(currentConditionsAPIURL, headers=headers, json={"segmentIds":[149],"conditions":[{"categoryId":1,"conditionIds":[3]},{"categoryId":3,"conditionIds":[13]}]})
        #print currentConditionsResponse

        # Link to TG WEB Staging API, open up TG WEB Winter Conditions Road Report
        TGWEBURL = 'http://mnwebtg.carsstage.org/tgevents/api/eventMapFeatures/'
        tgWebDict = {}
        driver = webdriver.Chrome()
        driver.get(TGWEBURL)

        # Get all the json from the API
        data = driver.find_element_by_tag_name('body').text
        jsonData = json.loads(data)

        # Get only road reports
        for item in jsonData:
            IDNum = item.get('id')
            toolTip = item.get('tooltip')
            tgWebDict[IDNum] = toolTip

        # Assert MDSS data is a part of Winter Driving Events
        for roadReportsNum in tgWebDict:
            if 'Roadway is completely covered with snow.' in tgWebDict[roadReportsNum]:
                roadReportsURL = 'http://mnwebtg.carsstage.org/#roadReports/eventAlbum/' + str(roadReportsNum) + '?timeFrame=TODAY&layers=winterDriving%2CvoxReports%2Cflooding'
                driver.get(roadReportsURL)
                mdssWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='slider']/div/div/div[2]/div/div[1]/div[1]/div[2]/div")))

                textBox = driver.find_element_by_xpath("//*[@id='slider']/div/div/div[2]/div/div[1]/div[1]/div[2]/div")
                assert ('Last updated' in textBox.text)

        driver.quit()

        # Delete the event
        currentConditionsDeletion = requests.post(currentConditionsAPIURL, headers=headers, json={"segmentIds": [1052], "deleteCurrentConditionsOnly": True})

if __name__ == '__main__':
    unittest.main()

