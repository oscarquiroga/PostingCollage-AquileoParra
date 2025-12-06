from django.core.mail import send_mail
from django.contrib import messages
import logging
import os
import json
import urllib.request
import urllib.error
from .forms import SupportForm
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from ValidatePosts.models import Post, Like
from django.db.models import Count, F, Q
from django.contrib.auth.decorators import login_required

def home(request):
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

            logger = logging.getLogger('django')

            # Prefer SendGrid HTTP API if SENDGRID_API_KEY is configured (works on Render)
            sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
            if sendgrid_api_key:
                try:
                    url = 'https://api.sendgrid.com/v3/mail/send'
                    payload = {
                        'personalizations': [{
                            'to': [{'email': 'xazadox@gmail.com'}],
                            'subject': f"[SOPORTE] {title}"
                        }],
                        'from': {'email': settings.EMAIL_HOST_USER},
                        'content': [{'type': 'text/plain', 'value': message}]
                    }
                    data = json.dumps(payload).encode('utf-8')
                    req = urllib.request.Request(url, data=data, method='POST')
                    req.add_header('Authorization', f'Bearer {sendgrid_api_key}')
                    req.add_header('Content-Type', 'application/json')
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        status = resp.getcode()
                        if 200 <= status < 300:
                            messages.success(request, "Tu mensaje de soporte ha sido enviado correctamente.")
                            return redirect('support')
                        else:
                            logger.error(f"SendGrid returned status {status}")
                            messages.error(request, "No se pudo enviar el mensaje de soporte. Intenta de nuevo más tarde.")
                            return redirect('support')
                except urllib.error.HTTPError as e:
                    body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
                    logger.exception(f"SendGrid HTTPError: {body}")
                    messages.error(request, "No se pudo enviar el mensaje de soporte (error de proveedor).")
                    return redirect('support')
                except Exception as e:
                    logger.exception("Unexpected error sending support email via SendGrid")
                    messages.error(request, "No se pudo enviar el mensaje de soporte en este momento. Intenta de nuevo más tarde.")
                    return redirect('support')

            # Fallback to Django SMTP send_mail
            try:
                send_mail(
                    subject=f"[SOPORTE] {title}",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=["xazadox@gmail.com"],
                )
            except Exception as e:
                # Log full exception for server-side diagnostics, but show friendly message to user
                logger.exception("Error sending support email via SMTP")
                messages.error(request, "No se pudo enviar el mensaje de soporte en este momento. Intenta de nuevo más tarde.")
                return redirect("support")

            messages.success(request, "Tu mensaje de soporte ha sido enviado correctamente.")
            return redirect("support")

    else:
        form = SupportForm()

    return render(request, "soporte.html", {"form": form})

def about(request):
    return render(request, "about.html")