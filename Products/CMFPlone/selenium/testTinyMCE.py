import unittest2
from plone.app.testing import selenium_layers as layers
from plone.app.testing.interfaces import TEST_USER_NAME, TEST_USER_PASSWORD

class TinyMCE(unittest2.TestCase):
    layer = layers.SELENIUM_TESTING

    def getTestUserDriver(self):
        driver = self.layer['selenium']
        portal = self.layer['portal']
        driver.get(portal.absolute_url()+'/login_form')
        driver.find_element_by_name('__ac_name').send_keys(TEST_USER_NAME)
        driver.find_element_by_name('__ac_password').send_keys(TEST_USER_PASSWORD)
        driver.find_element_by_name('submit').click()
        return driver


    def testAddImage(self):
        driver = self.getTestUserDriver()
