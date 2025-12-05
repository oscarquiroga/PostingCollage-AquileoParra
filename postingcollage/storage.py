"""
Custom storage backend that wraps cloudinary_storage.MediaCloudinaryStorage
to add missing attributes expected by django-ckeditor-5.
"""
from cloudinary_storage.storage import MediaCloudinaryStorage as BaseMediaCloudinaryStorage


class CloudinaryMediaStorage(BaseMediaCloudinaryStorage):
    """
    Extends MediaCloudinaryStorage to provide compatibility with django-ckeditor-5.
    
    Adds the 'location' attribute that django-ckeditor-5 may expect when deleting files.
    """
    
    @property
    def location(self):
        """
        Return a dummy location for compatibility with django-ckeditor-5.
        
        Since files are stored in Cloudinary (cloud), there's no filesystem location.
        Return 'cloudinary:' as a marker.
        """
        return 'cloudinary:'
