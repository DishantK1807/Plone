import transaction
import unittest2

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import PLONE_SITE_ID
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing import selenium_layers as layers
from plone.app.testing.helpers import applyProfile


class SeleniumTestCase(unittest2.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        self.baseurl = "http://%s:%s/%s" % (self.layer['host'],
                                            self.layer['port'],
                                            PLONE_SITE_ID)
        self.portal.acl_users._doAddUser('member1', 'secret',
                                         ['Member'], [])
        applyProfile(self.layer['portal'], 'Products.CMFPlone:plone-selenium')

    def open(self, path="/"):
        # ensure we have a clean starting point
        transaction.commit()
        portal = self.layer['portal']
        self.driver.get("%s%s" % (self.baseurl, path))

    def login(self, username=TEST_USER_NAME, password=TEST_USER_PASSWORD):
        self.open('/login_form')
        self.driver.find_element_by_name('__ac_name').send_keys(username)
        self.driver.find_element_by_name('__ac_password').send_keys(password)
        self.driver.find_element_by_name('submit').click()



    '''
    Convenience functions
    If you record the selenium tests in Firefox IDE and then export as web driver
    junit format, you should be able to replace "selenium." with "self.". It's
    not a catch all but should help quite a bit.
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
        
    def typeMce(self, value):
        '''
        Text fields with mce are different.We need to go into the frame and update the 
        p element to make this work. Unfortunately the code to get out of the frame is not 
        implemented in python yet. The workaround is to use this handle trick, which 
        is currently unsupported in chrome. See issue #405 for more. In general there
        are still a lot of open issues on frame support so if this breaks it won't 
        be a surprise.'''
        handle = self.driver.get_current_window_handle()
        self.driver.switch_to_frame("form.text_ifr")
        ele = self.driver.find_element_by_xpath("//p")
        ele.send_keys(value)
        self.driver.switch_to_window(handle)

    def clear(self, name):
        self.driver.find_element_by_name(name).clear()

    def select(self, xpath1, xpath2=''):
        xpath = xpath1
        if xpath2:
            xpath = "%s['%s']"%(xpath1, xpath2)
            xpath = xpath.replace("select['label=", "select/option['text()=")
        self.driver.find_element_by_xpath(xpath).set_selected()

    def waitForPageToLoad(self, foo):
        # this does nothing but make us lazy folks happy
        pass

    def publish(self):
        self.click("//dl[@id='plone-contentmenu-workflow']/dt/a")
        self.click("#workflow-transition-publish")
        
    def submit(self, formId):
        self.driver.find_element_by_id(formId).submit()
        

