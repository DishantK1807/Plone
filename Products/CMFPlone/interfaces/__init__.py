# interface definitions

from properties import IPropertiesTool
from properties import ISimpleItemWithProperties
from basetool import IPloneBaseTool
from basetool import IPloneTool
from events import ISiteManagerCreatedEvent
from installable import INonInstallable
from siteroot import IPloneSiteRoot
from siteroot import IMigratingPloneSiteRoot
from siteroot import ITestCasePloneSiteRoot
from constrains import IConstrainTypes
from constrains import ISelectableConstrainTypes
from structure import INonStructuralFolder
from view import IBrowserDefault
from view import ISelectableBrowserDefault
from view import IDynamicViewTypeInformation
from factory import IFactoryTool
from translationservice import ITranslationServiceTool
from breadcrumbs import IHideFromBreadcrumbs

import zope.deferredimport
zope.deferredimport.deprecated(
    "It has been moved to plone.app.workflow.interfaces. " 
    "This alias will be removed in Plone 5.0",
    IWorkflowChain = 'plone.app.workflow.interfaces:IWorkflowChain',
    )
