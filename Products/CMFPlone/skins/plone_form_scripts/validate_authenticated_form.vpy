## Controlled Python Script "validate_authenticated_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates a CSRF protection authenticator token
##
from AccessControl import Unauthorized
authenticator = context.restrictedTraverse('@@authenticator', None)
if authenticator is not None and not authenticator.verify():
    raise Unauthorized, 'invalid authenticator token'
return state
