import transaction
import unittest2

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing import selenium_layers as layers


class SeleniumTestCase(unittest2.TestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
    
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

