from Acquisition import aq_base

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.interfaces import IPloneSiteRoot


class NotFoundPage(BrowserView):
    """Page to be shown in case of NotFound errors."""

    index = ViewPageTemplateFile('notfound.pt')

    def __call__(self):
        self.exception = self.context

        context = None
        plonesite = False
        for parent in self.request.get('PARENTS'):
            traverse = getattr(aq_base(parent), 'restrictedTraverse', None)
            if context is None and traverse is not None:
                # Set the first traversable parent as the context, this avoids
                # for example resource directories being used as a context
                context = parent
            if IPloneSiteRoot.providedBy(parent):
                # Check if a Plone site is somewhere in the parents
                plonesite = True

        if plonesite:
            # The error view is registered globally, but the template depends
            # on being rendered inside a Plone site context
            self.context = context
            return self.index()

        # Return the exception itself
        return self.context
