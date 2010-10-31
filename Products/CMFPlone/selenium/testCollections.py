from Products.CMFPlone.selenium.base import SeleniumTestCase

class TestCollections(SeleniumTestCase):

    def test_add_collection(self):
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.login('manager', 'secret')
        self.open('/')
        self.driver.find_element_by_partial_link_text('Add new').click()
        self.driver.find_element_by_partial_link_text('Collection').click()
        self.driver.find_element_by_name('title').send_keys('I am a collection with javascript')
        self.driver.find_element_by_name('description').send_keys('skkep skip skop')
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='CreationDate']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='Creator']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='Description']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='EffectiveDate']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='end']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='ExpirationDate']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='getId']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='getObjSize']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='location']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='ModificationDate']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='review_state']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='start']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='Subject']").set_selected()
        self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='Type']").set_selected()
        
