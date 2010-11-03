from Products.Five.testbrowser import Browser
from Products.PloneTestCase import ptc

ptc.setupPloneSite(id=ptc.portal_name)
ptc.setupPloneSite(id='login_portal')

class TestSSOLogin(ptc.FunctionalTestCase):
    """ This is a base class for functional test cases for your custom product.
    """

    def afterSetUp(self):
        ptc.FunctionalTestCase.afterSetUp(self)

        self.browser = Browser()
        self.browser.handleErrors = False # Don't get HTTP 500 pages

        self.login_portal = self.app.login_portal # logins go here
        self.login_portal.acl_users.userFolderAddUser(ptc.default_user, ptc.default_password, ['Member'], [])

        self.login_portal.portal_properties.site_properties._updateProperty(
            'allow_external_login_sites', [self.portal.absolute_url()]
            )

        self.login_url = "%s/require_login?next=%s/acl_users/session/external_login" % (
            self.login_portal.absolute_url(),
            self.portal.absolute_url(),
            )
        self.portal.acl_users.credentials_cookie_auth.login_path = self.login_url
        self.portal.portal_actions.user.login._updateProperty(
            'url_expr', "python:portal.acl_users.credentials_cookie_auth.getProperty('login_path')"
            )

        for portal in (self.portal, self.login_portal):
            session = portal.acl_users.session
            session._shared_secret = 'secret'
            session.path = portal.absolute_url_path()

    def test_loginWithSSO(self):
        browser = self.browser
        browser.open(self.portal.absolute_url())
        browser.getLink('Log in').click()
        browser.getControl(name='__ac_name').value = ptc.default_user
        browser.getControl(name='__ac_password').value = ptc.default_password
        browser.getControl(name='submit').click()
        self.assertEqual(self.browser.cookies.getinfo('__ac')['path'], self.login_portal.absolute_url_path())
        # Without javascript we must click through
        browser.getForm('external_login_form').submit()
        self.assertEqual(self.browser.cookies.getinfo('__ac')['path'], self.portal.absolute_url_path())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSSOLogin))
    return suite
