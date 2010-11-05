from Products.CMFPlone.selenium.base import SeleniumTestCase
import time

class TestPortlets(SeleniumTestCase):    
    
    def test_add_static_portlet(self):
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.login('manager', 'secret')
        self.open('/')
        # create a test folder
        self.click("//dl[@id='plone-contentmenu-factories']/dt/a")
        self.click("#folder")
        self.type("title", "test")
        self.click("form.button.save")
        self.click("link=Manage portlets")
        
        # add a static header portlet
        self.select("//option[attribute::value='/++contextportlets++plone.rightcolumn/+/plone.portlet.static.Static']")
        self.typeMce("nom nom nom")
        self.type("form.header", "Better Header")
        self.type("form.footer", "I'll eat pancakes on your grave")
        self.click("form.actions.save")
        self.click("link=test")
        
        # confirm that the portlet is there
        assert(self.driver.find_element_by_class_name('portlet-static-better-header'))
        self.click("link=Manage portlets")
        # block nav portets
        self.select("//div[@id='portletmanager-plone-rightcolumn']/div[3]/form/div[1]/select", "label=Block")
        self.click("//div[@id='portletmanager-plone-rightcolumn']/div[3]/form/div[4]/input") # save
        
        # add navigation portlet at root
        self.click("//span[@id='breadcrumbs-home']/a")
        self.click("link=Manage portlets")
        self.select("//option[attribute::value='/++contextportlets++plone.rightcolumn/+/portlets.Navigation']")
        
        # not sure why but it seems that I need to put a pause in here for
        # this to work
        time.sleep(2)
        
        self.type("form.name", "Navigation Station")
        self.clear('form.topLevel')
        self.type("form.topLevel", "0")
        self.click("form.actions.save")
        self.click("link=Home")
        assert(self.driver.find_element_by_class_name('portletNavigationTree'))
        self.click("link=test")
        assert(not self.driver.find_elements_by_class_name('portletNavigationTree'))
        
        # edit an existing portlet
        self.click("link=Manage portlets")
        self.click("link=Better Header")
        self.click("form.omit_border")
        self.click("form.actions.save")
        self.click("link=test")
        # this path doesn't exist with a border turned on
        assert(self.driver.find_elements_by_xpath("//div[@class='portletStaticText portlet-static-better-header']/p"))
        
