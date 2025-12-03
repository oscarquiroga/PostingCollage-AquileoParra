from django.core.mail import send_mail
from django.contrib import messages
from .forms import SupportForm
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from ValidatePosts.models import Post, Like
from django.db.models import Count, F, Q
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import os

def home(request):
    print(default_storage)
    posts = Post.objects.filter(status="approved").annotate(
        likes_count=Count("likes")
    ).order_by("-likes_count", "-created_at")

    return render(request, "home.html", {"posts": posts})


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="approved")

    # Sumar vista
    Post.objects.filter(id=post_id).update(views=F('views') + 1)
    post.refresh_from_db()
    
    if hasattr(post, "get_tags"):
        tags = post.get_tags()  # si implementaste get_tags()
    else:
        raw = getattr(post, "tags", "") or ""
        # dividir por comas y limpiar
        tags = [t.strip() for t in raw.split(",") if t.strip()]

    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, "view_post.html", {
        "post": post,
        "user_liked": user_liked,
        "tags": tags,
    })


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="approved")

    existing = Like.objects.filter(post=post, user=request.user)

    if existing.exists():
        existing.delete()   # 👈 Quitar like
    else:
        Like.objects.create(post=post, user=request.user)

    return redirect("view_post", post_id=post_id)

def search_posts(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(id__icontains=query) |      
            Q(tags__icontains=query) 
        ).filter(status="approved") 

    return render(request, "search_results.html", {
        "query": query,
        "results": results,
    })
@login_required
def support_view(request):
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            user_name = request.user.username if request.user.is_authenticated else "Usuario no autenticado"
            user_email = request.user.email if request.user.is_authenticated else "No proporcionado"

            message = (
                f"📌 *Nuevo mensaje de soporte*\n\n"
                f"👤 Usuario: {user_name}\n"
                f"📧 Email: {user_email}\n\n"
                f"📌 *Título:*\n{title}\n\n"
                f"📝 *Descripción:*\n{description}"
            )

            send_mail(
                subject=f"[SOPORTE] {title}",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["xazadox@gmail.com"],
            )

            messages.success(request, "Tu mensaje de soporte ha sido enviado correctamente.")
            return redirect("support")

    else:
        form = SupportForm()

    return render(request, "soporte.html", {"form": form})

def about(request):
    return render(request, "about.html")