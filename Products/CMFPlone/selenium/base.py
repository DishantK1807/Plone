import transaction
import unittest2

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing import selenium_layers as layers
from plone.app.testing.helpers import applyProfile


class SeleniumTestCase(unittest2.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def open(self, path="/"):
        # ensure we have a clean starting point
        transaction.commit()
        portal = self.layer['portal']
        self.driver.get("%s%s" % (portal.absolute_url(), path))

    def login(self, username=TEST_USER_NAME, password=TEST_USER_PASSWORD):
        self.open('/login_form')
        self.driver.find_element_by_name('__ac_name').send_keys(username)
        self.driver.find_element_by_name('__ac_password').send_keys(password)
        self.driver.find_element_by_name('submit').click()
        
        
    
    '''
    Convenience functions
    If you record the selenium tests in Firefox IDE and then export as web driver
    junit format, you should be able to replace "selenium." with "self.". It's 
    not a catch all but should help a bit.
    '''
    def click(self, xpath):
        if xpath.count("link="):
            link = xpath.split("link=")[-1]
            element = self.driver.find_element_by_partial_link_text(link)
        elif xpath.count("//"):
            element = self.driver.find_element_by_xpath(xpath)
        elif xpath.count('#'):
            eleName = xpath.split("#")[-1]
            element = self.driver.find_element_by_id(eleName)
        else:
            element = self.driver.find_element_by_name(xpath)
        
        element.click()
        
    def type(self, name, value):
        self.driver.find_element_by_name(name).send_keys(value)
        
    def select(self, xpath1, xpath2=''):
        xpath = xpath1
        if xpath2:
            xpath = "%s['%s']"%(xpath1, xpath2)
            xpath = xpath.replace("select['label=", "select/option['attribute::value=")
        self.driver.find_element_by_xpath(xpath).set_selected()
        
    def waitForPageToLoad(self, foo):
        # this does nothing but make us lazy folks happy
        pass
        
    def publish(self):
        self.click("//dl[@id='plone-contentmenu-workflow']/dt/a")
        self.click("#workflow-transition-publish") 

