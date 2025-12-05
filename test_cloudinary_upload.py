#!/usr/bin/env python
"""
Test script: Verify Cloudinary upload works without needing DB connection.
Run: python test_cloudinary_upload.py
"""
import os
import sys
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postingcollage.settings')

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import django
# Configure Django but skip DB checks
from django.conf import settings

print("\n" + "="*70)
print("CLOUDINARY UPLOAD TEST")
print("="*70)

# Check settings
print(f"\n1. Settings Check:")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"   CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")

# Test upload
print(f"\n2. Testing Cloudinary upload...")
try:
    import cloudinary.uploader
    
    test_image_url = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
    print(f"   Uploading from: {test_image_url}")
    
    result = cloudinary.uploader.upload(test_image_url)
    
    print(f"\n[SUCCESS] Upload worked!")
    print(f"   Secure URL: {result.get('secure_url')}")
    print(f"   Public ID: {result.get('public_id')}")
    print(f"   Format: {result.get('format')}")
    print(f"   Size: {result.get('bytes')} bytes")
    
except Exception as e:
    print(f"\n[ERROR] Upload failed:")
    print(f"   {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("TEST PASSED - Cloudinary is ready!")
print("="*70 + "\n")
