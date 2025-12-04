from django.http import JsonResponse, HttpResponseServerError
import cloudinary.uploader
import traceback


def cloudinary_test_upload(request):
    """Diagnostic view: attempt a simple upload to Cloudinary and return JSON result.

    - Uploads a public image URL to Cloudinary using the configured SDK.
    - Returns JSON with `secure_url` on success.
    - On exception, returns 500 and the full traceback text (so it appears in deploy logs).
    Note: This endpoint is temporary and should be removed after debugging.
    """
    test_image = (
        "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    )
    try:
        result = cloudinary.uploader.upload(test_image)
        return JsonResponse({
            "ok": True,
            "secure_url": result.get('secure_url'),
            "raw_result_keys": list(result.keys())[:20],
        })
    except Exception as exc:
        tb = traceback.format_exc()
        # Return as plain text so logs include full traceback
        return HttpResponseServerError(f"Upload failed:\n{tb}")
