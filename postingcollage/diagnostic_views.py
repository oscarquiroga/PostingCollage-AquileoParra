"""
Diagnostic endpoints for production troubleshooting.
Protected by DIAGNOSTIC_TOKEN environment variable.
"""
import os
import smtplib
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('django')


def _check_diagnostic_token(request):
    """Verify that the request includes the correct DIAGNOSTIC_TOKEN in Authorization header or query param."""
    token = os.environ.get('DIAGNOSTIC_TOKEN')
    if not token:
        return False, "DIAGNOSTIC_TOKEN not configured on server."
    
    # Check Authorization header first (Bearer token)
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        request_token = auth_header.split(' ', 1)[1]
        return request_token == token, None
    
    # Fallback to query parameter
    request_token = request.GET.get('token', '')
    if request_token == token:
        return True, None
    
    return False, "Invalid or missing DIAGNOSTIC_TOKEN."


@require_http_methods(["GET"])
def test_smtp_connection(request):
    """
    Test SMTP connectivity without sending an email.
    
    Requires: DIAGNOSTIC_TOKEN in Authorization header (Bearer token) or ?token=<token> query param.
    
    Returns JSON with connection status and error details (if any).
    """
    # Check authentication
    is_auth, error_msg = _check_diagnostic_token(request)
    if not is_auth:
        return JsonResponse({'error': error_msg or 'Unauthorized'}, status=401)
    
    # Gather SMTP config from settings
    from django.conf import settings
    
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    use_tls = settings.EMAIL_USE_TLS
    user = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    
    # Validate that credentials are present
    if not (host and port and user and password):
        return JsonResponse({
            'ok': False,
            'error': 'SMTP credentials incomplete in settings.',
            'config': {
                'host': host or 'MISSING',
                'port': port or 'MISSING',
                'user': user or 'MISSING',
                'password': '***' if password else 'MISSING',
                'use_tls': use_tls,
            }
        }, status=400)
    
    # Attempt SMTP connection
    try:
        logger.info(f"[SMTP Diagnostic] Attempting connection to {host}:{port} (TLS={use_tls})")
        
        if use_tls:
            server = smtplib.SMTP(host, port, timeout=10)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        
        # Attempt login
        logger.info(f"[SMTP Diagnostic] Attempting login as {user}")
        server.login(user, password)
        
        # If we got here, connection and auth succeeded
        server.quit()
        
        logger.info("[SMTP Diagnostic] SUCCESS - SMTP connection and authentication OK")
        return JsonResponse({
            'ok': True,
            'message': 'SMTP connection and authentication successful.',
            'config': {
                'host': host,
                'port': port,
                'use_tls': use_tls,
                'user': user,
            }
        })
    
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"Authentication failed: {str(e)}"
        logger.error(f"[SMTP Diagnostic] {error_msg}")
        return JsonResponse({
            'ok': False,
            'error': error_msg,
            'type': 'SMTPAuthenticationError',
            'config': {
                'host': host,
                'port': port,
                'use_tls': use_tls,
                'user': user,
            }
        }, status=400)
    
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error: {str(e)}"
        logger.error(f"[SMTP Diagnostic] {error_msg}")
        return JsonResponse({
            'ok': False,
            'error': error_msg,
            'type': 'SMTPException',
        }, status=400)
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(f"[SMTP Diagnostic] {error_msg}")
        return JsonResponse({
            'ok': False,
            'error': error_msg,
            'type': type(e).__name__,
        }, status=500)
