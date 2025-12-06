"""
URL configuration for postingcollage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from postingcollage import ckeditor_handler, diagnostic_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("RegisterUsers.urls")),
    path("", include("Publicates.urls")),
    path("publicaciones/", include("ValidatePosts.urls")),
    # Override the default CKEditor upload endpoint with our custom handler
    path('ckeditor5/image_upload/', ckeditor_handler.ckeditor_upload),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # Diagnostic endpoints (protected by DIAGNOSTIC_TOKEN env var)
    path('diagnostic/test-smtp/', diagnostic_views.test_smtp_connection, name='test_smtp'),
]

# Custom error handlers for production (redirect to home on errors)
handler404 = 'postingcollage.error_views.handler404'
handler500 = 'postingcollage.error_views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
