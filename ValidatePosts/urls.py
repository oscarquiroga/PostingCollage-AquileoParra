from django.urls import path
from . import views

urlpatterns = [
    path('revisiones/', views.revisiones_view, name='revisiones'),
    path('mis-publicaciones/', views.myposts_view, name='mis-posts'),
    path('reviewstd/<int:post_id>/', views.update_posts, name='actualizar'),
    path('nueva-publicacion/', views.createposts_view, name='nueva-publicacion'),
    path("review/<int:post_id>/", views.review_detail, name="review"),
]