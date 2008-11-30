"""
CMFPlone setup handlers.
"""

from borg.localrole.utils import setup_localrole_plugin
from five.localsitemanager import make_objectmanager_site
from plone.app.upgrade.utils import logger
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.app.component.interfaces import ISite
from zope.app.component.hooks import setSite
from zope.component import queryUtility
from zope.event import notify
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.locales import locales, LoadLocaleError
from zope.interface import implements

from Acquisition import aq_base, aq_get
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.lib import constraintypes
from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from Products.PlonePAS.plugins.local_role import LocalRolesManager
from Products.StandardCacheManagers.AcceleratedHTTPCacheManager import \
     AcceleratedHTTPCacheManager
from Products.StandardCacheManagers.RAMCacheManager import RAMCacheManager

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.events import SiteManagerCreatedEvent
from Products.CMFPlone.factory import _DEFAULT_PROFILE


class HiddenProducts(object):
    implements(INonInstallable)

    def getNonInstallableProducts(self):
        return [
            'Archetypes', 'Products.Archetypes',
            'ATContentTypes', 'Products.ATContentTypes',
            'ATReferenceBrowserWidget', 'Products.ATReferenceBrowserWidget',
            'CMFActionIcons', 'Products.CMFActionIcons',
            'CMFCalendar', 'Products.CMFCalendar',
            'CMFDefault', 'Products.CMFDefault',
            'CMFPlone', 'Products.CMFPlone',
            'CMFTopic', 'Products.CMFTopic',
            'CMFUid', 'Products.CMFUid',
            'DCWorkflow', 'Products.DCWorkflow',
            'PasswordResetTool', 'Products.PasswordResetTool',
            'PlonePAS', 'Products.PlonePAS',
            'kupu', 'Products.kupu',
            'PloneLanguageTool', 'Products.PloneLanguageTool',
            'Kupu', 'Products.Kupu',
            'CMFFormController', 'Products.CMFFormController',
            'MimetypesRegistry', 'Products.MimetypesRegistry',
            'PortalTransforms', 'Products.PortalTransforms',
            'CMFDiffTool', 'Products.CMFDiffTool',
            'CMFEditions', 'Products.CMFEditions',
            'plone.portlet.static',
            'plone.portlet.collection',
            'borg.localrole',
            'plone.keyring',
            'plone.protect',
            ]


