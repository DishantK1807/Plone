## Script (Python) "require_login"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Login
##

login = 'login_form'

portal = context.portal_url.getPortalObject()
# if cookie crumbler did a traverse instead of a redirect,
# this would be the way to get the value of came_from
#url = portal.getCurrentUrl()
#context.REQUEST.set('came_from', url)

if context.portal_membership.isAnonymousUser():
    return portal.restrictedTraverse(login)()

next = context.REQUEST.get('next', None)
if next is not None and context.portal_url.isURLInPortal(next):
    return portal.restrictedTraverse('external_login_return')()

return portal.restrictedTraverse('insufficient_privileges')()
