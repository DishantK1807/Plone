from Products.CMFPlone.selenium.base import SeleniumTestCase

class TestPortlets(SeleniumTestCase):    
    
    def test_add_static_portlet(self):
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.login('manager', 'secret')
        self.open('/')
        self.click("//dl[@id='plone-contentmenu-factories']/dt/a")
        self.click("#folder")
        self.type("title", "test")
        self.click("form.button.save")
        #self.publish()
        self.click("link=Manage portlets")
        self.select("//div[@id='portletmanager-plone-rightcolumn']/div[1]/form/select", "label=Static text portlet")
        self.type("form.header", "Better Header")
        self.type("form.footer", "I'll eat pancakes on your grave")
        self.click("link=Home")
        self.click("form.actions.save")
        self.click("link=test")
        self.click("link=Manage portlets")
        self.select("//div[@id='portletmanager-plone-rightcolumn']/div[3]/form/div[1]/select", "label=Block")
        self.click("//div[@id='portletmanager-plone-rightcolumn']/div[3]/form/div[4]/input")
        self.click("link=test")
        self.click("//span[@id='breadcrumbs-home']/a")
        self.click("link=Manage portlets")
        self.click("link=Better Header")
        self.click("form.omit_border")
        self.click("form.actions.save")
        self.click("link=Home")
        