class PloneGenerator:

    def installArchetypes(self, p):
        """QuickInstaller install of Archetypes and required dependencies."""
        qi = getToolByName(p, "portal_quickinstaller")
        qi.installProduct('Archetypes', locked=1, hidden=1,
            profile=u'Products.Archetypes:Archetypes')

    def installProducts(self, p):
        """QuickInstaller install of required Products"""
        qi = getToolByName(p, 'portal_quickinstaller')
        qi.installProduct('PlonePAS', locked=1, hidden=1, forceProfile=True)
        qi.installProduct('kupu', locked=0, forceProfile=True)
        qi.installProduct('CMFDiffTool', locked=0, forceProfile=True)
        qi.installProduct('CMFEditions', locked=0, forceProfile=True)
        qi.installProduct('PloneLanguageTool', locked=1, hidden=1, forceProfile=True)

    def installDependencies(self, p):
        st=getToolByName(p, "portal_setup")
        st.runAllImportStepsFromProfile("profile-Products.CMFPlone:dependencies")


    def addCacheHandlers(self, p):
        """ Add RAM and AcceleratedHTTP cache handlers """
        mgrs = [(AcceleratedHTTPCacheManager, 'HTTPCache'),
                (RAMCacheManager, 'RAMCache'),
                (RAMCacheManager, 'ResourceRegistryCache'),
                ]
        for mgr_class, mgr_id in mgrs:
            existing = p._getOb(mgr_id, None)
            if existing is None:
                p._setObject(mgr_id, mgr_class(mgr_id))
            else:
                unwrapped = aq_base(existing)
                if not isinstance(unwrapped, mgr_class):
                    p._delObject(mgr_id)
                    p._setObject(mgr_id, mgr_class(mgr_id))

    def addCacheForResourceRegistry(self, portal):
        ram_cache_id = 'ResourceRegistryCache'
        if ram_cache_id in portal.objectIds():
            cache = getattr(portal, ram_cache_id)
            settings = cache.getSettings()
            settings['max_age'] = 24*3600 # keep for up to 24 hours
            settings['request_vars'] = ('URL',)
            cache.manage_editProps('Cache for saved ResourceRegistry files', settings)
        reg = getToolByName(portal, 'portal_css', None)
        if reg is not None and getattr(aq_base(reg), 'ZCacheable_setManagerId', None) is not None:
            reg.ZCacheable_setManagerId(ram_cache_id)
            reg.ZCacheable_setEnabled(1)

        reg = getToolByName(portal, 'portal_kss', None)
        if reg is not None and getattr(aq_base(reg), 'ZCacheable_setManagerId', None) is not None:
            reg.ZCacheable_setManagerId(ram_cache_id)
            reg.ZCacheable_setEnabled(1)

        reg = getToolByName(portal, 'portal_javascripts', None)
        if reg is not None and getattr(aq_base(reg), 'ZCacheable_setManagerId', None) is not None:
            reg.ZCacheable_setManagerId(ram_cache_id)
            reg.ZCacheable_setEnabled(1)

    def setProfileVersion(self, portal):
        setup = getToolByName(portal, 'portal_setup')
        version = setup.getVersionForProfile(_DEFAULT_PROFILE)
        setup.setLastVersionForProfile(_DEFAULT_PROFILE, version)

    def enableSyndication(self, portal, out):
        syn = getToolByName(portal, 'portal_syndication', None)
        if syn is not None:
            syn.editProperties(isAllowed=True)
            cat = getToolByName(portal, 'portal_catalog', None)
            if cat is not None:
                topics = cat(portal_type='Topic')
                for b in topics:
                    topic = b.getObject()
                    # If syndication is already enabled then another nasty string
                    # exception gets raised in CMFDefault
                    if topic is not None and not syn.isSyndicationAllowed(topic):
                        syn.enableSyndication(topic)
                        out.append('Enabled syndication on %s'%b.getPath())

    def enableSite(self, portal):
        """
        Make the portal a Zope3 site and create a site manager.
        """
        if not ISite.providedBy(portal):
            make_objectmanager_site(portal)
        # The following event is primarily useful for setting the site hooks
        # during test runs.
        notify(SiteManagerCreatedEvent(portal))

    def assignTitles(self, portal, out):
        titles={'portal_actions':'Contains custom tabs and buttons',
         'portal_membership':'Handles membership policies',
         'portal_memberdata':'Handles the available properties on members',
         'portal_undo':'Defines actions and functionality related to undo',
         'portal_types':'Controls the available content types in your portal',
         'plone_utils':'Various utility methods',
         'portal_metadata':'Controls metadata like keywords, copyrights, etc',
         'portal_registration':'Handles registration of new users',
         'portal_skins':'Controls skin behaviour (search order etc)',
         'portal_syndication':'Generates RSS for folders',
         'portal_workflow':'Contains workflow definitions for your portal',
         'portal_url':'Methods to anchor you to the root of your Plone site',
         'portal_discussion':'Controls how discussions are stored',
         'portal_catalog':'Indexes all content in the site',
         'portal_factory':'Responsible for the creation of content objects',
         'portal_calendar':'Controls how events are shown',
         'portal_quickinstaller':'Allows to install/uninstall products',
         'portal_actionicons':'Associates actions with icons',
         'portal_groupdata':'Handles properties on groups',
         'portal_groups':'Handles group related functionality',
         'translation_service': 'Provides access to the translation machinery',
         'mimetypes_registry': 'MIME types recognized by Plone',
         'portal_transforms': 'Handles data conversion between MIME types',
         }

        for oid in portal.objectIds():
            title=titles.get(oid, None)
            if title:
                setattr(aq_get(portal, oid), 'title', title)
        out.append('Assigned titles to portal tools.')

def importSite(context):
    """
    Import site settings.
    """
    site = context.getSite()
    gen = PloneGenerator()
    gen.enableSite(site)
    setSite(site)

def importArchetypes(context):
    """
    Install Archetypes and it's dependencies.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('plone_archetypes.txt') is None:
        return
    site = context.getSite()
    gen = PloneGenerator()
    gen.installArchetypes(site)

def importVarious(context):
    """
    Import various settings.

    Provisional handler that does initialization that is not yet taken
    care of by other handlers.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('plone_various.txt') is None:
        return
    site = context.getSite()
    gen = PloneGenerator()
    gen.installProducts(site)
    gen.addCacheHandlers(site)
    gen.addCacheForResourceRegistry(site)
    replace_local_role_manager(site)

def importFinalSteps(context):
    """
    Final Plone import steps.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('plone-final.txt') is None:
        return
    out = []
    site = context.getSite()
    pprop = getToolByName(site, 'portal_properties')
    pmembership = getToolByName(site, 'portal_membership')
    gen = PloneGenerator()
    gen.setProfileVersion(site)
    gen.enableSyndication(site, out)
    gen.assignTitles(site, out)
    pmembership.memberareaCreationFlag = False
    gen.installDependencies(site)

def updateWorkflowRoleMappings(context):
    """
    If an extension profile (such as the testfixture one) switches default,
    workflows, this import handler will make sure object security works
    properly.
    """
    site = context.getSite()
    portal_workflow = getToolByName(site, 'portal_workflow')
    portal_workflow.updateRoleMappings()

def replace_local_role_manager(portal):
    """Installs the borg local role manager in place of the standard one from
    PlonePAS"""
    uf = getToolByName(portal, 'acl_users', None)
    # Make sure we have a PAS user folder
    if uf is not None and hasattr(aq_base(uf), 'plugins'):
        # Remove the original plugin if it's there
        if 'local_roles' in uf.objectIds():
            orig_lr = getattr(uf, 'local_roles')
            if isinstance(orig_lr, LocalRolesManager):
                uf.plugins.removePluginById('local_roles')
                logger.info("Deactivated original 'local_roles' plugin")
        # Install the borg.localrole plugin if it's not already there
        logger.info(setup_localrole_plugin(portal))
