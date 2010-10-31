import transaction
from plone.app.testing.layers import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING
from Products.CMFPlone.selenium.base import SeleniumTestCase

class TestCollections(SeleniumTestCase):
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']
        
        # Set a default workflow for the site
        self.portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        for m in range(1,3):
            self.portal.invokeFactory('Folder', 'folder%s' % m, title='Folder %s' % m)
            for n in range(0,10):
                self.portal['folder%s' % m].invokeFactory('Event', 'event%s' % n, title='Event %s' % n)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
    
    def open(self, path="/"):
        # ensure we have a clean starting point
        transaction.commit()
        self.driver.get("%s%s" % (self.portal.absolute_url(), path))
    
    def test_add_collection(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.login()
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
        options = {'CreationDate': 'Creation Date',
                   'Creator': 'Creator',
                   'Description': 'Description',
                   'EffectiveDate': 'Effective Date',
                   'end': 'End Date',
                   'ExpirationDate': 'Expiration Date',
                   'getId': 'Short Name',
                   'getObjSize': 'Size',
                   'location': 'Location',
                   'ModificationDate': 'Modification Date',
                   'review_state': 'State',
                   'start': 'Start Date',
                   'Subject': 'Tags',
                   'Type': 'Item Type'}
        
        for opt in options.keys():
            self.driver.find_element_by_xpath("id('customViewFields_options')/option[attribute::value='%s']" % opt).set_selected()

        self.driver.find_element_by_xpath("//input[attribute::value='>>']").click()
        
        # Save the collection
        self.driver.find_element_by_name('form.button.save').click()

        # Publish it
        self.driver.find_element_by_partial_link_text('Private').click()
        self.driver.find_element_by_partial_link_text('Publish').click()
        self.assertIn('Published', self.driver.get_page_source())
        
        # Add a title criteria
        self.driver.find_element_by_link_text('Criteria').click()
        self.driver.find_element_by_xpath("id('field')/option[attribute::value='Title']").set_selected()
        self.driver.find_element_by_name("form.button.AddCriterion").click()
        self.driver.find_element_by_name("crit__Title_ATSimpleStringCriterion_value").send_keys("Event")
        self.driver.find_element_by_name("form.button.Save").click()
        self.assertTrue("Changes saved." in self.driver.get_page_source())
        
        # View the collection
        self.driver.find_element_by_link_text("View").click()
        
        # Check that all table columns requested are displayed
        for opt in options.values():
            self.assertIn(opt, self.driver.get_page_source())

        # Return the list of results
        def getCollectionResults(self):
            return self.driver.find_elements_by_xpath("//table[attribute::class='listing']/tbody/tr")
        
        # Make sure we find all 20 events
        self.assertEquals(len(getCollectionResults(self)), 20)
        
        