import os
from App.Common import package_home

from Products.CMFPlone.selenium.base import SeleniumTestCase
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles


class TinyMCE(SeleniumTestCase):

    def testAddImage(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.login()
        self.open('/')

        # Add a new collection
        self.driver.find_element_by_partial_link_text('Add new').click()
        self.driver.find_element_by_partial_link_text('Page').click()
        self.driver.find_element_by_name('title').send_keys('Image Test')

        self.driver.find_element_by_id('text_image').click()
        self.driver.switch_to_frame('mce_44_ifr')
        self.driver.find_element_by_id('upload').click()

        path = os.path.join(package_home(globals()), 'input', 'test.gif')

        self.driver.find_element_by_id('uploadfile').send_keys(path)
        
        self.driver.find_element_by_id('uploadbutton').click()
        self.driver.find_element_by_id('insert').click()
        self.driver.find_element_by_name('form.button.save').click()

        self.assertIn('test.gif', self.driver.get_page_source())
