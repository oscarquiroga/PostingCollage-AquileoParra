"""
Middleware personalizado para capturar y loguear errores en producción.
"""

import logging
import traceback

logger = logging.getLogger('django')

# Diagnostic startup print to help capture deployment-time context
print("[OK] ErrorLoggingMiddleware loaded")


class ErrorLoggingMiddleware:
    """Middleware para loguear errores detallados en producción."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Loguear el error completo
            logger.error(
                f"Error en {request.method} {request.path}",
                exc_info=True,
                extra={
                    'request': request,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
            )
            raise
        
        return response
