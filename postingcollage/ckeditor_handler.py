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
        
        # Upload to Cloudinary using the SDK directly
        # This bypasses django-cloudinary-storage which may have issues
        try:
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
            
            return JsonResponse({
                'error': {
                    'message': f'Cloudinary upload failed: {error_msg}'
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
