from Products.CMFPlone.selenium.base import SeleniumTestCase

class TestCollections(SeleniumTestCase):

    def test_add_collection(self):
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])
        self.login('manager', 'secret')
        self.open('/')
        
        # Add a new collection
        self.driver.find_element_by_partial_link_text('Add new').click()
        self.driver.find_element_by_partial_link_text('Collection').click()
        
        # Define title, description
        self.driver.find_element_by_name('title').send_keys('I am a collection with javascript')
        self.driver.find_element_by_name('description').send_keys('skkep skip skop')
        
        # Display as Table
        self.driver.find_element_by_id('customView').click()
        
        # Select all available table columns for viewing    
        options = ['CreationDate',
                   'Creator',
                   'Description', 
                   'EffectiveDate',
                   'end', 
                   'ExpirationDate', 
                   'getId', 
                   'getObjSize', 
                   'location',
                   'ModificationDate', 
                   'review_state', 
                   'start', 
                   'Subject',
                   'Type']
        
        for opt in options:
            self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='%s']" % opt).set_selected()

        self.driver.find_element_by_xpath("//input[attribute::value='>>']").click()
        
        # Save the collection
        self.driver.find_element_by_name('form.button.save').click()
