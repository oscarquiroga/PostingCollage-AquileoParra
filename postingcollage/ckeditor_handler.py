"""
Custom CKEditor upload handler that works with Cloudinary storage backend.
Provides better error handling and logging for uploads to Cloudinary.
"""
import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cloudinary.uploader
import cloudinary
import os

logger = logging.getLogger('django')


@require_http_methods(["POST"])
@csrf_exempt  # CKEditor sends CSRF token in header, not form
def ckeditor_upload(request):
    """
    Unified upload endpoint for CKEditor5.
    
    Accepts multipart file upload and stores it in Cloudinary.
    Returns JSON response compatible with CKEditor5 upload adapter.
    """
    try:
        # Get the uploaded file
        if 'upload' not in request.FILES:
            return JsonResponse({
                'error': {'message': 'No file provided'}
            }, status=400)
        
        uploaded_file = request.FILES['upload']
        
        logger.info(f"[CKEditor Upload] Received file: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Read file content
        file_content = uploaded_file.read()
        
        # Ensure Cloudinary SDK is configured in this process (helps in some PaaS cases)
        try:
            cfg = cloudinary.config()
        except Exception:
            cfg = None

        if not (cfg and getattr(cfg, 'api_secret', None)):
            # Attempt to parse CLOUDINARY_URL environment variable as a fallback
            cloudinary_url = os.environ.get('CLOUDINARY_URL')
            if cloudinary_url and cloudinary_url.startswith('cloudinary://'):
                try:
                    # Format: cloudinary://api_key:api_secret@cloud_name
                    url_part = cloudinary_url.replace('cloudinary://', '', 1)
                    creds_part, cn = url_part.rsplit('@', 1)
                    ak, as_ = creds_part.split(':', 1)
                    cloudinary.config(cloud_name=cn, api_key=ak, api_secret=as_, secure=True)
                    cfg = cloudinary.config()
                except Exception as e:
                    logger.error(f"[CKEditor Upload] Failed to parse CLOUDINARY_URL: {str(e)}")

        # Upload to Cloudinary using the SDK directly. This bypasses django-cloudinary-storage.
        try:
            # Log non-sensitive config diagnostic
            try:
                cfg = cloudinary.config()
                logger.info(f"[CKEditor Upload] cloud_name={getattr(cfg, 'cloud_name', None)}, api_key_present={bool(getattr(cfg, 'api_key', None))}")
            except Exception:
                logger.info("[CKEditor Upload] cloudinary.config() unavailable")

            result = cloudinary.uploader.upload(
                file_content,
                folder='posts/ckeditor',
                resource_type='auto',
                type='upload',
            )
            
            logger.info(f"[CKEditor Upload] SUCCESS: {result.get('public_id')}")
            
            # Return CKEditor-compatible response
            return JsonResponse({
                'url': result.get('secure_url'),
                'uploaded': 1,
            })
            
        except Exception as upload_error:
            error_msg = str(upload_error)
            logger.error(f"[CKEditor Upload] Cloudinary upload failed: {error_msg}")

            # If the error mentions an invalid signature, include guidance in the response
            help_msg = 'Cloudinary upload failed.'
            if 'Invalid Signature' in error_msg or 'signature' in error_msg.lower():
                help_msg = (
                    'Cloudinary reported an invalid signature. Verifica que la variable de entorno '
                    'CLOUDINARY_URL esté correctamente configurada en producción (sin comillas ni espacios). '
                    'Reinicia el servicio después de cambiar variables de entorno.'
                )

            return JsonResponse({
                'error': {
                    'message': f'{help_msg} ({error_msg})'
                }
            }, status=500)
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"[CKEditor Upload] Exception: {type(e).__name__}: {error_msg}", exc_info=True)
        
        return JsonResponse({
            'error': {
                'message': f'Upload failed: {error_msg}'
            }
        }, status=500)
