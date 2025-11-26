from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("post/<int:post_id>/", views.view_post, name="view_post"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("soporte/", views.support_view, name="support"),
    path("about/", views.about, name="about"),
    path("buscar/", views.search_posts, name="search_posts"),
]