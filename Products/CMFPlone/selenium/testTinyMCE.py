from Products.CMFPlone.selenium.base import SeleniumTestCase


class TinyMCE(SeleniumTestCase):

    def testAddImage(self):
        self.login()
