"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the 'context_processors' option of the configuration
of a DjangoTemplates backend and used by RequestContext.
"""

from django.conf import settings

def site_constants(request):
    return {
        "site_title": settings.DEFAULT_SITE_NAME
    }