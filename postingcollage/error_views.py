"""
Custom error handlers for production.

Redirects all 404 and 500 errors to home instead of displaying error pages.
"""
from django.shortcuts import render
from Publicates.views import home as home_view


def handler404(request, exception=None):
    """Handle 404 (not found) by returning the home view content with 404 status.

    Returning the home page content (instead of issuing a redirect) avoids
    creating redirect loops when the URL resolution unexpectedly raises 404.
    """
    response = home_view(request)
    response.status_code = 404
    return response


def handler500(request):
    """Handle 500 (server error) by returning the home view content with 500 status."""
    response = home_view(request)
    response.status_code = 500
    return response
