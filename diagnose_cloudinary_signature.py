#!/usr/bin/env python
"""
Diagnostic script: Test Cloudinary API credentials and upload.
This helps identify if CLOUDINARY_URL credentials are correct.

Run: python diagnose_cloudinary_signature.py
"""
import os
import sys
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postingcollage.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

import django
from django.conf import settings

print("\n" + "="*70)
print("CLOUDINARY CREDENTIALS DIAGNOSIS")
print("="*70)

# Check if Cloudinary is configured
print("\n1. Configuration Check:")
print("   CLOUDINARY_URL: " + (settings.CLOUDINARY_URL if settings.CLOUDINARY_URL else "NOT SET"))
print("   CLOUDINARY_STORAGE keys: " + str(list(settings.CLOUDINARY_STORAGE.keys())))

# Import cloudinary and check config
import cloudinary
cfg = cloudinary.config()

print("\n2. Parsed Credentials:")
print("   cloud_name: " + (cfg.cloud_name or "N/A"))
api_key_masked = (cfg.api_key[:4] + "..." + cfg.api_key[-4:]) if cfg.api_key else 'N/A'
print("   api_key: " + api_key_masked)
api_secret_masked = (cfg.api_secret[:4] + "..." + cfg.api_secret[-4:]) if cfg.api_secret else 'N/A'
print("   api_secret: " + api_secret_masked + " (masked)")
print("   secure: " + str(cfg.secure))

# Test actual upload
print("\n3. Testing Upload:")
try:
    import cloudinary.uploader
    
    test_url = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    result = cloudinary.uploader.upload(test_url, folder="posts/test")
    
    print("   SUCCESS - Upload worked!")
    print("   Secure URL: " + result.get('secure_url', 'N/A'))
    
except Exception as e:
    error_msg = str(e)
    print("   ERROR - Upload failed: " + type(e).__name__ + ": " + error_msg)
    if "Invalid Signature" in error_msg:
        print("\n   >>> SIGNATURE ERROR DETECTED <<<")
        print("   This means your API_SECRET might be:")
        print("   - Incorrect or malformed")
        print("   - Has leading/trailing spaces")
        print("   - Different between local and Render")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("DIAGNOSIS PASSED")
print("="*70 + "\n")
