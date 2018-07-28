from django import template
from login.views import getIncompleteTicket

register = template.Library()

# Returns an incomplete ticket ID.
@register.simple_tag
def getTicket():
    return getIncompleteTicket()