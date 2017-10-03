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
import bs4
import urllib2
from BeautifulSoup import BeautifulSoup
import requests
# -*- coding: utf-8 -*-


class Verify_Idaho_Links(unittest.TestCase):


    def test_idaho_tg_web_topbar_links(self):
        strList = []
        httpLinkList = []

        url = 'http://hb.511.idaho.gov/'
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page)

        allPageLinks = soup.findAll('a', href=True)

        for link in allPageLinks:
            strList.append(str(link['href']))

        for realLink in strList:
            if realLink.startswith('http'):
                httpLinkList.append(realLink)

        counter = 0

        for item in httpLinkList:
            try:
                r = requests.head(item)
                #print r.status_code
                if r.status_code != 200: # and r.status_code != 301 and r.status_code != 302:
                    print r.status_code
                    print item
                    counter =+1
            except:
                print "failed to connect"
                counter =+ 1

        if counter > 0:
            assert False

if __name__ == '__main__':
    unittest.main()