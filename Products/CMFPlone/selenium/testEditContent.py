from Products.CMFPlone.selenium.base import SeleniumTestCase

class TestEditContent(SeleniumTestCase):

    def test_edit_content(self):
        self.login('member1','secret')
        self.click("link=Folder 1")
        self.click("link=Edit")
        self.clear("title")
        self.type("title", "Some say potato")
        self.click("form.button.save")
