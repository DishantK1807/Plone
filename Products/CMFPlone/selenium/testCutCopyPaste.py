from Products.CMFPlone.selenium.base import SeleniumTestCase

class TestCutPaste(SeleniumTestCase):

    def test_cut_and_paste(self):
        self.login('member1','secret')
        self.click("link=Folder 1")
        self.click("link=Contents")
        self.click("#cb_folder-3")
        self.click("folder_cut:method")
        self.click("link=Folder 2")
        self.click("link=Contents")
        self.click("folder_paste:method")

    def test_copy_and_paste(self):
        self.login('member1','secret')
        self.click("link=Folder 1")
        self.click("link=Contents")
        self.click("#cb_folder-3")
        self.click("folder_copy:method")
        self.click("link=Folder 2")
        self.click("link=Contents")
        self.click("folder_paste:method")
