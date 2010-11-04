## Script (Python) "require_login"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Login
##

request = context.REQUEST

# Handle external login requests from other portals where the user is already
# logged in in this portal
next = request.get('next', None)
if (next is not None and context.portal_url.isURLInPortal(next) 
    and context.portal_membership.isAnonymousUser()):
    return context.restrictedTraverse('external_login_return')()

# Handle login on this portal where login is internal
external_login_url = context.portal_properties.site_properties.getProperty('external_login_url')
if not external_login_url:
    return context.restrictedTraverse('login_form')()

# Handle login on this portal where login is external
portal_url = context.portal_url()
came_from = request.get('came_from', portal_url)
next = portal_url + '/acl_users/session/external_login'
url = "%s?came_from=%s&next=%s" % (external_login_url, came_from, next)
request.RESPONSE.redirect(url)
