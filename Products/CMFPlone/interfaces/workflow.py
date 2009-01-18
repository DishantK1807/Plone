import zope.deferredimport
zope.deferredimport.deprecated(
    "It has been moved to plone.app.workflow.interfaces. " 
    "This alias will be removed in Plone 5.0",
    IWorkflowChain = 'plone.app.workflow.interfaces:IWorkflowChain',
    )
