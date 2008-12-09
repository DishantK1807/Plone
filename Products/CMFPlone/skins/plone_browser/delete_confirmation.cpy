## Controlled Python Script "delete_confirmation"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Redirects to the regular page
##

return state.set(status='confirm')
