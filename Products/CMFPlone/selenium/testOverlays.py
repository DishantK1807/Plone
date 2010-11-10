from Products.CMFPlone.selenium.base import SeleniumTestCase
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from selenium.common.exceptions import NoSuchElementException
import time

class TestOverlays(SeleniumTestCase):

    def test_login_form(self):
        # Make sure we're logged out before starting
        self.open('/logout')
        self.open()
        
        self.driver.find_element_by_link_text('Log in').click()
        self.driver.find_element_by_name('__ac_name').send_keys('wrong')
        self.driver.find_element_by_name('__ac_password').send_keys('fail')
        self.driver.find_element_by_name('submit').click()
        self.assertIn('Login failed.', self.driver.get_page_source())
        
        self.driver.find_element_by_name('__ac_name').send_keys(TEST_USER_NAME)
        self.driver.find_element_by_name('__ac_password').send_keys(TEST_USER_PASSWORD)
        self.driver.find_element_by_name('submit').click()
        
        self.assertEquals(TEST_USER_ID, self.driver.find_element_by_id('user-name').get_text())
        
        self.assertRaises(NoSuchElementException, self.driver.find_element_by_id, 'login_form')
        
        