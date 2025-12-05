"""
Custom error handlers for production.

Redirects all 404 and 500 errors to home instead of displaying error pages.
"""
from django.shortcuts import redirect


def handler404(request, exception=None):
    """Handle 404 (not found) errors by redirecting to home."""
    return redirect('home')


def handler500(request):
    """Handle 500 (server error) errors by redirecting to home."""
    return redirect('home')
