from zope.app.container.contained import notifyContainerModified

from AccessControl import ClassSecurityInfo
from DocumentTemplate.sequence import sort
from App.class_init import InitializeClass
from OFS.Folder import Folder
from OFS.ObjectManager import REPLACEABLE
from zExceptions import NotFound

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent


class ReplaceableWrapper:
    """A wrapper around an object to make it replaceable."""
    def __init__(self, ob):
        self.__ob = ob

    def __getattr__(self, name):
        if name == '__replaceable__':
            return REPLACEABLE
        return getattr(self.__ob, name)

# Portions of this class was copy/pasted from the OFS.Folder.OrderedFolder
# from Zope2.7.  This class is licensed under the ZPL 2.0 as stated here:
# http://www.zope.org/Resources/ZPL
# Zope Public License (ZPL) Version 2.0
# This software is Copyright (c) Zope Corporation (tm) and Contributors.
# All rights reserved.

class OrderedContainer(Folder):
    """Folder with subobject ordering support."""

    security = ClassSecurityInfo()

    security.declareProtected(ModifyPortalContent, 'moveObject')
    def moveObject(self, id, position):
        obj_idx  = self.getObjectPosition(id)
        if obj_idx == position:
            return None
        elif position < 0:
            position = 0

        metadata = list(self._objects)
        obj_meta = metadata.pop(obj_idx)
        metadata.insert(position, obj_meta)
        self._objects = tuple(metadata)

    # Here the implementation of IOrderedContainer starts
    # Once Plone depends on Zope 2.7 this should be replaced by mixing in
    # the 2.7 specific class OFS.OrderedContainer.OrderedContainer

    security.declareProtected(ModifyPortalContent, 'moveObjectsByDelta')
    def moveObjectsByDelta(self, ids, delta, subset_ids=None,
                           suppress_events=False):
        """Move specified sub-objects by delta."""
        if isinstance(ids, basestring):
            ids = (ids,)
        min_position = 0
        objects = list(self._objects)
        if subset_ids == None:
            subset_ids = self.getCMFObjectsSubsetIds(objects)
        else:
            subset_ids = list(subset_ids)
        # unify moving direction
        if delta > 0:
            ids = list(ids)
            ids.reverse()
            subset_ids.reverse()
        counter = 0

        for id in ids:
            try:
                old_position = subset_ids.index(id)
            except ValueError:
                continue
            new_position = max(old_position - abs(delta), min_position)
            if new_position == min_position:
                min_position += 1
            if not old_position == new_position:
                subset_ids.remove(id)
                subset_ids.insert(new_position, id)
                counter += 1

        if counter > 0:
            if delta > 0:
                subset_ids.reverse()
            obj_dict = {}
            for obj in objects:
                obj_dict[obj['id']] = obj
            pos = 0
            for i in range(len(objects)):
                if objects[i]['id'] in subset_ids:
                    try:
                        objects[i] = obj_dict[subset_ids[pos]]
                        pos += 1
                    except KeyError:
                        raise ValueError('The object with the id "%s" does '
                                         'not exist.' % subset_ids[pos])
            self._objects = tuple(objects)

        if not suppress_events:
            notifyContainerModified(self)

        return counter

    security.declarePrivate('getCMFObjectsSubsetIds')
    def getCMFObjectsSubsetIds(self, objs):
        """Get the ids of only cmf objects (used for moveObjectsByDelta)."""
        ttool = getToolByName(self, 'portal_types')
        cmf_meta_types = [ti.Metatype() for ti in ttool.listTypeInfo()]
        return [obj['id'] for obj in objs if obj['meta_type'] in cmf_meta_types]

    security.declareProtected(ModifyPortalContent, 'getObjectPosition')
    def getObjectPosition(self, id):

        objs = list(self._objects)
        om = [objs.index(om) for om in objs if om['id']==id]

        if om: # only 1 in list if any
            return om[0]

        raise NotFound, 'Object %s was not found' % str(id)

    security.declareProtected(ModifyPortalContent, 'moveObjectsUp')
    def moveObjectsUp(self, ids, delta=1, RESPONSE=None):
        """Move an object up."""
        self.moveObjectsByDelta(ids, -delta)
        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(ModifyPortalContent, 'moveObjectsDown')
    def moveObjectsDown(self, ids, delta=1, RESPONSE=None):
        """Move an object down."""
        self.moveObjectsByDelta(ids, delta)
        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(ModifyPortalContent, 'moveObjectsToTop')
    def moveObjectsToTop(self, ids, RESPONSE=None):
        """Move an object to the top."""
        self.moveObjectsByDelta(ids, - len(self._objects))
        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(ModifyPortalContent, 'moveObjectsToBottom')
    def moveObjectsToBottom(self, ids, RESPONSE=None):
        """Move an object to the bottom."""
        self.moveObjectsByDelta(ids, len(self._objects))
        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(ModifyPortalContent, 'moveObjectToPosition')
    def moveObjectToPosition(self, id, position, suppress_events=False):
        """Move specified object to absolute position."""
        delta = position - self.getObjectPosition(id)
        return self.moveObjectsByDelta(id, delta,
                                       suppress_events=suppress_events)

    security.declareProtected(ModifyPortalContent, 'orderObjects')
    def orderObjects(self, key, reverse=None):
        """Order sub-objects by key and direction."""
        ids = [id for id, obj in sort(self.objectItems(),
                                      ((key, 'cmp', 'asc'),))]
        if reverse:
            ids.reverse()
        return self.moveObjectsByDelta(ids, -len(self._objects))

    # Here the implementation of IOrderedContainer ends

    def manage_renameObject(self, id, new_id, REQUEST=None):
        """Rename a particular sub-object."""
        objidx = self.getObjectPosition(id)
        method = OrderedContainer.inheritedAttribute('manage_renameObject')
        result = method(self, id, new_id, REQUEST)
        self.moveObject(new_id, objidx)
        putils = getToolByName(self, 'plone_utils')
        putils.reindexOnReorder(self)
        return result

InitializeClass(OrderedContainer)
