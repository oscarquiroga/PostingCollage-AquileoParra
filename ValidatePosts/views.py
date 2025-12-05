from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import PostForm, ReviewPostForm, StudentReviewForm
from .models import Post
import cloudinary.uploader


@login_required
def createposts_view(request):
    if request.method == 'POST':
        fm = PostForm(request.POST, request.FILES)
        if fm.is_valid():
            post = fm.save(commit=False)
            post.user = request.user
            # Handle manual upload of files to Cloudinary to avoid CloudinaryField pre_save signature issues
            try:
                # Image field
                img_file = request.FILES.get('imgs')
                if img_file:
                    res = cloudinary.uploader.upload(img_file, folder='posts/images', resource_type='image', type='upload')
                    # Store the public_id in the CloudinaryField (prevents double-upload)
                    post.imgs = res.get('public_id')

                # Attachment field (raw files)
                attachment_file = request.FILES.get('attachment')
                if attachment_file:
                    res_att = cloudinary.uploader.upload(attachment_file, folder='posts/files', resource_type='auto', type='upload')
                    post.attachment = res_att.get('public_id')
            except Exception:
                # If cloudinary upload fails here, raise so the error appears in logs
                raise

            post.save()
            return redirect('home')
    else:
        fm = PostForm()

    return render(request, 'createposts.html', {
        'form': fm
    })

@login_required
def myposts_view(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'myposts.html', {
        'posts' : posts
    })
    

@login_required
def revisiones_view(request):
    estado = request.GET.get("estado", None)

    posts = Post.objects.filter().order_by("-id")

    if estado in ["pending", "approved", "rejected"]:
        posts = posts.filter(status=estado)

    return render(request, "checkposts.html", {
        "posts": posts,
        "estado": estado,
    })





@login_required
def review_detail(request, post_id):
    if request.user.role != "profesor":
        return HttpResponseForbidden("No tienes permisos para ver esta página.")

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = ReviewPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("revisiones")
    else:
        form = ReviewPostForm(instance=post)

    return render(request, "review_detail.html", {
        "post": post,
        "form": form
    })

def update_posts(request, post_id):    
    post = get_object_or_404(Post, id=post_id)

    # Solo el autor del post puede editarlo
    if post.user != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a este post.")

    if request.method == "POST":
        form = StudentReviewForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.status = "pending"   # Siempre vuelve a pendiente
            edited_post.save()
            return redirect("mis-posts")
    else:
        form = StudentReviewForm(instance=post)

    return render(request, "review_student.html", {
        "post": post,
        "form": form
    })